from pydantic import BaseModel


class QABase(BaseModel):
    """
    A base model for chat responses that includes the common attributes.
    """

    query: str
    result: str


class QARequest(BaseModel):
    query: str
