import streamlit as st
from components import form
from pages import results, catalogue

if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    st.title("Card Cover Generator")
    st.write("<h4>Create a custom card message and cover art!</h4>", unsafe_allow_html=True)
    form_data, submitted = form()
    if submitted:
        st.session_state.page = 2
        st.session_state.data = form_data
        st.experimental_rerun()
