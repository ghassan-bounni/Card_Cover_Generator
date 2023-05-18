import io
import random
import streamlit as st
from text_generator import generate_card_text
from cover_generator import generate_card_images
import constants


def results():
    occasion, person, likes, tone, orientation = st.session_state.data.values()

    st.header("Generated Message")

    if "message" not in st.session_state:
        st.session_state.message = generate_card_text(occasion, person, likes, tone)

    st.write(st.session_state.message)

    if st.button("Back"):
        st.session_state.page = 1
        st.experimental_rerun()

    st.header("Images")

    if "images" in st.session_state:
        cols = st.columns(3)
        for i, img in enumerate(st.session_state.images):
            cols[i % 3].image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            byte_im = buf.getvalue()
            cols[i % 3].download_button("Download", byte_im, file_name=f"img_{i}.png",
                                        help="Download this image", key=random.randint(1, 1000000))

    if "cleaned_images" in st.session_state:
        st.write("Transparent Background")
        cleaned_cols = st.columns(3)

        for i, img in enumerate(st.session_state.cleaned_images):
            im = cleaned_cols[i % 3].image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            byte_im = buf.getvalue()
            cleaned_cols[i % 3].download_button("Download", byte_im, file_name=f"img_{i}_transparent.png",
                                                help="Download this image", key=random.randint(1, 1000000))

    clean = st.checkbox("Do you want a transparent background?")

    with st.container():

        if st.button("Generate Cover Art"):
            if "images" in st.session_state:
                del st.session_state.images
            if "cleaned_images" in st.session_state:
                del st.session_state.cleaned_images

            st.session_state.images, cleaned_images = generate_card_images(
                constants.occasion_keyword_map[occasion],
                orientation, clean)

            if cleaned_images:
                st.session_state.cleaned_images = cleaned_images

            st.experimental_rerun()