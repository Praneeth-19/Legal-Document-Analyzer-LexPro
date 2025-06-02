import streamlit as st
import requests

st.title("⚖️ Legal Document Analyzer")

text_input = st.text_area("Paste legal text here:", height=300)

if st.button("Analyze"):
    if text_input:
        response = requests.post("http://localhost:8000/analyze/", data={"text": text_input})
        if response.status_code == 200:
            results = response.json()
            st.subheader("📄 Summary")
            st.write(results["summary"])
            st.subheader("📌 Key Clauses")
            st.write(results["clauses"])
            st.subheader("🔍 Named Entities")
            st.write(results["entities"])
        else:
            st.error(f"Error from backend: {response.status_code} - {response.text}")
    else:
        st.warning("Please paste some legal text to analyze.")