import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.llms import CTransformers


class SelfQueryRC():
    def __init__(self):
        pass

    def create_self_query_chain(self, docs, document_content_description, metadata_field_info, query):
        model_name = "nomic-ai/nomic-embed-text-v1"
        model_kwargs = {'device': 'cpu', "trust_remote_code":True}
        encode_kwargs = {'normalize_embeddings': False}
        embed_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
            )
        vectorstore = Chroma.from_documents(docs, embed_model)
        llm = CTransformers(model="./model/llama-2-7b-chat.ggmlv3.q8_0.bin", # Location of downloaded GGML model
                            model_type="llama",
                            stream=True,
                            config={'max_new_tokens': 256,
                                    'temperature': 0,
                                    'context_length': 4096})
        
        retriever = SelfQueryRetriever.from_llm(llm, vectorstore, document_content_description, metadata_field_info)
        result = retriever.invoke(query)
        return result
    
