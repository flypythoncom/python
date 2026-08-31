#!/usr/bin/env python3
"""Safely check links declared in ``_data/resources.yml``."""

from __future__ import annotations

import argparse
import ipaddress
import json
import math
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Protocol
from urllib.parse import urljoin, urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from tools.catalog import CatalogLoadError, catalog_resources, load_catalog, validate_catalog
except ModuleNotFoundError:  # Direct ``python tools/check_links.py`` execution.
    from catalog import CatalogLoadError, catalog_resources, load_catalog, validate_catalog


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = ROOT_DIR / "_data" / "resources.yml"
DEFAULT_OUTPUT = ROOT_DIR / "reports" / "link_check_results.json"
DEFAULT_BASE_URL = "https://python.flypython.com/"
REVIEW_STATUS_CODES = {403, 408, 425, 429}
RETRY_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}
KNOWN_METADATA_HOSTS = {
    "instance-data",
    "metadata",
    "metadata.google.internal",
    "metadata.google",
}
KNOWN_METADATA_IPS = {
    ipaddress.ip_address("169.254.169.254"),
    ipaddress.ip_address("100.100.100.200"),
    ipaddress.ip_address("fd00:ec2::254"),
}


class UnsafeTarget(ValueError):
    """Raised before a request can reach a non-public network target."""


@dataclass(frozen=True)
class ResolvedTarget:
    host: str
    port: int
    addresses: tuple[str, ...]


class Resolver(Protocol):
    def __call__(self, host: str, port: int) -> Iterable[str]: ...


def _system_resolver(host: str, port: int) -> Iterable[str]:
    for family, _, _, _, sockaddr in socket.getaddrinfo(
        host, port, type=socket.SOCK_STREAM
    ):
        if family in (socket.AF_INET, socket.AF_INET6):
            yield sockaddr[0]


def _is_unsafe_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return address in KNOWN_METADATA_IPS or not address.is_global


class SafeTargetGuard:
    """Validate targets and return only public IPs for connection pinning."""

    def __init__(self, resolver: Resolver | None = None) -> None:
        self._resolver = resolver or _system_resolver

    def resolve_url(self, url: str) -> ResolvedTarget:
        try:
            parsed = urlsplit(url)
            port = parsed.port
        except ValueError as exc:
            raise UnsafeTarget(f"invalid URL: {exc}") from exc
        if parsed.scheme.lower() not in {"http", "https"}:
            raise UnsafeTarget("only HTTP and HTTPS URLs are allowed")
        if parsed.username or parsed.password:
            raise UnsafeTarget("URLs with credentials are not allowed")
        if not parsed.hostname:
            raise UnsafeTarget("URL must include a hostname")
        try:
            host = parsed.hostname.rstrip(".").encode("idna").decode("ascii").lower()
        except UnicodeError as exc:
            raise UnsafeTarget("hostname is not valid IDNA") from exc
        if host == "localhost" or host.endswith(".localhost"):
            raise UnsafeTarget("localhost targets are blocked")
        if host in KNOWN_METADATA_HOSTS or host.endswith(".metadata.google.internal"):
            raise UnsafeTarget("cloud metadata targets are blocked")
        port = port or (443 if parsed.scheme.lower() == "https" else 80)

        try:
            literal = ipaddress.ip_address(host)
        except ValueError:
            try:
                raw_addresses = tuple(self._resolver(host, port))
            except OSError as exc:
                raise requests.ConnectionError(f"DNS lookup failed for {host}: {exc}") from exc
            if not raw_addresses:
                raise requests.ConnectionError(f"DNS lookup returned no addresses for {host}")
        else:
            raw_addresses = (str(literal),)

        addresses: set[str] = set()
        for raw_address in raw_addresses:
            try:
                address = ipaddress.ip_address(raw_address.split("%", 1)[0])
            except ValueError as exc:
                raise UnsafeTarget(f"DNS returned an invalid address: {raw_address}") from exc
            if _is_unsafe_ip(address):
                raise UnsafeTarget(f"non-public target is blocked: {address}")
            addresses.add(address.compressed)
        return ResolvedTarget(host, port, tuple(sorted(addresses)))


class PinnedDNSHTTPAdapter(HTTPAdapter):
    """Pin each request hop to a validated IP to prevent DNS rebinding."""

    def __init__(self, guard: SafeTargetGuard, *args: Any, **kwargs: Any) -> None:
        self.guard = guard
        super().__init__(*args, **kwargs)

    def get_connection_with_tls_context(
        self,
        request: requests.PreparedRequest,
        verify: bool | str,
        proxies: Mapping[str, str] | None = None,
        cert: Any = None,
    ) -> Any:
        if proxies:
            raise requests.ProxyError("proxies are disabled for safe link checks")
        target = self.guard.resolve_url(request.url or "")
        host_params, pool_kwargs = self.build_connection_pool_key_attributes(
            request, verify, cert
        )
        scheme = str(host_params["scheme"]).lower()
        original_host = target.host
        display_host = f"[{original_host}]" if ":" in original_host else original_host
        default_port = (scheme == "https" and target.port == 443) or (
            scheme == "http" and target.port == 80
        )
        request.headers["Host"] = (
            display_host if default_port else f"{display_host}:{target.port}"
        )
        host_params["host"] = target.addresses[0]
        host_params["port"] = target.port
        if scheme == "https":
            pool_kwargs["assert_hostname"] = original_host
            pool_kwargs["server_hostname"] = original_host
        return self.poolmanager.connection_from_host(
            **host_params, pool_kwargs=pool_kwargs
        )


