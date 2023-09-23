"""
This module defines API endpoints related to chat such as fetching, creating, and updating chat sessions
"""
from loguru import logger
from fastapi import APIRouter, Depends

from ai_driver.cloud_llm.cloud_chat_agent import (
    CloudChatAgent,
    CloudChatGenerationConfig,
)
from ai_driver.server import schemas
from ai_driver.server.crud import sessions as crud_sessions
from ai_driver.server.api import deps
from ai_driver.config import server_config
from ai_driver.server.redis import redis_client


router = APIRouter()


@router.post("/cloudllm", status_code=200, response_model=schemas.ChatBase)
def cloud_llm_endpoint(
    request: schemas.ChatRequest, user: schemas.User = Depends(deps.get_current_user)
):
    # Fetch chat history from Redis
    logger.info(request)
    config = CloudChatGenerationConfig(
        max_new_tokens=request.max_tokens, temperature=request.temperature
    )
    try:
        chat_history = crud_sessions.get_history(request.session_id, user.email)
    except Exception as err:
        logger.error(f"Error fetching chat history: {err}", exc_info=True)
        raise Exception("Error fetching chat history")

    logger.info(chat_history)
    agent = CloudChatAgent(
        history=[pair for pair in chat_history.history], config=config
    )
    response = agent.get_completion(request.query)
    result = response["result"]

    if isinstance(result, str):
        # Update the chat history
        new_chat_pair = schemas.ChatPair(human=request.query, ai=result)
        chat_history.history.append(new_chat_pair)
    else:
        # Handle unexpected response type if necessary
        logger.warning(f"Unexpected response type: {type(result)}")

    # Save new response in Redis
    redis_client.rpush(f"chathistory:{request.session_id}", new_chat_pair.json())
    response_model = schemas.ChatBase(
        query=request.query,
        result=result,
        session_id=request.session_id,
        user_id=user.id,
    )
    logger.info(response_model)
    return response_model


@router.post("/history", status_code=200, response_model=schemas.ChatHistory)
def get_chat_history(
    request: schemas.ChatHistoryRequest,
    user: schemas.User = Depends(deps.get_current_user),
):
    # Fetch chat history from Redis using the session_id
    chat_history = crud_sessions.get_history(request.session_id, user.email)
    logger.info(chat_history)
    return chat_history


@router.post("/sessions", status_code=200)
def get_chat_sessions(user: schemas.User = Depends(deps.get_current_user)):
    sessions = crud_sessions.get_sessions(user.email)
    logger.info(f"Got session list for user {user.email} : {sessions}")
    return sessions
