import os
import streamlit as st
# from utils import ChromaVectorStore
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()





if __name__ == "__main__":
    make_title(emoji="🧪", title="Retrieval Chain")
    make_gap(height=50)