def build_session(
    guard: SafeTargetGuard, *, retries: int, backoff_factor: float
) -> requests.Session:
    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        status=retries,
        allowed_methods=frozenset({"HEAD", "GET"}),
        status_forcelist=RETRY_STATUS_CODES,
        backoff_factor=backoff_factor,
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = PinnedDNSHTTPAdapter(
        guard, max_retries=retry, pool_connections=4, pool_maxsize=4
    )
    session = requests.Session()
    session.trust_env = False
    session.headers.update(
        {
            "User-Agent": "FlyPythonCatalogLinkChecker/1.0 (+https://github.com/flypythoncom/python)",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.8,*/*;q=0.5",
        }
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class ThreadLocalSessions:
    def __init__(self, factory: Callable[[], Any]) -> None:
        self._factory = factory
        self._local = threading.local()
        self._lock = threading.Lock()
        self._sessions: list[Any] = []

    def get(self) -> Any:
        session = getattr(self._local, "session", None)
        if session is None:
            session = self._factory()
            self._local.session = session
            with self._lock:
                self._sessions.append(session)
        return session

    def close_all(self) -> None:
        with self._lock:
            sessions, self._sessions = self._sessions, []
        for session in sessions:
            close = getattr(session, "close", None)
            if callable(close):
                close()


class HostRateLimiter:
    def __init__(self, min_interval: float) -> None:
        self.min_interval = min_interval
        self._master_lock = threading.Lock()
        self._locks: dict[str, threading.Lock] = {}
        self._last_request: dict[str, float] = {}

    def wait(self, url: str) -> None:
        if self.min_interval <= 0:
            return
        host = (urlsplit(url).hostname or "").lower()
        with self._master_lock:
            lock = self._locks.setdefault(host, threading.Lock())
        with lock:
            elapsed = time.monotonic() - self._last_request.get(host, 0.0)
            delay = self.min_interval - elapsed
            if delay > 0:
                time.sleep(delay)
            self._last_request[host] = time.monotonic()


@dataclass(frozen=True)
class CatalogLink:
    id: str
    path: str
    title: str
    url: str


@dataclass
class LinkResult:
    id: str
    path: str
    title: str
    url: str
    status: str
    status_code: int | None = None
    method: str | None = None
    final_url: str | None = None
    history: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None


def _history(response: Any) -> list[dict[str, Any]]:
    return [
        {
            "status_code": item.status_code,
            "url": item.url,
            "location": item.headers.get("Location"),
        }
        for item in getattr(response, "history", [])
    ]


def classify_status(status_code: int, *, redirected: bool) -> str:
    if 200 <= status_code < 300:
        return "redirect" if redirected else "working"
    if 300 <= status_code < 400:
        return "redirect"
    if status_code in REVIEW_STATUS_CODES or status_code >= 500:
        return "review"
    if 400 <= status_code < 500:
        return "broken"
    return "review"


class LinkChecker:
    def __init__(
        self,
        *,
        timeout: float = 10.0,
        workers: int = 8,
        retries: int = 2,
        backoff_factor: float = 0.5,
        min_interval: float = 0.2,
        guard: SafeTargetGuard | None = None,
        session_factory: Callable[[], Any] | None = None,
    ) -> None:
        self.timeout = timeout
        self.workers = workers
        self.guard = guard or SafeTargetGuard()
        factory = session_factory or (
            lambda: build_session(
                self.guard, retries=retries, backoff_factor=backoff_factor
            )
        )
        self.sessions = ThreadLocalSessions(factory)
        self.rate_limiter = HostRateLimiter(min_interval)

    def _request(self, session: Any, method: str, url: str) -> Any:
        self.rate_limiter.wait(url)
        kwargs: dict[str, Any] = {"timeout": self.timeout, "allow_redirects": True}
        if method == "GET":
            kwargs["stream"] = True
            return session.get(url, **kwargs)
        return session.head(url, **kwargs)

    def check_one(self, link: CatalogLink) -> LinkResult:
        try:
            self.guard.resolve_url(link.url)
            session = self.sessions.get()
            head = self._request(session, "HEAD", link.url)
            try:
                if head.status_code < 400:
                    history = _history(head)
                    return LinkResult(
                        link.id,
                        link.path,
                        link.title,
                        link.url,
                        classify_status(head.status_code, redirected=bool(history)),
                        status_code=head.status_code,
                        method="HEAD",
                        final_url=head.url,
                        history=history,
                    )
            finally:
                head.close()

            response = self._request(session, "GET", link.url)
            try:
                history = _history(response)
                return LinkResult(
                    link.id,
                    link.path,
                    link.title,
                    link.url,
                    classify_status(response.status_code, redirected=bool(history)),
                    status_code=response.status_code,
                    method="GET",
                    final_url=response.url,
                    history=history,
                )
            finally:
                response.close()
        except UnsafeTarget as exc:
            return LinkResult(
                link.id, link.path, link.title, link.url, "blocked", error=str(exc)
            )
        except requests.Timeout as exc:
            return LinkResult(
                link.id, link.path, link.title, link.url, "review", error=f"timeout: {exc}"
            )
        except requests.RequestException as exc:
            return LinkResult(
                link.id,
                link.path,
                link.title,
                link.url,
                "review",
                error=f"request failed: {exc}",
            )
        except Exception as exc:  # Surface checker defects without aborting other workers.
            return LinkResult(
                link.id,
                link.path,
                link.title,
                link.url,
                "error",
                error=f"unexpected checker error: {exc}",
            )

    def check_all(self, links: Iterable[CatalogLink]) -> list[LinkResult]:
        link_list = list(links)
        results: list[LinkResult] = []
        try:
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = {
                    executor.submit(self.check_one, link): link for link in link_list
                }
                for future in as_completed(futures):
                    results.append(future.result())
        finally:
            self.sessions.close_all()
        return sorted(results, key=lambda result: (result.path, result.id, result.url))


def select_links(
    data: Mapping[str, Any], *, mode: str, base_url: str
) -> list[CatalogLink]:
    base_host = (urlsplit(base_url).hostname or "").lower()
    links: list[CatalogLink] = []
    for resource in catalog_resources(data):
        raw_url = str(resource.get("url", ""))
        absolute_url = urljoin(base_url, raw_url)
        host = (urlsplit(absolute_url).hostname or "").lower()
        is_internal = host == base_host
        if mode == "internal" and not is_internal:
            continue
        if mode == "external" and is_internal:
            continue
        links.append(
            CatalogLink(
                id=str(resource.get("id", "")),
                path=str(resource.get("path", "")),
                title=str(resource.get("title", "")),
                url=absolute_url,
            )
        )
    return links


def build_report(
    *, catalog: Path, mode: str, results: list[LinkResult]
) -> dict[str, Any]:
    statuses = ("working", "redirect", "review", "broken", "blocked", "error")
    counts = {status: sum(item.status == status for item in results) for status in statuses}
    counts["total"] = len(results)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog": str(catalog),
        "mode": mode,
        "counts": counts,
        "results": [asdict(result) for result in results],
    }


def exit_code_for_report(report: Mapping[str, Any]) -> int:
    counts = report.get("counts", {})
    if not isinstance(counts, Mapping):
        return 2
    return (
        1
        if counts.get("broken", 0)
        or counts.get("blocked", 0)
        or counts.get("error", 0)
        else 0
    )


def _positive_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("must be a finite number greater than zero")
    return parsed


def _non_negative_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise argparse.ArgumentTypeError("must be a finite number zero or greater")
    return parsed


def _workers(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= 32:
        raise argparse.ArgumentTypeError("must be between 1 and 32")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--mode", choices=("internal", "external", "all"), default="all")
    mode.add_argument("--internal", action="store_const", const="internal", dest="mode")
    mode.add_argument("--external", action="store_const", const="external", dest="mode")
    mode.add_argument("--all", action="store_const", const="all", dest="mode")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT), help="JSON path, or '-' for stdout"
    )
    parser.add_argument("--timeout", type=_positive_float, default=10.0)
    parser.add_argument("--workers", type=_workers, default=8)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--backoff", type=_non_negative_float, default=0.5)
    parser.add_argument("--min-interval", type=_non_negative_float, default=0.2)
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.retries < 0:
        print("--retries must be zero or greater", file=sys.stderr)
        return 2
    try:
        data = load_catalog(args.catalog)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    issues = validate_catalog(data)
    if issues:
        print("catalog validation failed before link checks", file=sys.stderr)
        for issue in issues:
            print(f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr)
        return 2

    links = select_links(data, mode=args.mode, base_url=args.base_url)
    checker = LinkChecker(
        timeout=args.timeout,
        workers=args.workers,
        retries=args.retries,
        backoff_factor=args.backoff,
        min_interval=args.min_interval,
    )
    results = checker.check_all(links)
    report = build_report(catalog=args.catalog, mode=args.mode, results=results)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output == "-":
        sys.stdout.write(payload)
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
        print(f"link report: {output}", file=sys.stderr)
    counts = report["counts"]
    print(
        "links: " + ", ".join(f"{key}={value}" for key, value in counts.items()),
        file=sys.stderr,
    )
    return exit_code_for_report(report)


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
