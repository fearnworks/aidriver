import textwrap
from dataclasses import dataclass

from loguru import logger
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate


@dataclass
class QADBConfig:
    db_path: str
    embed_model: str
    return_source: str
    vector_count: str


def wrap_text_preserve_newlines(text, width=110):
    lines = text.split("\n")
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = "\n".join(wrapped_lines)
    return wrapped_text


def qa_pipeline(query: str, retriever, model):
    template = """Answer the question based only on the following context:
        {context}

        Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke(query)
    return response
