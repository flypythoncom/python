from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest
import requests
import tools.check_links as check_links

from tools.check_links import (
    CatalogLink,
    LinkChecker,
    LinkResult,
    PinnedDNSHTTPAdapter,
    SafeTargetGuard,
    ThreadLocalSessions,
    UnsafeTarget,
    build_report,
    build_session,
    classify_status,
    exit_code_for_report,
    select_links,
)


PUBLIC_IP = "93.184.216.34"


class FakeResponse:
    def __init__(self, status_code, url="https://example.com/", history=None, headers=None):
        self.status_code = status_code
        self.url = url
        self.history = history or []
        self.headers = headers or {}
        self.closed = False

    def close(self):
        self.closed = True


class FakeSession:
    def __init__(self, head, get=None):
        self.head_response = head
        self.get_response = get
        self.calls = []
        self.closed = False

    def head(self, url, **kwargs):
        self.calls.append(("HEAD", url, kwargs))
        return self.head_response

    def get(self, url, **kwargs):
        self.calls.append(("GET", url, kwargs))
        return self.get_response

    def close(self):
        self.closed = True


def guard_for(address=PUBLIC_IP):
    return SafeTargetGuard(lambda _host, _port: [address])


def link():
    return CatalogLink("docs", "foundations", "Docs", "https://example.com/docs")


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (200, "working"),
        (301, "redirect"),
        (403, "review"),
        (408, "review"),
        (425, "review"),
        (429, "review"),
        (503, "review"),
        (404, "broken"),
    ],
)
def test_status_classification(status_code, expected) -> None:
    assert classify_status(status_code, redirected=False) == expected


def test_redirect_history_is_preserved() -> None:
    hop = FakeResponse(301, "https://example.com/old", headers={"Location": "/docs"})
    response = FakeResponse(200, "https://example.com/docs")

    class RedirectSession(FakeSession):
        def __init__(self):
            super().__init__(hop)
            self.responses = iter([hop, response])

        def head(self, url, **kwargs):
            self.calls.append(("HEAD", url, kwargs))
            return next(self.responses)

    session = RedirectSession()
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )
    redirect_link = CatalogLink(
        "docs", "foundations", "Docs", "https://example.com/old"
    )
    result = checker.check_one(redirect_link)
    assert result.status == "redirect"
    assert result.history == [
        {"status_code": 301, "url": "https://example.com/old", "location": "/docs"}
    ]
    assert hop.closed is True


def test_head_failure_falls_back_to_streaming_get_and_confirms_404() -> None:
    session = FakeSession(FakeResponse(404), FakeResponse(404))
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )
    result = checker.check_one(link())
    assert result.status == "broken"
    assert result.method == "GET"
    assert session.calls[1][2]["stream"] is True


def test_head_redirect_without_location_falls_back_to_get() -> None:
    head = FakeResponse(301)
    response = FakeResponse(200)
    session = FakeSession(head, response)
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )

    result = checker.check_one(link())

    assert result.status == "working"
    assert result.method == "GET"
    assert head.closed is True
    assert response.closed is True


def test_get_redirect_without_location_is_fatal() -> None:
    head = FakeResponse(301)
    response = FakeResponse(301)
    session = FakeSession(head, response)
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )

    result = checker.check_one(link())

    assert result.status == "error"
    assert "no Location" in (result.error or "")
    assert head.closed is True
    assert response.closed is True


def test_unsupported_redirect_status_is_fatal() -> None:
    response = FakeResponse(304)
    session = FakeSession(response)
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )

    result = checker.check_one(link())

    assert result.status == "error"
    assert "unsupported redirect status 304" in (result.error or "")
    assert response.closed is True


