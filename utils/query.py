from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.retrievers.multi_query import MultiQueryRetriever

from typing import List
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


class MultiQuery():
    def __init__(self):
        pass

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
    
    def create_multi_query_retriever(self, llm, vectorstore):
        retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)
        return retriever
    
    
    
    
class LineList(BaseModel):
    lines: List[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)


    
