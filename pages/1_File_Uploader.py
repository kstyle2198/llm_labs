from utils import FileUploader
import streamlit as st
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config


custom_page_config()
button_style()
file_uploader = FileUploader()

if __name__ == "__main__":
    make_title(emoji="🧪", title="File Uploader")
    make_gap(height=100)
    with st.container():
        file_uploader.file_uploader()

    