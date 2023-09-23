"""
This module creates an API router for the FastAPI application and includes routes from the auth module.
"""

from ai_driver.server.api.api_v1.endpoints import auth, chat, image, retrieval_qa
from fastapi import APIRouter

api_router = APIRouter()
"""
An instance of APIRouter to which we will include the routes from the auth module.
"""

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
"""
Includes the routes defined in the auth module under the prefix "/auth".
The routes from the auth module will be categorized under the tag "auth" in the API documentation.
"""

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
"""
Includes the routes defined in the chat module under the prefix "/chat".
"""

api_router.include_router(image.router, prefix="/image", tags=["image"])
"""
Includes the routes defined in the image module under the prefix "/image".
"""

api_router.include_router(retrieval_qa.router, prefix="/retrieval", tags=["retrieval"])
"""
Includes the routes defined in the retrieval module under the prefix "/retrieval".
"""
