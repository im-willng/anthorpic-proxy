from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1 import message
from api.admin import proxies, web
import uvicorn
from pathlib import Path

app = FastAPI(title="Anthropic Proxy")

# Include routers
app.include_router(message.router)
app.include_router(proxies.router)
app.include_router(web.router)

# Serve static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "proxy:app",
        host="127.0.0.1",
        port=8082,
        reload=True,
    )
