import streamlit as st
from components import form
from st_pages import Page, show_pages

st.set_page_config(page_title="Card Cover Generator", page_icon="📚", initial_sidebar_state="expanded")

show_pages(
    [
        Page("app.py", "Customize Your Card", ":pencil2:"),
        Page("pages/catalogue.py", "Browse Designs", ":frame_with_picture:"),
    ]
)

if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    st.title(":pencil2: Customize Your Card")
    st.write("<h4>Create a custom card message and cover art!</h4>", unsafe_allow_html=True)
    form_data, submitted = form()
    if submitted:
        st.session_state.page = 2
        st.session_state.data = form_data
        st.experimental_rerun()
