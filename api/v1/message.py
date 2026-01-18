from fastapi import APIRouter
from models import LLMInputModel

router = APIRouter(
    prefix="/v1",
)

@router.post("/messages")
def post_messages(llm: LLMInputModel):

    return llm.send_message()