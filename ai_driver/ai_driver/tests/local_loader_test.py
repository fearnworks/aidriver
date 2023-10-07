from ai_driver.vector_storage.local_loader import load, split
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader, UnstructuredMarkdownLoader
import pytest
import os
import shutil


@pytest.fixture
def chunks():
    return load(os.path.join(os.path.dirname(__file__), "test_data"), "*.pdf", loader=PyPDFLoader)


def test_should_return_empty_list_for_empty_directory():
    empty_dir = os.path.join(os.path.dirname(__file__), "test_data", "empty_dir")
    os.makedirs(empty_dir, exist_ok=True)
    assert load(empty_dir, "*.pdf", loader=PyPDFLoader) == []
    shutil.rmtree(empty_dir)


def test_should_return_empty_list_for_no_matching_files():
    assert load(os.path.join(os.path.dirname(__file__), "test_data"), "*.txt", loader=TextLoader) == []


def test_should_return_chunks_from_matching_files():
    assert (
        len(load(os.path.join(os.path.dirname(__file__), "test_data"), "*.pdf", loader=PyPDFLoader)) == 115
    )


def test_should_split_chunks_by_size_and_overlap(chunks):
    chunk_size = 342
    chunk_overlap = 200

    texts = split(chunks, chunk_size, chunk_overlap)

    ### assert that chunks are not larger than expected
    for doc in texts:
        assert len(doc.page_content) <= chunk_size