@pytest.mark.parametrize("status_code", [403, 408, 425, 429, 500, 503])
def test_transient_and_access_denied_statuses_need_review(status_code) -> None:
    head = FakeResponse(status_code)
    session = FakeSession(head, FakeResponse(status_code))
    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: session,
        workers=1,
        retries=0,
        min_interval=0,
    )
    assert checker.check_one(link()).status == "review"
    assert len(session.calls) == 1
    assert head.closed is True


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/admin",
        "http://127.0.0.1/",
        "http://169.254.169.254/latest/meta-data/",
        "http://100.100.100.200/latest/meta-data/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "https://168.63.129.16/",
        "https://224.0.0.1/",
        "https://[64:ff9b::7f00:1]/",
        "https://[::ffff:93.184.216.34]/",
    ],
)
def test_literal_local_and_metadata_targets_are_blocked(url) -> None:
    with pytest.raises(UnsafeTarget):
        SafeTargetGuard().resolve_url(url)


def test_dns_resolution_to_private_ip_is_blocked() -> None:
    with pytest.raises(UnsafeTarget, match="non-public"):
        guard_for("10.0.0.8").resolve_url("https://example.com/")


def test_adapter_pins_public_ip_and_preserves_tls_hostname() -> None:
    adapter = PinnedDNSHTTPAdapter(guard_for(), max_retries=0)
    captured = {}

    class PoolManager:
        def connection_from_host(self, **kwargs):
            captured.update(kwargs)
            return "pool"

    adapter.poolmanager = PoolManager()
    request = requests.Request("GET", "https://example.com/path").prepare()
    assert adapter.get_connection_with_tls_context(request, True) == "pool"
    assert captured["host"] == PUBLIC_IP
    assert captured["pool_kwargs"]["server_hostname"] == "example.com"
    assert captured["pool_kwargs"]["assert_hostname"] == "example.com"
    assert request.headers["Host"] == "example.com"


def test_adapter_revalidates_and_blocks_an_unsafe_redirect_hop() -> None:
    resolved_hosts = []

    def resolver(host, _port):
        resolved_hosts.append(host)
        return [PUBLIC_IP if host == "example.com" else "127.0.0.1"]

    adapter = PinnedDNSHTTPAdapter(SafeTargetGuard(resolver), max_retries=0)

    class PoolManager:
        def connection_from_host(self, **_kwargs):
            return "pool"

    adapter.poolmanager = PoolManager()
    first = requests.Request("GET", "https://example.com/start").prepare()
    redirect = requests.Request("GET", "https://internal.example/admin").prepare()

    assert adapter.get_connection_with_tls_context(first, True) == "pool"
    with pytest.raises(UnsafeTarget, match="non-public"):
        adapter.get_connection_with_tls_context(redirect, True)
    assert resolved_hosts == ["example.com", "internal.example"]


def test_checker_blocks_https_redirect_downgrade() -> None:
    hop = FakeResponse(
        302,
        "https://example.com/start",
        headers={"Location": "http://example.com/docs"},
    )
    session = FakeSession(hop)
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )

    result = checker.check_one(link())

    assert result.status == "blocked"
    assert "may not downgrade" in (result.error or "")
    assert hop.closed is True


def test_thread_local_sessions_are_not_shared_between_workers() -> None:
    created = []
    barrier = threading.Barrier(2)

    def factory():
        value = object()
        created.append(value)
        return value

    sessions = ThreadLocalSessions(factory)
    results = []

    def worker():
        first = sessions.get()
        barrier.wait()
        results.append((first, sessions.get()))

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(created) == 2
    assert results[0][0] is results[0][1]
    assert results[1][0] is results[1][1]
    assert results[0][0] is not results[1][0]


def test_check_all_closes_worker_sessions() -> None:
    sessions = []

    def factory():
        session = FakeSession(FakeResponse(200))
        sessions.append(session)
        return session

    checker = LinkChecker(
        guard=guard_for(), session_factory=factory, workers=1, min_interval=0
    )
    assert len(checker.check_all([link()])) == 1
    assert len(sessions) == 1
    assert sessions[0].closed is True


