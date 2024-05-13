import streamlit as st
import numpy as np
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
import time


import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
custom_page_config(layout='wide')
button_style()

def stream_data(answer):
    for word in answer.split(" "):
        yield word + " "
        time.sleep(0.1)

if "result18" not in st.session_state:
    st.session_state.result18 = ""

if __name__ == "__main__":
    make_title(emoji="🧪", title="Re-Ranking")
    make_gap(height=50)

    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjernbnlkdfj")
            docs = st.session_state.splitted_result[:sample_cnt]
            docs

    
    txt1 = st.text_area("질문", "what is the main features of FW Generator?")
    with st.spinner("Processing..."):
        if st.button("Re-Ranking"):
            st.session_state.result18 = ""

            model_name = "nomic-ai/nomic-embed-text-v1"
            model_kwargs = {'device': 'cpu', "trust_remote_code":True}
            encode_kwargs = {'normalize_embeddings': True}
            embed_model = OllamaEmbeddings(model="nomic-embed-text")
            vectorstore = FAISS.from_documents(docs, embed_model, distance_strategy=DistanceStrategy.DOT_PRODUCT)
            retrieved_docs = vectorstore.similarity_search(txt1, k=5)
            cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-2-v2", max_length=512, device="cpu")

            rr_reranked_docs = cross_encoder.rank(
                txt1,
                [doc.page_content for doc in retrieved_docs],
                top_k=3,
                return_documents=True,
                )
            
            rr_reranked_docs
            rearranged_docs = []
            for rr_reranked_doc in rr_reranked_docs:
                result = Document(
                    page_content=rr_reranked_doc["text"],
                    metadata = {} 
                )
                rearranged_docs.append(result)

            rearranged_docs

            llm = ChatOllama(model="llama3:latest")

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
                    "context": rearranged_docs,
                    "messages": [
                        HumanMessage(content=txt1)
                    ],
                }
            )
            st.session_state.result18 = result9

    st.session_state.result18
    st.write_stream(stream_data(st.session_state.result18))


