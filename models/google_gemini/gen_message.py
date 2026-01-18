from openai import OpenAI
from pydantic import BaseModel
from models import Message

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class GeminiProcess(BaseModel):

    max_tokens: int
    messages: list[Message]
    model: str

    def send_message(self):

        req_data = client.chat.completions.create(
            model=os.getenv("GOOGLE_MODEL"),
            messages=[msg.model_dump() for msg in self.messages],
            max_tokens=self.max_tokens
        )

        response_data = {
            "id": req_data.id,
            "content": [
                {
                    "citations": [{
                        "cited_text": "cited_text",
                        "document_index": 0,
                        "document_title": "document_title",
                        "end_char_index": 0,
                        "file_id": "file_id",
                        "start_char_index": 0,
                        "type": "char_location"
                    }],
                    "text": req_data.choices[0].message.content,
                    "type": "text"
                }],
                "model": self.model,
                "role": req_data.choices[0].message.role,
                "stop_reason": req_data.choices[0].finish_reason,
                "stop_sequence": None,
                "type": "message",
                "usage": {
                    "cache_creation": {
                        "ephemeral_1h_input_tokens": 0,
                        "ephemeral_5m_input_tokens": 0
                    },
                    "cache_creation_input_tokens": 2051,
                    "cache_read_input_tokens": 2051,
                    "input_tokens": req_data.usage.prompt_tokens,
                    "output_tokens": req_data.usage.completion_tokens,
                    "server_tool_use": {
                        "web_search_requests": 0
                    },
                    "service_tier": "standard"
                }
            }
        
        return response_data