import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-3.8-flash")

st.title("LLM Prompt Injection Tester")
st.write("Enter a prompt below and see how the AI responds.")

user_input = st.text_area("Enter your prompt:")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Sending to Gemini..."):
            response = model.generate_content(user_input)
        st.subheader("Response:")
        st.write(response.text)
