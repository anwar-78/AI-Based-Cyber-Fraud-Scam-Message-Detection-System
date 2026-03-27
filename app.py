import streamlit as st
import pickle
import re
from keywords import scam_keywords

model = pickle.load(open("model/model.pkl","rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl","rb"))

st.set_page_config(page_title="AI Cyber Scam Detector")

st.title("🛡 AI Cyber Fraud Detector")

message = st.text_area("Enter message to analyze")

def detect_link(text):
    pattern = r"http[s]?://"
    return re.search(pattern,text)

def keyword_scan(text):
    found=[]
    for word in scam_keywords:
        if word in text.lower():
            found.append(word)
    return found

if st.button("Analyze Message"):

    vector = vectorizer.transform([message])
    prediction = model.predict(vector)

    prob = model.predict_proba(vector)[0][1]

    risk = int(prob*100)

    if detect_link(message):
        st.warning("⚠ Suspicious link detected")

    keywords_found = keyword_scan(message)

    if keywords_found:
        st.info("Scam keywords found: "+",".join(keywords_found))

    if prediction[0]==1:
        st.error("⚠ Scam Message Detected")
    else:
        st.success("✅ Safe Message")

    st.subheader("Risk Meter")

    st.progress(risk)

    st.write("Risk Percentage:",risk,"%")