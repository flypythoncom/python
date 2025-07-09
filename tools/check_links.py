#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FlyPython 链接检查工具
用于定期检查README文件中所有外部链接的有效性
"""

import re
import requests
import time
import json
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class LinkChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
        self.results = {
            'working': [],
            'broken': [],
            'redirect': [],
            'timeout': [],
            'unknown': []
        }
    
    def extract_links_from_file(self, filename):
        """从markdown文件中提取所有外部链接"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"无法读取文件 {filename}: {e}")
            return []
        
        # 匹配markdown链接格式 [text](url)
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        # 匹配纯链接格式
        url_pattern = r'https?://[^\s\])\}]+'
        plain_links = re.findall(url_pattern, content)
        
        links = []
        
        # 处理markdown链接
        for text, url in markdown_links:
            if url.startswith('http'):
                links.append({
                    'text': text,
                    'url': url,
                    'file': filename,
                    'type': 'markdown'
                })
        
        # 处理纯链接
        for url in plain_links:
            # 避免重复
            if not any(link['url'] == url for link in links):
                links.append({
                    'text': url,
                    'url': url,
                    'file': filename,
                    'type': 'plain'
                })
        
        return links
    
    def check_link(self, link):
        """检查单个链接的状态"""
        url = link['url']
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            status_code = response.status_code
            
            if status_code == 200:
                link['status'] = 'working'
                link['status_code'] = status_code
                self.results['working'].append(link)
            elif 300 <= status_code < 400:
                link['status'] = 'redirect'
                link['status_code'] = status_code
                link['final_url'] = response.url
                self.results['redirect'].append(link)
            else:
                # 尝试GET请求，有些网站不支持HEAD
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        link['status'] = 'working'
                        link['status_code'] = response.status_code
                        self.results['working'].append(link)
                    else:
                        link['status'] = 'broken'
                        link['status_code'] = response.status_code
                        self.results['broken'].append(link)
                except:
                    link['status'] = 'broken'
                    link['status_code'] = status_code
                    self.results['broken'].append(link)
        
        except requests.exceptions.Timeout:
            link['status'] = 'timeout'
            link['error'] = 'Request timeout'
            self.results['timeout'].append(link)
        
        except requests.exceptions.RequestException as e:
            link['status'] = 'unknown'
            link['error'] = str(e)
            self.results['unknown'].append(link)
        
        return link
    
    def check_all_links(self, links, max_workers=10):
        """并发检查所有链接"""
        print(f"开始检查 {len(links)} 个链接...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_link = {executor.submit(self.check_link, link): link for link in links}
            
            for i, future in enumerate(as_completed(future_to_link), 1):
                link = future_to_link[future]
                try:
                    result = future.result()
                    status = result.get('status', 'unknown')
                    print(f"[{i}/{len(links)}] {status.upper()}: {result['url']}")
                    time.sleep(0.1)
                except Exception as e:
                    print(f"检查链接时出错 {link['url']}: {e}")
    
    def generate_report(self):
        """生成检查报告"""
        total = sum(len(links) for links in self.results.values())
        
        print("\n" + "="*60)
        print("链接检查报告")
        print("="*60)
        print(f"总链接数: {total}")
        print(f"正常链接: {len(self.results['working'])}")
        print(f"重定向链接: {len(self.results['redirect'])}")
        print(f"失效链接: {len(self.results['broken'])}")
        print(f"超时链接: {len(self.results['timeout'])}")
        print(f"未知状态: {len(self.results['unknown'])}")
        
        # 保存详细结果
        os.makedirs('../reports', exist_ok=True)
        with open('../reports/link_check_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细结果已保存到: reports/link_check_results.json")

def main():
    checker = LinkChecker()
    
    # 从README文件提取链接 (相对于项目根目录)
    files_to_check = ['../README.md', '../README_cn.md']
    all_links = []
    
    for filename in files_to_check:
        print(f"从 {filename} 提取链接...")
        links = checker.extract_links_from_file(filename)
        all_links.extend(links)
        print(f"找到 {len(links)} 个链接")
    
    if not all_links:
        print("没有找到任何链接!")
        return
    
    # 去重
    unique_links = []
    seen_urls = set()
    for link in all_links:
        if link['url'] not in seen_urls:
            unique_links.append(link)
            seen_urls.add(link['url'])
    
    print(f"去重后共 {len(unique_links)} 个唯一链接")
    
    # 检查链接
    checker.check_all_links(unique_links)
    
    # 生成报告
    checker.generate_report()

if __name__ == '__main__':
    main() 