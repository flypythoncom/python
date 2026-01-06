#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FlyPython Link Checker Tool
Periodically checks the validity of all external links in README files
"""

import re
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class LinkChecker:
    def __init__(self, timeout: int = 10, max_workers: int = 10):
        self.session = self._create_session()
        self.timeout = timeout
        self.max_workers = max_workers
        self.results = {
            'working': [],
            'broken': [],
            'redirect': [],
            'timeout': [],
            'unknown': []
        }
        self.processed_urls = set()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy and headers"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Set user agent
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return session

    def extract_links_from_file(self, filename: str) -> List[Dict]:
        """Extract all external links from a markdown file"""
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"File not found: {filename}")
            return []
        
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            return []
        
        links = []
        
        # Extract markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        for text, url in markdown_links:
            if url.startswith('http'):
                links.append({
                    'text': text,
                    'url': url,
                    'file': str(filepath),
                    'type': 'markdown'
                })
        
        # Extract plain URLs
        plain_urls = re.findall(r'https?://[^\s\])\}]+', content)
        seen = {link['url'] for link in links}
        
        for url in plain_urls:
            if url not in seen:
                links.append({
                    'text': url,
                    'url': url,
                    'file': str(filepath),
                    'type': 'plain'
                })
                seen.add(url)
        
        return links

    def check_link(self, link: Dict) -> Dict:
        """Check the status of a single link"""
        url = link['url']
        
        if url in self.processed_urls:
            return link
        
        self.processed_urls.add(url)
        
        try:
            # Try HEAD request first (faster)
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            return self._process_response(link, response)
        
        except requests.exceptions.Timeout:
            link['status'] = 'timeout'
            link['error'] = 'Request timeout'
            self.results['timeout'].append(link)
            return link
        
        except requests.exceptions.RequestException as e:
            # Fall back to GET request for servers that don't support HEAD
            try:
                response = self.session.get(url, timeout=self.timeout)
                return self._process_response(link, response)
            except requests.exceptions.RequestException:
                link['status'] = 'unknown'
                link['error'] = str(e)
                self.results['unknown'].append(link)
                return link

    def _process_response(self, link: Dict, response: requests.Response) -> Dict:
        """Process HTTP response and categorize link"""
        status_code = response.status_code
        
        if status_code == 200:
            link['status'] = 'working'
            self.results['working'].append(link)
        elif 300 <= status_code < 400:
            link['status'] = 'redirect'
            link['final_url'] = response.url
            self.results['redirect'].append(link)
        else:
            link['status'] = 'broken'
            self.results['broken'].append(link)
        
        link['status_code'] = status_code
        return link

    def check_all_links(self, links: List[Dict]) -> None:
        """Concurrently check all links"""
        print(f"Checking {len(links)} links...\n")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.check_link, link): link for link in links}
            
            for i, future in enumerate(as_completed(futures), 1):
                link = futures[future]
                try:
                    result = future.result()
                    status = result.get('status', 'unknown').upper()
                    print(f"[{i}/{len(links)}] {status}: {result['url']}")
                except Exception as e:
                    print(f"Error checking {link['url']}: {e}")

    def generate_report(self, output_dir: str = 'reports') -> None:
        """Generate and save detailed report"""
        total = sum(len(links) for links in self.results.values())
        
        report = f"""
{'='*60}
Link Check Report
{'='*60}
Total Links: {total}
✓ Working: {len(self.results['working'])}
→ Redirects: {len(self.results['redirect'])}
✗ Broken: {len(self.results['broken'])}
⏱ Timeouts: {len(self.results['timeout'])}
? Unknown: {len(self.results['unknown'])}
{'='*60}
"""
        print(report)
        
        # Save detailed results
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results_file = output_path / 'link_check_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"Detailed results saved to: {results_file}")

    def deduplicate_links(self, links: List[Dict]) -> List[Dict]:
        """Remove duplicate links by URL"""
        seen = set()
        unique = []
        for link in links:
            if link['url'] not in seen:
                unique.append(link)
                seen.add(link['url'])
        return unique


def main():
    files = ['../README.md', '../README_cn.md']
    
    # Extract links
    checker = LinkChecker(timeout=10, max_workers=10)
    all_links = []
    
    for filename in files:
        print(f"Extracting links from {filename}...")
        links = checker.extract_links_from_file(filename)
        if links:
            all_links.extend(links)
            print(f"Found {len(links)} links\n")
    
    if not all_links:
        print("No links found!")
        return
    
    # Deduplicate and check
    unique_links = checker.deduplicate_links(all_links)
    print(f"Checking {len(unique_links)} unique links\n")
    
    checker.check_all_links(unique_links)
    checker.generate_report()


if __name__ == '__main__':
    main()
