import streamlit as st
import constants


def form():
    with st.form("my-form"):
        occasion = st.selectbox("What is this card for?", constants.occasion_keyword_map.keys())
        person = st.text_input("Who is this card for?", max_chars=30)
        likes = st.text_input("What does this person like?", max_chars=30)
        tone = st.selectbox("Message Tone", constants.tone_select_options)
        orientation = st.selectbox("Orientation", ('Landscape', 'Portrait'))
        submitted = st.form_submit_button("Generate")
    form_data = {
        "occasion": occasion,
        "person": person,
        "likes": likes,
        "tone": tone,
        "orientation": orientation
    }
    return form_data, submitted
