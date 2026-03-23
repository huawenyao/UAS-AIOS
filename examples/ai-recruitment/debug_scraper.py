# -*- coding: utf-8 -*-
"""
简历数据采集器 - 调试版
"""

import json
import time
import random
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class RecruitmentScraper:
    def __init__(self, headless: bool = False):
        self.driver = None
        self.results = []
        
    def setup_driver(self):
        print("[SETUP] 正在配置 Chrome 浏览器...")
        
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--lang=zh-CN')
        options.add_argument('--window-size=1920,1080')
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        options.add_argument(f'--user-agent={user_agent}')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("[OK] 浏览器配置完成！")
            return True
            
        except Exception as e:
            print(f"[ERROR] 浏览器配置失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def search_and_debug(self, keywords):
        print(f"\n[DEBUG] 搜索: {keywords}")
        
        search_url = f"https://github.com/search?q={keywords}&type=users"
        self.driver.get(search_url)
        
        time.sleep(5)
        
        print(f"  页面标题: {self.driver.title}")
        print(f"  当前URL: {self.driver.current_url}")
        
        # 获取页面源码
        page_source = self.driver.page_source[:2000]
        print(f"\n--- 页面源码 (前2000字符) ---")
        print(page_source)
        print("\n--- 结束 ---\n")
        
        # 尝试查找常见元素
        print("[DEBUG] 尝试查找元素...")
        
        # 尝试所有可能的选择器
        test_selectors = [
            "ul.user-list",
            "div.user-list",
            ".user-list",
            "ul[data-testid='user-list']",
            "div[data-testid='user-list']",
            "li[data-testid='user-list-item']",
            ".flex-1",
            "div.Box-sc",
            "article",
            "div.row",
            "div.col-12"
        ]
        
        for sel in test_selectors:
            try:
                elems = self.driver.find_elements(By.CSS_SELECTOR, sel)
                if elems:
                    print(f"  [{sel}] -> 找到 {len(elems)} 个元素")
            except:
                pass
        
        # 尝试查找所有链接
        print("\n[DEBUG] 查找用户链接...")
        links = self.driver.find_elements(By.TAG_NAME, "a")
        github_links = []
        for link in links[:30]:
            try:
                href = link.get_attribute("href") or ""
                text = link.text.strip()
                if "github.com" in href and text and "/" in href:
                    github_links.append(f"{text}: {href}")
            except:
                pass
        
        print(f"  找到 {len(github_links)} 个 GitHub 相关链接:")
        for link in github_links[:15]:
            print(f"    {link}")
    
    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    print("=" * 60)
    print("[Recruitment] 调试模式 - 分析 GitHub 页面结构")
    print("=" * 60)
    
    scraper = RecruitmentScraper(headless=False)
    
    try:
        if not scraper.setup_driver():
            return
        
        scraper.search_and_debug("python engineer")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.close()


if __name__ == "__main__":
    main()