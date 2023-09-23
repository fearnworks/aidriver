"""
This module defines API endpoints related to chat such as fetching, creating, and updating chat sessions
"""
from loguru import logger

from ai_driver.server import schemas
from ai_driver.server.redis import redis_client
from typing import List
import time
import json


def get_sessions(user_id: str, store=redis_client) -> List[str]:
    session_list = store.zrange(f"session_list:{user_id}", 0, -1)
    logger.info(f"Got session list for user {user_id}")
    logger.info(session_list)
    return session_list


def set_sessions(user_id: str, session_id: str, store=redis_client):
    # session_list = store.lpush(f"session_list:{user_id}", session_id)
    session_list = store.zadd(f"session_list:{user_id}", {session_id: time.time()})
    logger.info(f"Added session {session_id} to user {user_id}")
    return session_list


def remove_sessions(user_id: str, session_id: str, store=redis_client):
    session_list = store.zrem(f"session_list:{user_id}", session_id)
    logger.info(f"Removed session {session_id} from user {user_id}")
    return session_list


def get_history(session_id: str, user_id: str, store=redis_client):
    logger.info(f"Checking store for session {session_id}")
    session_list = get_sessions(user_id, store)
    if session_id not in session_list:
        logger.info(f"New Session: {session_id}")
        set_sessions(user_id, session_id, store)
        chat_history = schemas.ChatHistory(
            history=[], session_id=session_id, user_id=user_id
        )
        return chat_history
    else:
        logger.info(f"Existing Session: {session_id}")
        store_list = store.lrange(f"chathistory:{session_id}", 0, -1)
        logger.info(store_list)
        try:
            serialized_chat = []
            for str_val in store_list:
                val = json.loads(str_val)
                logger.info(val)
                chat_pair = schemas.ChatPair.parse_obj(val)
                serialized_chat.append(chat_pair)
            logger.info(serialized_chat)
            chat_history = schemas.ChatHistory(
                history=serialized_chat, session_id=session_id, user_id=user_id
            )
            return chat_history
        except Exception as err:
            logger.error(f"Error deserializing chat history: {err}")
            raise Exception("Error deserializing chat history")
