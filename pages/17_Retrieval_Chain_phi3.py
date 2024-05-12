import os
import streamlit as st
# from utils import ChromaVectorStore
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config



from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from llama_cpp import Llama


custom_page_config(layout='wide')
button_style()



# A utility function for answer generation
def ask(question):
   context = retriever.invoke(question)
   st.markdown(context)

   answer = (chain({"input_documents": context, "question": question}, return_only_outputs=True))['output_text']
   return answer


if __name__ == "__main__":
    make_title(emoji="🧪", title="Retrieval Chain")
    make_gap(height=50)

    with st.expander("Documents"):
        with st.container(height=300):
            sample_cnt = st.number_input("샘플개수", step=10, min_value=5, max_value=500, value="min", key="dgjernbnlkdfj")
            splitted_texts = st.session_state.splitted_result[:sample_cnt]
            splitted_texts

    user_question = st.text_input("My Query", "what is the main features of FW Generator?")
    
    if st.button("Test4"):
        model_name = "nomic-ai/nomic-embed-text-v1"
        model_kwargs = {'device': 'cpu', "trust_remote_code":True}
        encode_kwargs = {'normalize_embeddings': False}
        embed_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
            )


        llm = Llama(
            model_path="./model/Phi-3-mini-4k-instruct-q4.gguf",  # path to GGUF file
            n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
            n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
            n_gpu_layers=0, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
            )


        db=Chroma.from_documents(splitted_texts, embedding=embed_model, persist_directory="test_index")
        # db.persist()

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
        answer = (answer.split("<|assistant|>")[-1]).strip()
        answer