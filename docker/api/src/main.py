import logging
import ollama
import async_timeout
import asyncio
from src.ai import vn
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

GENERATION_TIMEOUT_SEC = 60

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

    if vn.config is not None:
        initial_prompt = vn.config.get("initial_prompt", None)
    else:
        initial_prompt = None

    question_sql_list = vn.get_similar_question_sql(message, **kwargs)
    ddl_list = vn.get_related_ddl(message, **kwargs)
    doc_list = vn.get_related_documentation(message, **kwargs)

    prompt = vn.get_sql_prompt(
        initial_prompt=initial_prompt,
        question=message,
        question_sql_list=question_sql_list,
        ddl_list=ddl_list,
        doc_list=doc_list,
        **kwargs,
    )

    messages = messages + prompt

    print(messages)

    return messages


def stream_generator(stream):
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

    response = ""

    for chunk in stream:
        content = chunk["message"]["content"]
        response += content
        sql = vn.extract_sql_query(response)
        is_sql = vn.is_sql_valid(sql)

    return {"response": response}

    # type = "text"
    # response = vn.generate_sql(message or "")
    #
    # if vn.is_sql_valid(response):
    #    try:
    #        df = vn.run_sql(response)
    #
    #        type = "table"
    #        response = df.to_dict(orient="records")
    #    except Exception as e:
    #        logging.error(e)
    #        type = "text"
    #        response = """Lo siento, no pude encontrar la información que buscas. ¿Podrías intentar preguntar de otra manera?"""
    #
    # return {"response": response, "type": type}
