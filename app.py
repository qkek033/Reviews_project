# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from crawler import crawl_reviews
from preprocess import preprocess_reviews
from sentiment_analysis import analyze_reviews
from visualization import set_korean_font, plot_sentiment_distribution, plot_wordcloud
from trend_analysis import preprocess_date, plot_daily_trend, plot_weekly_monthly_trend

# ====================
# Streamlit 메인 앱
# ====================
def main():
    st.set_page_config(page_title="리뷰 분석 앱", layout="wide")
    st.title("📝 네이버 리뷰 크롤링 & 감성분석 & 시각화")

    # 한글 폰트 설정
    set_korean_font()

    # -----------------------------
    # Step 1: 리뷰 수집
    # -----------------------------
    with st.expander("📌 Step 1: 리뷰 수집"):
        url = st.text_input("리뷰 페이지 URL 입력")
        pages = st.slider("수집할 페이지 수", 1, 20, 5)
        if st.button("리뷰 수집 시작"):
            with st.spinner("리뷰 수집 중..."):
                raw_df = crawl_reviews(url, max_pages=pages)
                st.success(f"✅ 총 {len(raw_df)}개 리뷰 수집 완료!")
                st.dataframe(raw_df.head())

    # -----------------------------
    # Step 2: 전처리
    # -----------------------------
    with st.expander("🧹 Step 2: 리뷰 전처리"):
        try:
            df_clean = preprocess_reviews(raw_df.to_dict(orient='records'))
            st.success(f"✅ 전처리 완료! 유효 리뷰 개수: {len(df_clean)}")
            st.dataframe(df_clean.head())
        except:
            st.warning("⚠️ 먼저 리뷰를 수집해주세요.")

    # -----------------------------
    # Step 3: 감성분석
    # -----------------------------
    with st.expander("🔍 Step 3: 감성분석"):
        try:
            df_sentiment = analyze_reviews(df_clean)
            st.success("✅ 감성분석 완료")
            st.dataframe(df_sentiment[['review','sentiment']].head())
        except:
            st.warning("⚠️ 전처리된 리뷰가 필요합니다.")

    # -----------------------------
    # Step 4: 감성분석 시각화
    # -----------------------------
    with st.expander("📊 Step 4: 감성 시각화"):
        try:
            sentiment_counts = df_sentiment['sentiment'].value_counts()
            plot_sentiment_distribution(df_sentiment)
            plot_wordcloud(df_sentiment, sentiment='긍정')
            plot_wordcloud(df_sentiment, sentiment='부정', background_color='black', colormap='Reds')
        except:
            st.warning("⚠️ 감성분석 결과가 필요합니다.")

    # -----------------------------
    # Step 5: 시계열/추세 분석
    # -----------------------------
    with st.expander("📈 Step 5: 리뷰 추세 분석"):
        try:
            df_sentiment = preprocess_date(df_sentiment, date_col='date')
            plot_daily_trend(df_sentiment)
            plot_weekly_monthly_trend(df_sentiment)
        except:
            st.warning("⚠️ 날짜 정보가 필요합니다.")

if __name__ == "__main__":
    main()
