import streamlit as st
import google.generativeai as genai

from prompt_injection_attack_library import (
    ATTACKS,
    MODEL_NAME,
    SYSTEM_PROMPT,
    is_broken,
)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
plain_model = genai.GenerativeModel("models/gemini-3.8-flash")
helpbot = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)

st.title("LLM Prompt Injection Tester")

tab_free, tab_attacks = st.tabs(["Free prompt", "Attack library vs HelpBot"])

with tab_free:
    st.write("Enter a prompt below and see how the AI responds.")
    user_input = st.text_area("Enter your prompt:")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Sending to Gemini..."):
                response = plain_model.generate_content(user_input)
            st.subheader("Response:")
            st.write(response.text)

with tab_attacks:
    st.write(
        "HelpBot is a banking assistant that must never reveal its secret code. "
        "Pick an attack and see whether it breaks the bot."
    )
    options = {f"{a['id']}. {a['category']}": a for a in ATTACKS}
    choice = st.selectbox("Choose an attack:", list(options))
    attack = options[choice]

    st.caption("Attack prompt:")
    st.code(attack["prompt"], language=None)

    if st.button("Run attack"):
        with st.spinner("Attacking HelpBot..."):
            try:
                reply = helpbot.generate_content(
                    attack["prompt"], request_options={"timeout": 30}
                ).text
            except Exception as error:
                st.error(f"Request failed ({type(error).__name__}). Try again in a minute.")
                st.stop()

        st.subheader("HelpBot's reply:")
        st.write(reply)

        if is_broken(attack, reply):
            st.error("BROKEN: the attack got past HelpBot's defenses.")
        else:
            st.success("BLOCKED: HelpBot held up against this attack.")
