import streamlit as st
from style import make_title, make_gap, custom_page_config

custom_page_config()

if __name__ == "__main__":
    
    # 윗여백
    make_gap(height=20)
    # 타이틀
    make_title(emoji="🧪", title="Advanced LLM Labs")
    make_gap(height=100)

    st.chat_input()
