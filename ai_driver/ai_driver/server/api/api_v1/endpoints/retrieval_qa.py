"""
This module defines API endpoints related to vector store retrieval and querying
"""
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_driver.local_llm.ggml_pipeline import local_llm_qa_pipeline
from ai_driver.server import schemas
from ai_driver.server.api import deps
from ai_driver.server.schemas import User
from ai_driver.vector_storage.local_download_pipeline import local_download_pipeline
from ai_driver.cloud_llm.cloud_qa import pinecone_qa_pipeline
from ai_driver.config import server_config
from ai_driver.local_llm.ggml_config import get_default_ggml_config
from ai_driver.retrieval.qa_config import get_default_qa_config

router = APIRouter()


@router.get("/local_download_pipline")
def local_endpoint(
    db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)
):
    local_download_pipeline(
        dir_path=server_config.DATA_PATH, embed_model=server_config.INSTRUCT_EMBED_MODEL
    )


@router.post("/pinecone", status_code=200, response_model=schemas.QABase)
def pinecone_endpoint(
    request: schemas.QARequest, user: User = Depends(deps.get_current_user)
):
    response = pinecone_qa_pipeline(request.query)
    result = schemas.QABase(query=request.query, result=response)
    logger.info(result)
    return result


@router.post("/local_llm", status_code=200, response_model=schemas.QABase)
def local_llm_endpoint(
    request: schemas.QARequest, user: User = Depends(deps.get_current_user)
):
    qa_config = get_default_qa_config()
    ggml_config = get_default_ggml_config()
    response = local_llm_qa_pipeline(
        request.query, device="cuda", qa_config=qa_config, ggml_config=ggml_config
    )
    result = schemas.QABase(query=request.query, result=response)
    logger.info(result)
    return result
