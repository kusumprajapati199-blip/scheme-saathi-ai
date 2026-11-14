import json
import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Scheme Saathi", page_icon="🏛️", layout="centered")
st.title("🏛️ Scheme Saathi")
st.caption("Multilingual Government Scheme Eligibility & Guidance Chatbot")

LANGUAGES = {
    "English": "Answer in clear, simple English.",
    "Hindi": "हिंदी में सरल और स्पष्ट उत्तर दें।",
}

@st.cache_data
def load_schemes():
    with open("schemes.json", "r", encoding="utf-8") as f:
        return json.load(f).get("schemes", [])

schemes = load_schemes()

with st.sidebar:
    st.header("Your details")
    language = st.selectbox("Language", list(LANGUAGES.keys()))
    age = st.number_input("Age", min_value=0, max_value=120, value=20)
    state = st.text_input("State", placeholder="e.g. Uttar Pradesh")
    annual_income = st.number_input("Annual family income (₹)", min_value=0, value=0, step=10000)
    occupation = st.selectbox("Occupation", ["Not specified", "Student", "Farmer", "Worker", "Self-employed", "Other"])
    category = st.selectbox("Category (optional)", ["Not specified", "General", "OBC", "SC", "ST", "Other"])
    check = st.button("Check possible schemes", use_container_width=True)

st.info("This is a guidance tool, not an official government portal. Final eligibility is decided by the relevant department.")

if not schemes:
    st.warning("No verified scheme information has been added yet. Add schemes to `schemes.json` using official government sources before using eligibility results.")
else:
    st.success(f"{len(schemes)} scheme record(s) loaded.")

profile = {
    "age": age,
    "state": state or "Not provided",
    "annual_family_income_inr": annual_income,
    "occupation": occupation,
    "category": category,
}

def ask_gemini(question):
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    if not api_key:
        return "Gemini API key is missing. Add GEMINI_API_KEY in Streamlit Secrets."
    if not schemes:
        return "I don't have verified scheme records yet. Please add official scheme details to schemes.json first."
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are Scheme Saathi, a careful government-scheme information assistant.
{LANGUAGES[language]}
Use ONLY the scheme data provided below. Never invent a scheme, eligibility rule,
benefit amount, document, deadline, website, or application process.
If the data does not answer something, say it is not available in the verified dataset.
Clearly distinguish 'may be eligible' from confirmed approval.
Mention the source URL for every scheme discussed.
User profile: {json.dumps(profile, ensure_ascii=False)}
Verified scheme dataset: {json.dumps(schemes, ensure_ascii=False)}
User question: {question}
Give a concise, easy-to-understand answer.
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text or "I couldn't generate a response. Please try again."

if check:
    st.subheader("Possible matches")
    with st.spinner("Checking the verified scheme rules..."):
        result = ask_gemini("Based on my profile, which schemes may I qualify for? Explain which rules match and which information is missing.")
    st.write(result)

st.divider()
st.subheader("Ask Scheme Saathi")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about eligibility, documents, or how to apply...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Preparing an answer..."):
            answer = ask_gemini(question)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