def test_mode_selects_internal_external_or_all() -> None:
    data = {
        "resources": [
            {"id": "internal", "path": "foundations", "title": "I", "url": "/guide/"},
            {
                "id": "external",
                "path": "foundations",
                "title": "E",
                "url": "https://docs.python.org/3/",
            },
        ]
    }
    internal = select_links(data, mode="internal", base_url="https://python.flypython.com/")
    external = select_links(data, mode="external", base_url="https://python.flypython.com/")
    all_links = select_links(data, mode="all", base_url="https://python.flypython.com/")
    assert [item.id for item in internal] == ["internal"]
    assert [item.id for item in external] == ["external"]
    assert len(all_links) == 2


def test_exit_code_only_fails_broken_or_blocked_links() -> None:
    review_report = {"counts": {"review": 2, "broken": 0, "blocked": 0}}
    assert exit_code_for_report(review_report) == 0
    assert exit_code_for_report({"counts": {"broken": 1, "blocked": 0}}) == 1
    assert exit_code_for_report({"counts": {"broken": 0, "blocked": 1}}) == 1
    assert exit_code_for_report({"counts": {"error": 1}}) == 1


def test_unexpected_checker_error_is_fatal() -> None:
    class BrokenSession(FakeSession):
        def head(self, url, **kwargs):
            raise RuntimeError("programming defect")

    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: BrokenSession(FakeResponse(200)),
        workers=1,
        retries=0,
        min_interval=0,
    )
    result = checker.check_one(link())
    assert result.status == "error"
    assert "programming defect" in (result.error or "")


@pytest.mark.parametrize(
    "exception",
    [
        requests.exceptions.ConnectionError("connection failed"),
        requests.exceptions.SSLError("certificate failed"),
        requests.exceptions.TooManyRedirects("redirect loop"),
        requests.exceptions.InvalidURL("invalid redirect"),
    ],
)
def test_terminal_request_failures_are_fatal(exception) -> None:
    class BrokenSession(FakeSession):
        def head(self, url, **kwargs):
            raise exception

    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: BrokenSession(FakeResponse(200)),
        workers=1,
        retries=0,
        min_interval=0,
    )

    assert checker.check_one(link()).status == "error"


def test_timeout_remains_review_needed() -> None:
    class SlowSession(FakeSession):
        def head(self, url, **kwargs):
            raise requests.Timeout("timed out")

    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: SlowSession(FakeResponse(200)),
        workers=1,
        retries=0,
        min_interval=0,
    )

    assert checker.check_one(link()).status == "review"


def test_adapter_transport_and_status_retries_are_disabled() -> None:
    session = build_session(guard_for())
    try:
        retry = session.get_adapter("https://").max_retries
        assert retry.respect_retry_after_header is False
        assert retry.backoff_max == 5.0
        assert retry.total == 0
        assert retry.connect == 0
        assert retry.read == 0
        assert retry.status == 0
        assert not retry.status_forcelist
    finally:
        session.close()


def test_status_retry_is_manual_and_closes_each_response() -> None:
    first = FakeResponse(503)
    second = FakeResponse(200)

    class RetrySession(FakeSession):
        def __init__(self):
            super().__init__(first)
            self.responses = iter([first, second])

        def head(self, url, **kwargs):
            self.calls.append(("HEAD", url, kwargs))
            return next(self.responses)

    session = RetrySession()
    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: session,
        workers=1,
        retries=1,
        backoff_factor=0,
        min_interval=0,
    )

    result = checker.check_one(link())

    assert result.status == "working"
    assert len(session.calls) == 2
    assert first.closed is True
    assert second.closed is True


@pytest.mark.parametrize("retry_after", ["60", "9" * 400])
def test_large_retry_after_stops_without_get_fallback(
    monkeypatch, retry_after: str
) -> None:
    response = FakeResponse(429, headers={"Retry-After": retry_after})
    session = FakeSession(response)
    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: session,
        workers=1,
        retries=2,
        min_interval=0,
    )
    sleeps = []
    monkeypatch.setattr(check_links.time, "sleep", sleeps.append)

    result = checker.check_one(link())

    assert result.status == "review"
    assert len(session.calls) == 1
    assert sleeps == []
    assert response.closed is True


