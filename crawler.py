# crawler.py
"""
네이버 스토어 리뷰 크롤러 (업데이트 버전)
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless=True):
    """크롬 드라이버 생성"""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait


def crawl_reviews(url, max_pages=5, output_file="reviews.csv"):
    """리뷰 크롤링 함수"""
    driver, wait = create_driver(headless=True)
    driver.get(url)
    time.sleep(2)

    review_list = []

    for page in range(1, max_pages + 1):
        print(f"\n--- {page} 페이지 ---")
        try:
            review_blocks = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#REVIEW div.HakaEZ240l"))
            )
            for block in review_blocks:
                # 리뷰 내용
                try:
                    review_text = block.find_element(By.CSS_SELECTOR, "span.MX91DFZo2F").text.strip()
                except:
                    review_text = None

                # 날짜
                try:
                    parent = block.find_element(By.XPATH, "./ancestor::div[contains(@class,'O2M37e85_1')]")
                    date_text = parent.find_element(By.CSS_SELECTOR, "div.Db9Dtnf7gY span.MX91DFZo2F").text.strip()
                except:
                    date_text = None

                if review_text:
                    review_list.append({"review": review_text, "date": date_text})

            print(f"✅ {len(review_blocks)}개 리뷰 수집 완료")

        except Exception as e:
            print(f"❌ {page} 페이지 수집 실패:", e)
            break

        # 다음 페이지 버튼 클릭
        try:
            next_btn = driver.find_element(By.XPATH, f"//a[contains(@class,'hyY6CXtbcn') and text()='{page+1}']")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(1.5)
        except:
            print("⚠️ 다음 페이지 없음 → 종료")
            break

    driver.quit()

    # CSV 저장
    df = pd.DataFrame(review_list)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n총 {len(df)}개 리뷰 저장 완료 → {output_file}")

    return df


if __name__ == "__main__":
    URL = "https://brand.naver.com/popmart/products/10643619141"
    crawl_reviews(URL, max_pages=20, output_file="naver_store_reviews.csv")
