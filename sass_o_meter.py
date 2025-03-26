import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/roberta-hate-speech-dynabench-r4-target"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json={"inputs": payload})
    if response.status_code == 200:
        return response.json()
    else:
        return [[{"label": "UNKNOWN", "score": 0.0}]]

def classify_text(text):
    try:
        result = query(text)
        label_scores = {item['label']: item['score'] for item in result[0]}
        top_label = max(label_scores, key=label_scores.get)
        top_score = label_scores[top_label]
        return top_label.upper(), top_score
    except Exception as e:
        return "ERROR", 0.0

# Streamlit App
st.set_page_config(page_title="Kathy’s Sass-O-Meter™", layout="centered")
st.title("💬 Kathy’s Sass-O-Meter™")
st.caption("Powered by Huggy Bear & STEKA")

user_input = st.text_input("Enter your phrase below:", "")

if st.button("Sassify Me Kathy"):
    if not user_input.strip():
        st.warning("Please enter some text to sassify.")
    else:
        verdict, confidence = classify_text(user_input)
        if verdict == "ERROR":
            st.error("Sorry, Huggy Bear had a meltdown. Try again.")
        elif verdict == "UNKNOWN":
            st.info("Huggy didn’t know how to classify that. Try rephrasing.")
        else:
            st.success(f"**Verdict:** {verdict}\n**Confidence:** {confidence:.2%}")