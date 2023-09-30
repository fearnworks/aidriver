import os
from llama_hub.file.pymu_pdf.base import PyMuPDFReader
from llama_index.text_splitter import SentenceSplitter
from llama_index.schema import TextNode
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
)
from llama_index.embeddings import OpenAIEmbedding

def load_pdf(path):
    loader = PyMuPDFReader()
    documents = loader.load(file_path=path)
    return documents

def split_docs(documents):
    text_splitter = SentenceSplitter(
        chunk_size=1024,
        # separator=" ",
    )
    text_chunks = []
    # maintain relationship with source doc index, to help inject doc metadata in (3)
    doc_idxs = []
    for doc_idx, doc in enumerate(documents):
        cur_text_chunks = text_splitter.split_text(doc.text)
        text_chunks.extend(cur_text_chunks)
        doc_idxs.extend([doc_idx] * len(cur_text_chunks))
    return text_chunks, doc_idxs

def extract_metadata(nodes, llm):
    metadata_extractor = MetadataExtractor(
        extractors=[
            TitleExtractor(nodes=5, llm=llm),
            QuestionsAnsweredExtractor(questions=3, llm=llm),
        ],
        in_place=False,
    )
    nodes = metadata_extractor
    return nodes

def create_nodes(text_chunks, documents, doc_idxs):
    nodes = []
    for idx, text_chunk in enumerate(text_chunks):
        node = TextNode(
            text=text_chunk,
        )
        src_doc = documents[doc_idxs[idx]]
        node.metadata = src_doc.metadata
        nodes.append(node)
    print(nodes[0].get_content(metadata_mode="all"))
    return nodes

def embed_nodes(nodes, embed_model = OpenAIEmbedding):
    embed_model = embed_model()
    for node in nodes:
        node_embedding = embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
    return nodes