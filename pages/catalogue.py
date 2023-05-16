import io
import requests
import streamlit as st
from PIL import Image
from constants import catalog_urls

st.title(":frame_with_picture: Browse Designs")
st.write("Checkout some of our generated cover designs")

cols = st.columns(4)


@st.cache_data(show_spinner=False)
def load_images():
    return [Image.open(requests.get(url, stream=True).raw) for url in catalog_urls]


with st.spinner("Loading images..."):
    images = load_images()

for i, img in enumerate(images):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()

    cols[i % 4].image(img, use_column_width=True)
    cols[i % 4].download_button("Download", byte_im, file_name=f"catalogue_img_{i}.png",
                                help="Download this image", key=i)
