from abc import ABC, abstractmethod

class VectorStore(ABC):
    
    @abstractmethod
    def add_documents():
        pass 
    
    @abstractmethod
    def get_relevant_documents(query: str, limit: int):
        pass
    
    @abstractmethod
    def create_index():
        pass 