# trend_analysis.py
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. 날짜 전처리 함수
# -----------------------------
def preprocess_date(df, date_col='date', date_format="%y.%m.%d."):
    """
    문자열 날짜를 datetime으로 변환하고 결측치 제거
    """
    df = df.copy()
    df[date_col] = df[date_col].astype(str).str.strip()
    df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors='coerce')
    df = df.dropna(subset=[date_col])
    return df

# -----------------------------
# 2. 일별 리뷰 추세 시각화
# -----------------------------
def plot_daily_trend(df, date_col='date', figsize=(12,6)):
    daily_counts = df.groupby(df[date_col]).size()
    plt.figure(figsize=figsize)
    plt.plot(daily_counts.index, daily_counts.values, marker='o')
    plt.title("일별 리뷰 개수 추세")
    plt.xlabel("날짜")
    plt.ylabel("리뷰 개수")
    plt.grid(True)
    plt.show()

# -----------------------------
# 3. 주간 & 월간 리뷰 추세 시각화
# -----------------------------
def plot_weekly_monthly_trend(df, date_col='date', figsize=(12,6)):
    weekly_counts = df.groupby(pd.Grouper(key=date_col, freq='W')).size()
    monthly_counts = df.groupby(pd.Grouper(key=date_col, freq='M')).size()

    plt.figure(figsize=figsize)
    plt.plot(weekly_counts.index, weekly_counts.values, marker='o', label="주간 리뷰")
    plt.plot(monthly_counts.index, monthly_counts.values, marker='s', label="월간 리뷰")
    plt.title("주간 & 월간 리뷰 추세")
    plt.xlabel("날짜")
    plt.ylabel("리뷰 개수")
    plt.legend()
    plt.grid(True)
    plt.show()
