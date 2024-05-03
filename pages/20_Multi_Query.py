import streamlit as st
from utils import MultiQuery, LineListOutputParser
from langchain_core.prompts import PromptTemplate
from typing import List


import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()

q = MultiQuery()

if "embed_model1" not in st.session_state:
    st.session_state.embed_model1 = ""
    st.session_state.vs1 = ""
    st.session_state.llm1 = ""
    st.session_state.rc1 = ""
    st.session_state.llm_chain1 = ""
    st.session_state.multi_query = ""

if __name__ == "__main__":
    make_title(emoji="🧪", title="Multi-Query")
    make_gap(height=50)

    with st.container(height=300):
        docs = st.session_state.splitted_result[:3]
        docs


    if st.button("Load Embed Model"):
        st.session_state.embed_model1 = q.creat_embed_model()
    
    if st.session_state.embed_model1: st.session_state.embed_model1

    if st.button("Create VectorStore"):
        st.session_state.vs1 = q.create_vs(docs=docs, embed_model=st.session_state.embed_model1)
    if st.session_state.vs1: st.session_state.vs1

    if st.button("Load LLM"):
        st.session_state.llm1 = q.load_llm()
    if st.session_state.llm1: st.session_state.llm1

    if st.button("Create Retrieval Chain"):
        st.session_state.rc1 = q.create_multi_query_retriever(llm=st.session_state.llm1, vectorstore=st.session_state.vs1)
    if st.session_state.rc1: st.session_state.rc1



    with st.expander("Test : get_relevant_documents"):
        query1 = st.text_area("테스트 문장", "PURCHASE ORDER SPECIFICATION FOR F.W. GENERATOR")
        with st.spinner("Processing..."):
            if st.button("Test"):
                result = st.session_state.rc1.get_relevant_documents(query1)
                result


    with st.spinner("Processing..."):
        if st.button("Create LLM Chain"):
            st.session_state.llm_chain1 = ""
            output_parser = LineListOutputParser()
            query_prompt = PromptTemplate(
                input_variables=["question"],
                template="""You are an AI language model assistant. Your task is to generate five
                different versions of the given user question to retrieve relevant documents from a vector
                database. By generating multiple perspectives on the user question, your goal is to help
                the user overcome some of the limitations of the distance-based similarity search.
                Provide these alternative questions separated by newlines.
                Original question: {question}""",
                # partial_variables={"format_instructions": output_parser.get_format_instructions()},
                )

            st.session_state.llm_chain1 = query_prompt | st.session_state.llm1 | output_parser

            st.session_state.llm_chain1
    
    intial_query = st.text_input("질문을 입력해주세요.", "what is the name of equipment?")
    intial_query = [intial_query]
    with st.spinner("Processing..."):
        if st.button("Create Multi Query"):
            try:
                res = st.session_state.llm_chain1.invoke(intial_query)
                st.markdown(f"정상: {res}")
            except Exception as e:
                res = e
                st.markdown(f"에러: {e}")
    

