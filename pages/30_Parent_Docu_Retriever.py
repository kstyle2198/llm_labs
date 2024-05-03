import streamlit as st
from utils import ParentDocuRetriever
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
custom_page_config(layout='wide')
button_style()


pdr = ParentDocuRetriever()

if "child_split" not in st.session_state:
    st.session_state.child_split = ""
    st.session_state.parent_split = ""
    st.session_state.embed_model = ""
    st.session_state.vectorstore = ""
    st.session_state.memorystore = ""
    st.session_state.p_retriever = ""


if __name__ == "__main__":
    make_title(emoji="🧪", title="Parent Document Retriever")
    make_gap(height=50)

    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjerlkdfj")
            docs = st.session_state.splitted_result[:sample_cnt]
            docs

    col501, col502, col503, col504 = st.columns(4)
    with col501: child_chunk_size = st.number_input("child_chunk_size", step=10, min_value=100, max_value=500, value="min", key="dgjerlsadfakdfj")
    with col502: child_chuck_overlap = st.number_input("child_chuck_overlap", step=10, min_value=20, max_value=50, value="min", key="dgjerlhfdkdfj")
    with col503: parent_chunk_size = st.number_input("parent_chunk_size", step=10, min_value=200, max_value=1000, value="min", key="dgjerlbnmkdfj")
    with col504: parent_chuck_overlap = st.number_input("parent_chuck_overlap", step=10, min_value=40, max_value=100, value="min", key="dgjevbrlkdfj")

    if st.button("Parent & Child Split"):
        st.session_state.child_split = pdr.child_split(chuck_size=child_chunk_size, chuck_overlap=child_chuck_overlap)
        st.session_state.child_split
        st.session_state.parent_split = pdr.parent_split(chuck_size=parent_chunk_size, chunk_overlap=parent_chuck_overlap)
        st.session_state.parent_split
        
    if st.button("Create VectorStore"):
        st.session_state.embed_model = pdr.creat_embed_model()
        st.session_state.embed_model
        st.session_state.memorystore = pdr.create_ms()
        st.session_state.memorystore
        st.session_state.vectorstore = pdr.create_vs(docs=docs, embed_model=st.session_state.embed_model)
        st.session_state.vectorstore

    with st.spinner("Processing..."):
        if st.button("Parent Document Retriever"):
            st.session_state.p_retriever = pdr.create_retriever(vectorstore=st.session_state.vectorstore, 
                                                                store= st.session_state.memorystore,
                                                                child_splitter = st.session_state.child_split,
                                                                parent_splitter= st.session_state.parent_split,
                                                                docs=docs)
            st.session_state.p_retriever


    intial_query = st.text_input("질문을 입력해주세요.", "what is the name of equipment?")
    with st.spinner("Processing..."):
        if st.button("Test"):
            col441, col442 = st.columns(2)
            with col441:
                st.markdown("#### Similarity Search")
                result1 = st.session_state.vectorstore.similarity_search(intial_query)
                result1
            with col442:
                st.markdown("#### Parent Document Retriever")
                result2 = st.session_state.p_retriever.get_relevant_documents(intial_query)
                result2




