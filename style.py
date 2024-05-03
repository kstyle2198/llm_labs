import streamlit as st


def custom_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="expanded"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state)

title_font_size = "45px"
title_color = "navy"
def make_title(emoji:str, title:str):
    global title_font_size, title_color
    st.markdown(f"<h1 style='text-align:center; font-size: {title_font_size}; color: {title_color};'>{emoji} {title}</h1>", unsafe_allow_html=True)


def button_style():
    st.markdown(""" 
            <style>
            div.stButton > button:first-child {
            background-color: #0A66C2;
            color:white;
            font-size:20px;
            height:2em;
            width:10em;
            border-radius:10px 10px 10px 10px;
            position:relative;
            left:0%
            }
            </style>""", unsafe_allow_html=True)


gap_border_line = False
def make_gap(height:int):
    global gap_border_line
    with st.container(height=height, border=gap_border_line): st.empty()