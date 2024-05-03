import streamlit as st
from utils import Splitter
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()

splitter = Splitter()

if "splitted_result" not in st.session_state:
    st.session_state.splitted_result = ""
    st.session_state.content_list = []
    st.session_state.metatdata_list = []
 

if __name__ == "__main__":
    make_title(emoji="🧪", title="Splitter")
    make_gap(height=50)

    col331, col332, col333 = st.columns(3)
    with col331: selected_splitter = st.radio("Splitter", ["RecursiveCharacterTextSplitter", "CharacterTextSplitter"])
    with col332: chunck_size = st.number_input("chunck_size", step=50, min_value=200, max_value=500, value="min", key="dgjlkdfj")
    with col333: chunk_overlap = st.number_input("chunk_overlap", step=10, min_value=20, max_value=100, value="min", key="dgjlkddfdffj")

    with st.expander("Pasing Documents"):
        with st.container(height=300):
            try:
                st.session_state.pages
            except:
                st.warning("Pasing을 먼저 실시해주세요.")

    if st.button("Split"):
        st.session_state.splitted_result = ""
        if selected_splitter == "RecursiveCharacterTextSplitter":
            st.session_state.splitted_result = splitter.do_recursive_character_text_split(st.session_state.pages, chunk_size=chunck_size, chunk_overlap=chunk_overlap, seperator=["\n\n", "\n", " ", ""])
        else:
            st.info("CharacterTextSplitter 준비 안됨.. 거의 안쓰니까..")

    
    st.session_state.content_list = [x.page_content for x in st.session_state.splitted_result]
    st.session_state.metatdata_list = [x.metadata for x in st.session_state.splitted_result]


    if st.session_state.splitted_result: 
        st.session_state.content_list = [x.page_content for x in st.session_state.splitted_result]
        st.session_state.metatdata_list = [x.metadata for x in st.session_state.splitted_result]
        with st.container(height=500):
            col3331, col3332 = st.columns(2)
            with col3331: st.session_state.content_list
            with col3332: st.session_state.metatdata_list
        
        
        
        with st.expander("Full Result"): 
            with st.container(height=500): st.session_state.splitted_result

    

    
    



