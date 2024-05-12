import os
import streamlit as st
# from utils import ChromaVectorStore
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


custom_page_config(layout='wide')
button_style()


if "result17" not in st.session_state:
    st.session_state.result17 = ""


if __name__ == "__main__":
    make_title(emoji="🧪", title="Retrieval Chain")
    make_gap(height=50)

    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjernbnlkdfj")
            splitted_texts = st.session_state.splitted_result[:sample_cnt]
            splitted_texts

    my_query = st.text_input("My Query", "what is the main features of FW Generator?")
    with st.spinner("Processing..."):
        if st.button("Test4"):
            st.session_state.result7 = ""

            model_name = "nomic-ai/nomic-embed-text-v1"
            model_kwargs = {'device': 'cpu', "trust_remote_code":True}
            encode_kwargs = {'normalize_embeddings': True}
            embed_model = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
                multi_process=False,
                show_progress=False
                )
            vectorstore = FAISS.from_documents(splitted_texts, embed_model, distance_strategy=DistanceStrategy.DOT_PRODUCT)
            retriever = vectorstore.as_retriever(k=4)
            docs = retriever.invoke(my_query)
            docs


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
                [("system",
                  SYSTEM_TEMPLATE,),
                  MessagesPlaceholder(variable_name="messages"),
                  ])

            document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

            from langchain_core.messages import HumanMessage

            result = document_chain.invoke(
                {
                    "context": docs,
                    "messages": [
                        HumanMessage(content=my_query)
                    ],
                }
            )
            st.session_state.result17 = result
    
    st.session_state.result17

    