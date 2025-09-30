# visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# -----------------------------
# 1. 한글 폰트 설정 함수
# -----------------------------
def set_korean_font(font_path="C:/Windows/Fonts/malgun.ttf"):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 2. 감성 분포 막대/파이차트
# -----------------------------
def plot_sentiment_distribution(df, sentiment_col='sentiment'):
    sentiment_counts = df[sentiment_col].value_counts()

    # 막대그래프
    plt.figure(figsize=(6, 4))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='pastel')
    plt.title("리뷰 감성 분포")
    plt.xlabel("감성")
    plt.ylabel("리뷰 수")
    plt.show()

    # 파이차트
    plt.figure(figsize=(5, 5))
    plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%.1f%%', startangle=90,
            colors=['skyblue', 'lightcoral'])
    plt.title("감성 분석 비율")
    plt.axis('equal')
    plt.show()

# -----------------------------
# 3. 워드클라우드 생성
# -----------------------------
def plot_wordcloud(df, sentiment='긍정', review_col='review', font_path="C:/Windows/Fonts/malgun.ttf",
                   background_color='white', colormap=None, figsize=(10, 5), title=None):
    """
    sentiment: '긍정' 또는 '부정'
    colormap: 색상맵, None이면 기본
    """
    text = ' '.join(df[df['sentiment'] == sentiment][review_col])

    wordcloud = WordCloud(
        font_path=font_path,
        background_color=background_color,
        width=800,
        height=400,
        colormap=colormap
    ).generate(text)

    plt.figure(figsize=figsize)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    if not title:
        title = f"{sentiment} 리뷰 WordCloud"
    plt.title(title, fontsize=16, color='black' if sentiment=='긍정' else 'white')
    plt.show()
