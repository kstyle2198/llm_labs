from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers




class ParentDocuRetriever():
    def __init__(self):
        pass

    def child_split(self, chuck_size=100, chuck_overlap=20):
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chuck_overlap)
        return child_splitter
    
    def parent_split(self, chuck_size=200, chunk_overlap=40):
        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chunk_overlap)
        return parent_splitter
    
    def creat_embed_model(self):
        model_name = "nomic-ai/nomic-embed-text-v1"
        model_kwargs = {'device': 'cpu', "trust_remote_code":True}
        encode_kwargs = {'normalize_embeddings': False}
        embed_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
            )
        return embed_model
    
    def create_ms(self):
        ms = InMemoryStore()
        return ms
    
    def create_vs(self, docs, embed_model):
        vectorstore = FAISS.from_documents(docs, embed_model)
        return vectorstore
    
    def load_llm(self):
        llm = CTransformers(model="./model/llama-2-7b-chat.ggmlv3.q8_0.bin", # Location of downloaded GGML model
                            model_type="llama",
                            stream=True,
                            config={'max_new_tokens': 256,
                                    'temperature': 0,
                                    'context_length': 4096})
        return llm
    
    def create_retriever(self, vectorstore, store, child_splitter, parent_splitter, docs):
        retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter)
        retriever.add_documents(docs, ids=None)
        return retriever
            




