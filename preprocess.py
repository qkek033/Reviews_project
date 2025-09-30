# preprocess.py
"""
네이버 리뷰 텍스트 전처리 모듈
"""

import re
import pandas as pd


def clean_review(text):
    """리뷰 텍스트 전처리"""
    if not isinstance(text, str):
        return ""  # 안전장치

    # 1. 이모지 제거 (한글/영문/숫자/기본 문장부호만 허용)
    text = re.sub(r'[^\w\s.,!?ㄱ-ㅎㅏ-ㅣ가-힣]', '', text)

    # 2. 특수문자 제거 (일부 문장부호는 남김)
    text = re.sub(r'[_~^·•☆★▶️✔️❤]+', '', text)

    # 3. 반복 자음/모음 줄이기 (ㅋㅋㅋㅋ → ㅋㅋ)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # 4. 줄바꿈 제거
    text = text.replace("\n", " ")

    # 5. 너무 짧은 리뷰 제거
    if len(text.strip()) < 5:
        return None

    # 6. '더보기' 같은 불필요 단어 제거
    if text.strip() == "더보기":
        return None

    return text.strip()


def preprocess_reviews(review_list, output_file="naver_reviews_cleaned.csv"):
    """
    리뷰 리스트 전처리 후 CSV 저장
    review_list: [{"review": "...", "date": "2025.09.30"}, ...]
    """
    cleaned_reviews = []
    for review in review_list:
        raw_text = review.get("review", "")
        cleaned = clean_review(raw_text)
        if cleaned:
            cleaned_reviews.append({
                "date": review.get("date", ""),
                "review": cleaned
            })

    # CSV 저장
    df = pd.DataFrame(cleaned_reviews)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ 전처리 완료! 유효한 리뷰 개수: {len(cleaned_reviews)}")
    print(f"📁 저장 파일: {output_file}")

    return df


if __name__ == "__main__":
    # 예시 실행 (테스트할 대만 쓰는 코드, 단독 실행했을 때만 동작)
    sample_reviews = [
        {"date": "2025.09.30", "review": "너무 귀여워요 ㅋㅋㅋㅋ😍😍"},
        {"date": "2025.09.29", "review": "더보기"},
        {"date": "2025.09.28", "review": "좋아요! 👍👍"},
    ]

    preprocess_reviews(sample_reviews, output_file="naver_reviews_cleaned.csv")
