# -*- coding: utf-8 -*-
"""
简历数据采集器 - 使用 Selenium + Chrome
用于从公开平台采集候选人信息
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class RecruitmentScraper:
    def __init__(self, headless: bool = False, proxy: Optional[str] = None):
        self.headless = headless
        self.proxy = proxy
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
        
        if self.headless:
            options.add_argument('--headless=new')
        
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
    
    def random_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))
    
    def scroll_page(self, scrolls=3):
        for i in range(scrolls):
            self.driver.execute_script(f"window.scrollTo(0, {i * 500});")
            self.random_delay(0.5, 1)
    
    def search_github(self, keywords, max_results=20):
        print(f"\n[SEARCH] 正在搜索 GitHub: {keywords}")
        
        search_url = f"https://github.com/search?q={keywords}&type=users"
        self.driver.get(search_url)
        
        self.random_delay(3, 5)
        self.scroll_page(2)
        
        candidates = []
        
        try:
            time.sleep(3)
            
            selectors = ["ul.user-list li", "div.user-list-item", ".user-list li"]
            user_items = []
            
            for selector in selectors:
                try:
                    user_items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if user_items:
                        print(f"[INFO] 使用选择器: {selector}, 找到 {len(user_items)} 个用户")
                        break
                except:
                    continue
            
            if not user_items:
                print(f"[WARN] 未找到用户列表")
                print(f"  页面标题: {self.driver.title}")
                print(f"  当前URL: {self.driver.current_url}")
                return []
            
            print(f"[INFO] 找到 {len(user_items)} 个用户")
            
            for idx, user_item in enumerate(user_items[:max_results]):
                try:
                    user_data = self._extract_user(user_item)
                    if user_data:
                        candidates.append(user_data)
                        name = user_data.get('name', 'N/A') or user_data.get('username', 'N/A')
                        print(f"  [{idx+1}] {name}")
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"[ERROR] 搜索失败: {e}")
        
        self.results = candidates
        return candidates
    
    def _extract_user(self, user_element):
        try:
            username, profile_url = "", ""
            
            try:
                elem = user_element.find_element(By.CSS_SELECTOR, "a[data-hovercard-type='user']")
                username = elem.text.strip()
                profile_url = elem.get_attribute("href")
            except:
                pass
            
            if not username:
                links = user_element.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href") or ""
                    if "github.com" in href and href.count('/') == 3:
                        username = link.text.strip()
                        profile_url = href
                        break
            
            try:
                name = user_element.find_element(By.CSS_SELECTOR, "span.full-name").text.strip()
            except:
                try:
                    name = user_element.find_element(By.CSS_SELECTOR, "div.f4").text.strip()
                except:
                    name = username
            
            bio = ""
            try:
                bio = user_element.find_element(By.CSS_SELECTOR, "p.bio").text.strip()
            except:
                pass
            
            location = ""
            try:
                location = user_element.find_element(By.CSS_SELECTOR, "span.location").text.strip()
            except:
                pass
            
            if not username:
                return None
            
            return {
                "username": username,
                "name": name,
                "bio": bio,
                "location": location,
                "profile_url": profile_url,
                "source": "GitHub",
                "collected_at": datetime.now().isoformat()
            }
        except:
            return None
    
    def save_results(self, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"candidates_{timestamp}.json"
        
        output_dir = r"C:\Users\ranwu\XiaomiCloud\UAS-AIOS\examples\output"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n[SAVE] 结果已保存到: {filepath}")
        print(f"[INFO] 共采集 {len(self.results)} 条记录")
        return filepath
    
    def close(self):
        if self.driver:
            self.driver.quit()
            print("[DONE] 浏览器已关闭")


def main():
    print("=" * 60)
    print("[Recruitment] 招聘简历数据采集器")
    print("    Selenium + Chrome 方案验证")
    print("=" * 60)
    
    scraper = RecruitmentScraper(headless=False)
    
    try:
        if not scraper.setup_driver():
            return
        
        print("\n开始采集候选人数据...")
        
        print("\n[TASK 1] 搜索 GitHub Python 工程师")
        github_candidates = scraper.search_github(
            keywords="python backend engineer",
            max_results=10
        )
        
        scraper.random_delay(3, 5)
        
        if github_candidates:
            scraper.save_results("github_candidates.json")
        
        print("\n" + "=" * 60)
        print(f"[DONE] 采集完成! 共采集: {len(github_candidates)} 条")
        print("=" * 60)
        
        if github_candidates:
            print("\n[PREVIEW] 部分采集结果:")
            for i, c in enumerate(github_candidates[:5]):
                print(f"\n--- 候选人 {i+1} ---")
                print(f"  用户名: {c.get('username')}")
                print(f"  姓名: {c.get('name')}")
                bio = c.get('bio', '')[:50] if c.get('bio') else 'N/A'
                print(f"  简介: {bio}")
                print(f"  位置: {c.get('location')}")
        else:
            print("\n[WARN] 未采集到数据")
        
    except KeyboardInterrupt:
        print("\n\n[WARN] 用户中断")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.close()


if __name__ == "__main__":
    main()