import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer
client = chromadb.PersistentClient()


@st.experimental_fragment
class ChromaVectorStore():
    def __init__(self):
        pass

    def create_embed_model(self):
        model = SentenceTransformer('nomic-ai/nomic-embed-text-v1', trust_remote_code=True)
        return model

    def create_vectordb(self, model, docs, chunk_size):
        client = chromadb.PersistentClient()
        try:
            client.delete_collection("vectorstore")
        except:
            pass
        vectorstore = client.create_collection(name="vectorstore")

        ids = []
        metadatas = []
        embeddings = []

        for id, txt in enumerate(docs):
            metadata = {"content": txt}
            embedding = model.encode(txt, normalize_embeddings=True)

            ids.append(str(id))
            metadatas.append(metadata)
            embeddings.append(embedding)

        chunk_size = chunk_size  # 한 번에 처리할 chunk 크기 설정
        total_chunks = len(embeddings) // chunk_size + 1  # 전체 데이터를 chunk 단위로 나눈 횟수
        embeddings = [e.tolist() for e in embeddings] 

        for chunk_idx in range(total_chunks):
            start_idx = chunk_idx * chunk_size
            end_idx = (chunk_idx + 1) * chunk_size
            
            # chunk 단위로 데이터 자르기
            chunk_embeddings = embeddings[start_idx:end_idx]
            chunk_ids = ids[start_idx:end_idx]
            chunk_metadatas = metadatas[start_idx:end_idx]
            
            # chunk를 vectorstore 추가
            vectorstore.add(embeddings=chunk_embeddings, ids=chunk_ids, metadatas=chunk_metadatas)
        return vectorstore

