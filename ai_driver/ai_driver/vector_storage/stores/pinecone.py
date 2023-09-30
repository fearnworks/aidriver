import pinecone
from llama_index.vector_stores import PineconeVectorStore

def init_index(index_name: str):
    pinecone.create_index(index_name, dimension=1536, metric="euclidean", pod_type="p1")
    index = pinecone.Index(index_name)
    return index

def get_index(index_name: str, reset: bool = False) -> PineconeVectorStore:
    index = pinecone.Index(index_name)
    if reset:
        index.delete(deleteAll=True)
    vector_store = PineconeVectorStore(pinecone_index=index)
    return vector_store