def test_bounded_retry_after_is_honored(monkeypatch) -> None:
    first = FakeResponse(429, headers={"Retry-After": "2"})
    second = FakeResponse(200)

    class RetrySession(FakeSession):
        def __init__(self):
            super().__init__(first)
            self.responses = iter([first, second])

        def head(self, url, **kwargs):
            self.calls.append(("HEAD", url, kwargs))
            return next(self.responses)

    session = RetrySession()
    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: session,
        workers=1,
        retries=1,
        min_interval=0,
    )
    sleeps = []
    monkeypatch.setattr(check_links.time, "sleep", sleeps.append)

    result = checker.check_one(link())

    assert result.status == "working"
    assert len(session.calls) == 2
    assert sleeps == [2.0]


def test_transport_timeout_retry_is_manual() -> None:
    response = FakeResponse(200)

    class FlakySession(FakeSession):
        def __init__(self):
            super().__init__(response)
            self.attempt = 0

        def head(self, url, **kwargs):
            self.calls.append(("HEAD", url, kwargs))
            self.attempt += 1
            if self.attempt == 1:
                raise requests.Timeout("timed out")
            return response

    session = FlakySession()
    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: session,
        workers=1,
        retries=1,
        backoff_factor=0,
        min_interval=0,
    )

    result = checker.check_one(link())

    assert result.status == "working"
    assert len(session.calls) == 2


def test_wrapped_timeout_remains_review_needed() -> None:
    class WrappedTimeoutSession(FakeSession):
        def head(self, url, **kwargs):
            raise requests.ConnectionError(TimeoutError("timed out"))

    checker = LinkChecker(
        guard=guard_for(),
        session_factory=lambda: WrappedTimeoutSession(FakeResponse(200)),
        workers=1,
        retries=0,
        min_interval=0,
    )

    assert checker.check_one(link()).status == "review"


def test_responses_close_when_result_processing_fails(monkeypatch) -> None:
    head = FakeResponse(404)
    response = FakeResponse(200)
    session = FakeSession(head, response)
    checker = LinkChecker(
        guard=guard_for(), session_factory=lambda: session, workers=1, min_interval=0
    )

    def fail_classification(_status_code, *, redirected):
        raise RuntimeError("cannot process response")

    monkeypatch.setattr(check_links, "classify_status", fail_classification)
    result = checker.check_one(link())

    assert result.status == "error"
    assert head.closed is True
    assert response.closed is True


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("--timeout", "nan"),
        ("--timeout", "inf"),
        ("--backoff", "nan"),
        ("--min-interval", "inf"),
    ],
)
def test_cli_rejects_non_finite_float_arguments(option: str, value: str) -> None:
    with pytest.raises(SystemExit, match="2"):
        check_links.build_parser().parse_args([option, value])


@pytest.mark.parametrize(
    ("status", "status_code", "expected_exit"),
    [
        ("review", 408, 0),
        ("broken", 404, 1),
        ("blocked", None, 1),
        ("error", None, 1),
    ],
)
def test_cli_writes_json_and_uses_report_exit_code(
    monkeypatch,
    tmp_path: Path,
    valid_catalog: dict,
    status: str,
    status_code: int | None,
    expected_exit: int,
) -> None:
    monkeypatch.setattr(check_links, "load_catalog", lambda _path: valid_catalog)
    monkeypatch.setattr(check_links, "validate_catalog", lambda _data: [])
    result = LinkResult(
        "docs",
        "foundations",
        "Docs",
        "https://example.com/docs",
        status,
        status_code=status_code,
        method="GET" if status_code is not None else None,
    )
    monkeypatch.setattr(
        check_links.LinkChecker, "check_all", lambda _self, _links: [result]
    )
    output = tmp_path / f"{status}.json"

    exit_code = check_links.run(
        ["--catalog", "ignored.yml", "--output", str(output), "--min-interval", "0"]
    )

    assert exit_code == expected_exit
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["counts"][status] == 1
    assert report["results"][0]["status_code"] == status_code
