import streamlit as st
import requests
import random

API_URL = "https://api-inference.huggingface.co/models/facebook/roberta-hate-speech-dynabench-r4-target"
headers = {"Authorization": "Bearer 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"}

# Global variable to track input count
if 'input_count' not in st.session_state:
    st.session_state.input_count = 0

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

# Inject CSS for background and styling
st.markdown("""
    <style>
        body {
            background-color: #f7f7f7; /* Soft light gray */
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #7f58af; /* Soft purple */
            color: white;
            font-size: 18px;
            padding: 10px 30px;
            border-radius: 10px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #5e42a6; /* Slightly darker purple on hover */
            cursor: pointer;
        }
        .stSuccess {
            color: #1a9e1a; /* Green for positive verdict */
        }
        .stWarning {
            color: #ffa500; /* Orange for warning */
        }
        .stError {
            color: #ff0000; /* Red for error */
        }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Kathy’s Sass-O-Meter™")
st.caption("Powered by Huggy Bear & STEKA - co-starring Shanthi")

# Input text box
user_input = st.text_input("Enter your phrase below:", "")

if st.button("Sassify Me Kathy"):
    # Increase the input count each time button is pressed
    st.session_state.input_count += 1
    
    if st.session_state.input_count == 4:
        st.warning("This is getting boring.. Type **'Fuck You'** in the box if you Dare")
        st.stop()  # Stops the app here until the user types 'Fuck You'
    
    # Check if the user typed 'Fuck You' after the 4th input
    if user_input.strip().lower() == "fuck you":
        st.text_input("Enter your phrase below:", value="", key="cleared_box")
        st.warning("**Fuck Me?** - No - **F You**, and your newly encrypted files. Want the key? Send **.5 BC** to **DoNotPissKathyOff@aol.com**. Add another .5 BC if you don't want your porn history sent to all the people in your contacts.")
        st.stop()  # Stop further input
    elif not user_input.strip():
        st.warning("Please enter some text to sassify.")
    else:
        verdict, confidence = classify_text(user_input)
        follow_ups = {
            "NOTHATE": [
                "You’re funnier than I thought!",
                "Look at you, cracking jokes like a pro!",
                "Not bad, you're a delight!"
            ],
            "HATE": [
                "Ouch! Might want to keep this one to yourself next time.",
                "Yikes, that one cut deep! Kathy can’t save you now.",
                "You sure you want to say that? Kathy's not gonna let that slide."
            ],
            "UNKNOWN": [
                "Huggy Bear was confused—try rephrasing!",
                "Even Huggy Bear can’t figure that one out."
            ]
        }
        if verdict == "ERROR":
            st.error("Sorry, Huggy Bear had a meltdown. Try again.")
        else:
            follow_up = random.choice(follow_ups[verdict])
            st.success(f"**Verdict:** {verdict}\n**Confidence:** {confidence:.2%}\n{follow_up}")


