import streamlit as st
# from utils import MultiQuery, LineListOutputParser
# from langchain.output_parsers import PydanticOutputParser
# from langchain_core.prompts import PromptTemplate
# from pydantic import BaseModel, Field

# from typing import List, Optional
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


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


if "result25" not in st.session_state:
    st.session_state.result25 = ""


if __name__ == "__main__":
    make_title(emoji="🧪", title="Multi-Query")
    make_gap(height=50)

    with st.container(height=300):
        sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjerldgdekdfj")
        docs = st.session_state.splitted_result[:sample_cnt]
        docs

    
    my_context = st.text_input("my_context", "what is the main features of FW Generator?")
    with st.spinner("Processing..."):

        if st.button("Test"):
            st.session_state.result25 = ""

            model_name = "nomic-ai/nomic-embed-text-v1"
            model_kwargs = {'device': 'cpu', "trust_remote_code":True}
            encode_kwargs = {'normalize_embeddings': False}
            embed_model = OllamaEmbeddings(model="nomic-embed-text")
            
            vectorstore = FAISS.from_documents(docs, embed_model)

            llm1 = ChatOllama(model="llama3:latest")
        

            retriever_from_llm = MultiQueryRetriever.from_llm(
                retriever=vectorstore.as_retriever(), llm=llm1)
        
            import logging
            logging.basicConfig()
            logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

            unique_docs = retriever_from_llm.invoke(my_context)
            unique_docs


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

            document_chain = create_stuff_documents_chain(llm1, question_answering_prompt)

            result = document_chain.invoke(
                {
                    "context": unique_docs,
                    "messages": [
                        HumanMessage(content=my_context)
                    ],
                }
            )
            st.session_state.result25 = result
    st.session_state.result25
    st.write_stream(stream_data(st.session_state.result25))



