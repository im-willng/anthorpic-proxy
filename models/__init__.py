from pydantic import BaseModel

class Message(BaseModel):
    content: str
    role: str


# 
from typing import Union
from models.google_gemini.gen_message import GeminiProcess

LLMInputModel = Union[GeminiProcess]

