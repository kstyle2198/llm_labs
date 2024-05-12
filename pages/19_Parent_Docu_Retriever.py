import streamlit as st
from utils import ParentDocuRetriever
from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain


import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
custom_page_config(layout='wide')
button_style()


pdr = ParentDocuRetriever()

if "result19" not in st.session_state:
    st.session_state.result19 = ""



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
    
    intial_query = st.text_input("질문을 입력해주세요.",  "what is the main features of FW Generator?")
    with st.spinner("Processing..."):
        if st.button("Parent & Child Split"):
            st.session_state.result19 = ""

            child_split = pdr.child_split(chuck_size=child_chunk_size, chuck_overlap=child_chuck_overlap)
            child_split
            parent_split = pdr.parent_split(chuck_size=parent_chunk_size, chunk_overlap=parent_chuck_overlap)
            parent_split
            embed_model = pdr.creat_embed_model()
            embed_model
            memorystore = pdr.create_ms()
            memorystore
            vectorstore = pdr.create_vs(docs=docs, embed_model=embed_model)
            vectorstore

            p_retriever = pdr.create_retriever(vectorstore=vectorstore, 
                                                store= memorystore,
                                                child_splitter = child_split,
                                                parent_splitter= parent_split,
                                                docs=docs)
            p_retriever
            retrieval_docs = p_retriever.invoke(intial_query)
            retrieval_docs
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
                    "context": retrieval_docs,
                    "messages": [
                        HumanMessage(content=intial_query)
                    ],
                }
            )
            st.session_state.result19 =  result9

    st.session_state.result19












    
    # with st.spinner("Processing..."):
    #     if st.button("Test"):
    #         col441, col442 = st.columns(2)
    #         with col441:
    #             st.markdown("#### Similarity Search with Score")
    #             result1 = st.session_state.vectorstore.similarity_search_with_score(intial_query)
    #             result1

    #         with col442:
    #             st.markdown("#### Parent Document Retriever")
    #             result3 = st.session_state.p_retriever.invoke(intial_query)
    #             result3




