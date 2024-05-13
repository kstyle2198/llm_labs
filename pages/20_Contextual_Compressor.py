import streamlit as st
# from utils import ContextualCompress
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
import time

def stream_data(answer):
    for word in answer.split(" "):
        yield word + " "
        time.sleep(0.1)

import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
custom_page_config(layout='wide')
button_style()


if "result20" not in st.session_state:
    st.session_state.result20 = ""

# con_com = ContextualCompress()

if __name__ == "__main__":
    make_title(emoji="🧪", title="Contextual Compressor")
    make_gap(height=50)

    st.info("Metadata에 리스트 또는 None이 있으면 에러남.. ")

    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjedsxrlkdfj")
            docs = st.session_state.splitted_result[:sample_cnt]
            docs

    test_query = st.text_input("질문을 입력해주세요.", "what is the main features of FW Generator?", key="erdfsf")
    with st.spinner("Processing..."):
        if st.button("Test"):
            st.session_state.result20 = ""

            model_name = "nomic-ai/nomic-embed-text-v1"
            model_kwargs = {'device': 'cpu', "trust_remote_code":True}
            encode_kwargs = {'normalize_embeddings': False}
            embed_model = OllamaEmbeddings(model="nomic-embed-text")
            vectorstore = Chroma.from_documents(docs, embed_model)

            retriever = vectorstore.as_retriever()

            llm = ChatOllama(model="llama3:latest")

            compressor = LLMChainExtractor.from_llm(llm)
            compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)




            # compression_retriever = con_com.create_compression_retriever(docs=docs)
            compressed_docs = compression_retriever.invoke(test_query)
            compressed_docs

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

            from langchain_core.messages import HumanMessage

            result = document_chain.invoke(
                {
                    "context": compressed_docs,
                    "messages": [
                        HumanMessage(content=test_query)
                    ],
                }
            )
            st.session_state.result20 = result

    st.session_state.result20
    st.write_stream(stream_data(st.session_state.result20))