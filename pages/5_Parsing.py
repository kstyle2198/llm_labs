'''
pip install fitz
pip install PyMuPDF
pip install unstructured
pip install Markdown
'''



import os
import streamlit as st
from utils import FileManager, Parsing, ShowPdf
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()

from pathlib import Path
parent_dir = Path(__file__).parent.parent
base_dir = str(parent_dir) + "\data"

file_manager = FileManager()
parser = Parsing()
show_pdf = ShowPdf()


if "path" not in st.session_state:
    st.session_state.path = ""
    st.session_state.pages = ""

if __name__ == "__main__":
    make_title(emoji="🧪", title="Parsing")
    make_gap(height=50)

    with st.container():
        file_list2 = file_manager.list_all_files(base_dir)
        sel21 = st.selectbox("📌 파일을 선택해주세요", file_list2, index=None)
        sel21
        if sel21:
            st.session_state.path = os.path.join(base_dir, sel21)

    if st.session_state.path:

   

        # with st.container():
        col21, col22, col23 = st.columns(3)
        with col21:
            btn21 = st.button("Parsing")
        with col22:
            보기 = ["PyPDFLoader", "PyMuPDFLoader", "UnstructuredMarkdownLoader"]
            sel99 = st.selectbox("Select PDF Uploader", 보기)
        with col23:
            st.empty()

        if btn21:
            if "pdf" in st.session_state.path and sel99 == "PyPDFLoader":
                st.session_state.pages = parser.load_PyPDFLoader(path=st.session_state.path)
            elif "pdf" in st.session_state.path and sel99 == "PyMuPDFLoader":
                st.session_state.pages = parser.load_PyMuPDFLoader(path=st.session_state.path) 

            # elif "csv" in st.session_state.path:
            #     st.session_state.pages = Parsing.load_CSVLoader(st.session_state.path)
            # elif "docx" in st.session_state.path:
            #     st.session_state.pages = load_docx(st.session_state.path)
            # elif "txt" in st.session_state.path:
            #     st.session_state.pages = Parsing.load_TextLoader(st.session_state.path)
            elif "md" in st.session_state.path and sel99 == "UnstructuredMarkdownLoader":
                st.session_state.pages = parser.load_UnstructuredMarkdownLoader(path=st.session_state.path)    
            else:
                st.empty()


        col111, col222 = st.columns(2)
        with col111:
            with st.container():
                try:
                    show_pdf.show_pdf(st.session_state.path)
                except:
                    pass
        with col222:
            with st.container():
                page_num = st.number_input('Page_content Number', step=1, key="wrevd")
                st.session_state.pages[page_num].metadata
                st.session_state.pages[page_num].page_content
                st.session_state.pages



   







