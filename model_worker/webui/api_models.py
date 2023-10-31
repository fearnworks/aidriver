from dataclasses import dataclass, field
from typing import List, Optional
from loguru import logger 
@dataclass
class ModelPermission:
    id: str
    object: str
    created: int
    allow_create_engine: bool
    allow_sampling: bool
    allow_logprobs: bool
    allow_search_indices: bool
    allow_view: bool
    allow_fine_tuning: bool
    organization: str
    group: Optional[str]
    is_blocking: bool

@dataclass
class Model:
    id: str
    object: str
    created: int
    owned_by: str
    root: str
    parent: Optional[str]
    permission: List[ModelPermission]

@dataclass
class ModelListResponse:
    object: str
    data: List[Model]
    
import httpx
import json
from typing import List

async def get_models():
    url = "http://localhost:8100/v1/models"
    headers = {"accept": "application/json"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=60.0)
            response.raise_for_status()  # Check if the request was successful

        if response.status_code == 200:
            model_list_response = ModelListResponse(**json.loads(response.text))
            return model_list_response

    except httpx.HTTPError as e:
        logger.info(f"An error occurred while making the request: {e}")
        return None

