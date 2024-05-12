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
    st.markdown(""" <style> .font {font-size:50px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)
    st.markdown(f"<p calss='font' style='text-align:center; font-size: {title_font_size}; color: {title_color};'>{emoji} {title}</p>", unsafe_allow_html=True)


# st.markdown('<p class="font">Guess the object Names</p>', unsafe_allow_html=True)



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
    
    ### Font change -> 나눔고딕 

    # font_link = 'https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap'
    font_link = "https://fonts.googleapis.com/css2?family=Sedan+SC&display=swap"
    st.markdown(f'<link href="{font_link}" rel="stylesheet">', unsafe_allow_html=True)
    custom_css = """
    <style>
        html, body, [class*="st-"] {
            font-family: 'Nanum Gothic', sans-serif;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


gap_border_line = False
def make_gap(height:int):
    global gap_border_line
    with st.container(height=height, border=gap_border_line): st.empty()