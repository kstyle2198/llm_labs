import streamlit as st
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader

import base64
from pathlib import Path


class FileManager():
    def __init__(self):
        pass

    def list_selected_files(self, path, 확장자):
        file_list = os.listdir(path)
        selected_files = [file for file in file_list if file.endswith(확장자)]
        return selected_files

    def list_all_files(self, path):
        file_list = os.listdir(path)
        selected_files = [file for file in file_list]
        return selected_files


class Parsing():
    def __init__(self):
        pass

    def load_TextLoader(self, path):
        loader = TextLoader(path)
        data = loader.load()
        return data
    
    def load_UnstructuredMarkdownLoader(self, path):
        loader = UnstructuredMarkdownLoader(path, mode='elements') # elements or single
        data = loader.load()
        return data
    
    def load_CSVLoader(self, path):
        loader = CSVLoader(file_path=path)
        data = loader.load()
        return data
    
    def load_PyPDFLoader(self, path):
        loader = PyPDFLoader(path)
        pages = loader.load()
        return pages
    
    def load_PyMuPDFLoader(self, path):   
        loader = PyMuPDFLoader(path)
        data = loader.load()
        return data
    

class ShowPdf():
    def __init__(self):
        pass

    def show_pdf(self, path):
        pdf_path1 = Path(path)
        base64_pdf = base64.b64encode(pdf_path1.read_bytes()).decode("utf-8")
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height=1800" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

