from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
from pathlib import Path

from app.agent import agent_executor
from app.database import engine, SessionLocal
from app.models import Base, Message

# Create tables (safe to call multiple times)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "ui"

# Serve frontend
app.mount("/chat-ui", StaticFiles(directory=UI_DIR), name="chat-ui")


@app.get("/chat-ui")
def chat_ui():
    return FileResponse(UI_DIR / "index.html")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    session_id = "default"

    db = SessionLocal()
    db.add(Message(session_id=session_id, role="user", content=req.message))
    db.commit()

    result = agent_executor.invoke({"input": req.message})
    output = result.get("output") if isinstance(result, dict) else result

    if isinstance(output, list) and output and isinstance(output[0], dict):
        reply_text = json.dumps(output, indent=2)
    elif isinstance(output, dict):
        reply_text = json.dumps(output, indent=2)
    else:
        reply_text = str(output)

    db.add(Message(
        session_id=session_id,
        role="agent",
        content=reply_text
    ))
    db.commit()
    db.close()

    return {"reply": reply_text}


@app.get("/")
def root():
    return {"status": "Library Desk Agent running"}

