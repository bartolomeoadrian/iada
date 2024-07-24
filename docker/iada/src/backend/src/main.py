from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .utils import ask, stream_generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/chat/proyects")
async def proyects(chat_id: str, message: str):
    stream = ask(chat_id, message)
    return StreamingResponse(stream_generator(stream), media_type="text/event-stream")


@app.get("/api/chat/navigator")
async def navigator(chat_id: str, message: str):
    stream = ask(chat_id, message)
    return StreamingResponse(stream_generator(stream), media_type="text/event-stream")
