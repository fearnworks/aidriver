import os
from loguru import logger
from langsmith import Client as LangsmithClient

LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")


def get_client():
    """Default client for langchain"""
    LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2")
    if LANGCHAIN_TRACING_V2:
        return LangsmithClient(api_url=LANGCHAIN_ENDPOINT, api_key=LANGCHAIN_API_KEY)
    else:
        logger.info("Langsmith disabled")
        return None
