import streamlit as st
from langchain.chains.query_constructor.base import AttributeInfo
from utils import SelfQueryRC
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers

import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
custom_page_config(layout='wide')
button_style()


# if "embed_model" not in st.session_state:
#     st.session_state.self_embed_model = ""
#     st.session_state.self_vectorstore = ""
#     st.session_state.self_llm = ""
#     st.session_state.self_retriever = ""

self_rc = SelfQueryRC()

if __name__ == "__main__":
    st.info("Metadata에 리스트가 있으면 에러남.. ")
    make_title(emoji="🧪", title="Self Query Retriever")
    make_gap(height=50)


    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjerlk33dfj")
            docs = st.session_state.splitted_result[:sample_cnt]
            docs

    document_content_description = "Guidelines for Safe STS LNG Transfer Operation"
    metadata_field_info = [
        AttributeInfo(
            name="page_number",
            description="page number",
            type="integer",
            ),
        AttributeInfo(
            name="keywords",
            description="important words in the context like the name of equipment",
            type="string",
            ),
        AttributeInfo(
            name="table_contexts",
            description="contents of tables that is included in the page",
            type="string",
            ),
        AttributeInfo(
            name="source",
            description="directory information (e.g., D:\\AA_develop\\adv_llm_labs\\data\\Unit_Cooler.pdf)",
            type="string",
            ),
        
        ]
    with st.expander("document_content_description & metadata_field_info"):
        document_content_description
        metadata_field_info

    test_query = st.text_input("질문을 입력해주세요.", "what is the main features of FW Generator?", key="erf")
    with st.spinner("Processing..."):
        if st.button("Self Query Retriever"):
            st.session_state.self_retriever = ""
            result = self_rc.create_self_query_chain(docs, document_content_description, metadata_field_info, test_query)
            result
            llm = CTransformers(model="./model/llama-2-7b-chat.ggmlv3.q8_0.bin", # Location of downloaded GGML model
                            model_type="llama",
                            stream=True,
                            config={'max_new_tokens': 256,
                                    'temperature': 0,
                                    'context_length': 4096})
            SYSTEM_TEMPLATE = """
            Answer the user's questions based on the below context. 
            If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

            <context>
            {context}
            </context>
            """   
            question_answering_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        SYSTEM_TEMPLATE,
                    ),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )

            document_chain = create_stuff_documents_chain(llm, question_answering_prompt)
            result9 = document_chain.invoke(
                {
                    "context": result,
                    "messages": [
                        HumanMessage(content=test_query)
                    ],
                }
            )
            result9



