import streamlit as st
from utils import FileManager, ShowPdf, CustomPDFLoader
import os
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()


from pathlib import Path
parent_dir = Path(__file__).parent.parent
base_dir = str(parent_dir) + "\data"

file_manager = FileManager()
show_pdf = ShowPdf()
custom_loader = CustomPDFLoader()

if "path9" not in st.session_state:
    st.session_state.path9 = ""
    st.session_state.pages = ""
    

if __name__ == "__main__":
    make_title(emoji="🧪", title="Parsing to the Hell")
    make_gap(height=50)

    with st.container():
        file_list2 = file_manager.list_all_files(base_dir)
        sel21 = st.selectbox("📌 파일을 선택해주세요", file_list2, index=None, key="wetgfw")
        if sel21:
            st.session_state.path9 = os.path.join(base_dir, sel21)
    if st.session_state.path9: st.session_state.path9

    with st.spinner("Processing..."):
        crop_check = st.checkbox("Crop", value=True)
        if st.button("TEST1"):
            st.session_state.pages = ""
            st.session_state.pages = custom_loader.lazy_load(st.session_state.path9, crop_check)
            
    col31, col32 = st.columns(2)
    with col31:
        try: show_pdf.show_pdf(st.session_state.path9)
        except: pass
    with col32:
        with st.container():
            page_num1 = st.number_input('Page_content Number', step=1, key="wrevddd")
            
            st.session_state.pages[page_num1].metadata
            st.session_state.pages[page_num1].page_content
            st.session_state.pages[page_num1]
