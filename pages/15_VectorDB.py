import os
import streamlit as st
from utils import ChromaVectorStore
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()


vs = ChromaVectorStore()

if "embed_model" not in st.session_state:
    st.session_state.embed_model = ""
    st.session_state.vectordb = ""

if __name__ == "__main__":
    make_title(emoji="🧪", title="Vector DataBase")
    make_gap(height=50)


    sample_cnt = st.number_input("샘플문장개수", step=1, min_value=3, max_value=500, value="min", key="dgjdfdflkdfj")

    target = st.session_state.content_list[:sample_cnt] 
    target

    if st.button("Load Embed Model"):
        st.session_state.embed_model = vs.create_embed_model()
        st.session_state.embed_model


    if st.button("Create VectorDB"):
        st.session_state.vectordb = vs.create_vectordb(model=st.session_state.embed_model, docs=target, chunk_size=1024)
        st.session_state.vectordb

    
    조회문장 = st.text_area("유사도 조회 문장", "PURCHASE ORDER SPECIFICATION FOR F.W. GENERATOR")
    if st.session_state.vectordb and st.button("Test"):


        result = st.session_state.vectordb.query(
            query_embeddings=st.session_state.embed_model.encode(조회문장, normalize_embeddings=True).tolist(),
            n_results=3)
        result
    



