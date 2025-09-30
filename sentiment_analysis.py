# sentiment_analysis.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import pandas as pd
from tqdm import tqdm

# 1. 모델 & 토크나이저 로드
MODEL_NAME = "Copycats/koelectra-base-v3-generalized-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# 2. 레이블 매핑
id2label = {0: "부정", 1: "긍정"}

# 3. 감성 분석 함수 (단일 텍스트)
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return id2label[pred], probs.squeeze().tolist()

# 4. DataFrame 단위 감성 분석 함수
def analyze_reviews(df, text_column="review"):
    sentiments = []
    probabilities = []

    for review in tqdm(df[text_column]):
        try:
            label, probs = predict_sentiment(review)
        except Exception as e:
            label, probs = "분석 실패", [0.0, 0.0]
        sentiments.append(label)
        probabilities.append(probs)

    df["sentiment"] = sentiments
    df["probabilities"] = probabilities
    return df
