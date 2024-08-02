from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .utils import (
    ask_proyects,
    ask_navigator,
    proyects_stream_generator,
    navigator_stream_generator,
)

app = FastAPI(
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/chat/proyects")
async def proyects(chat_id: str, message: str):
    stream = ask_proyects(chat_id, message)
    return StreamingResponse(
        proyects_stream_generator(stream), media_type="text/event-stream"
    )


@app.get("/api/chat/navigator")
async def navigator(chat_id: str, message: str):
    stream = ask_navigator(chat_id, message)
    return StreamingResponse(
        navigator_stream_generator(stream), media_type="text/event-stream"
    )
