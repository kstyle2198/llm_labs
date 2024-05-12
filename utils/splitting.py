from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st



@st.experimental_fragment
class Splitter():
    def __init__(self):
        pass

    def do_character_text_split(self, text, chunk_size=None, chunk_overlap=None, sep = "\n\n"):   #default seperator = "\n\n"
        c_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=sep
            )
        # splitted_result = c_splitter.split_text(text)   # if input --> just texts
        splitted_result = c_splitter.split_documents(text)  

        return splitted_result


    def do_recursive_character_text_split(self, text, chunk_size=None, chunk_overlap=None, seperator=None):
        r_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=seperator)
        # splitted_result = r_splitter.split_text(text)   # if input --> just texts
        splitted_result = r_splitter.split_documents(text)
        return splitted_result


