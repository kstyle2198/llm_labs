import streamlit as st
# from utils import to_markdown, convert_pdf_to_markdown
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

# custom_page_config(layout='wide')
# button_style()

# base_dir = "D:\AA_develop\\adv_llm_labs\data"

# to_markdown = to_markdown()
# convert_pdf_to_markdown = convert_pdf_to_markdown()



if __name__ == "__main__":
    make_title(emoji="🧪", title="PDF to Markdown")
    make_gap(height=50)
    pass