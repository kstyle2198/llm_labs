import os
import streamlit as st
# from utils import ChromaVectorStore
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
import time

custom_page_config(layout='wide')
button_style()

def stream_data(answer):
    for word in answer.split(" "):
        yield word + " "
        time.sleep(0.1)

# A utility function for answer generation
def ask(question):
   context = retriever.invoke(question)
   st.markdown(context)

   answer = (chain({"input_documents": context, "question": question}, return_only_outputs=True))['output_text']
   return answer

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

    user_question = st.text_input("My Query", "what is the main features of FW Generator?")
    
    with st.spinner("Processing..."):
        if st.button("Test4"):
            model_name = "nomic-ai/nomic-embed-text-v1"
            model_kwargs = {'device': 'cpu', "trust_remote_code":True}
            encode_kwargs = {'normalize_embeddings': False}
            embed_model = OllamaEmbeddings(model="nomic-embed-text")

            llm = ChatOllama(model="phi3:latest")
            db=Chroma.from_documents(splitted_texts, embedding=embed_model, persist_directory="test_index")

            # Load the database
            vectordb = Chroma(persist_directory="test_index", embedding_function = embed_model)

            # Load the retriver
            retriever = vectordb.as_retriever(search_kwargs = {"k" : 3})

            # Define the custom prompt template suitable for the Phi-3 model
            qna_prompt_template="""<|system|>
            You have been provided with the context and a question, try to find out the answer to the question only using the context information. If the answer to the question is not found within the context, return "I dont know" as the response.<|end|>
            <|user|>
            Context:
            {context}

            Question: {question}<|end|>
            <|assistant|>"""
            PROMPT = PromptTemplate(template=qna_prompt_template, input_variables=["context", "question"])

            # Define the QNA chain
            chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)

            # Take the user input and call the function to generate output
            answer = ask(user_question)
            st.session_state.result17 = (answer.split("<|assistant|>")[-1]).strip()

        st.write_stream(stream_data(st.session_state.result17))
        st.session_state.result17