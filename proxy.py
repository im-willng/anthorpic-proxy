from fastapi import FastAPI
from api.v1 import message

import uvicorn


app = FastAPI()
app.include_router(message.router)

if __name__ == "__main__":
    uvicorn.run(
        "proxy:app",
        host="127.0.0.1",
        port=8082,
        reload=True,
    )