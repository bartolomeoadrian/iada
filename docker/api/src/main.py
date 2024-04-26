import logging
import ollama
import json
from src.ai import vn
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []


def get_messages(message, **kwargs):
    global messages

    prompt = vn.get_sql_prompt(
        initial_prompt=(
            vn.config.get("initial_prompt", None) if vn.config is not None else None
        ),
        question=message,
        question_sql_list=vn.get_similar_question_sql(message, **kwargs),
        ddl_list=vn.get_related_ddl(message, **kwargs),
        doc_list=vn.get_related_documentation(message, **kwargs),
        **kwargs,
    )

    messages = messages + prompt

    return messages


def stream_sql_generator(first_chunk, stream):
    query = first_chunk["message"]["content"]
    for chunk in stream:
        query += chunk["message"]["content"]

    try:
        df = vn.run_sql(query)
        return json.dumps({"response": df.to_dict(orient="records"), "type": "table"})
    except Exception as e:
        logging.error(e)
        return """Lo siento, no pude encontrar la información que buscas. ¿Podrías intentar preguntar de otra manera?"""


def stream_generator(stream):
    first_chunk = next(stream)
    sql = vn.extract_sql_query(first_chunk["message"]["content"])
    is_sql = vn.is_sql_valid(sql)

    if is_sql:
        yield stream_sql_generator(first_chunk, stream)
    else:
        yield first_chunk["message"]["content"]
        for chunk in stream:
            yield chunk["message"]["content"]


@app.get("/api/chat")
async def chat(message: Union[str, None] = None):
    stream = ollama.chat(
        model="llama3",
        messages=get_messages(message or ""),
        stream=True,
    )

    return StreamingResponse(stream_generator(stream), media_type="text/event-stream")
