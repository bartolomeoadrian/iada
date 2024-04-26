import logging
import json
import psycopg2.pool
import os
from ollama import Client
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


db_url = (
    os.environ.get("DATABASE_URL")
    or "postgres://postgres:postgres@localhost:5432/postgres"
)

pool = psycopg2.pool.SimpleConnectionPool(
    2,
    3,
    database=db_url.split("/")[-1],
    host=db_url.split("@")[1].split(":")[0],
    user=db_url.split("://")[1].split(":")[0],
    password=db_url.split("://")[1].split(":")[1].split("@")[0],
    port=db_url.split("@")[1].split(":")[1].split("/")[0],
)


def execute_query_and_fetchall(query: str) -> Union[list, str]:
    try:
        conn = pool.getconn()

        cursor = conn.cursor()
        cursor.execute(query)

        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in cursor.fetchall()]

        pool.putconn(conn)
        return result
    except Exception as e:
        pool.putconn(conn)
        raise e


def get_messages(chat_id, message, **kwargs):
    global messages

    prompt = vn.get_sql_prompt(
        initial_prompt="""
			Sos un asistente virtual que ayuda a los usuarios a responder preguntas sobre los proyectos de ley presentados en el Congreso de la República Argentina.
			El usuario no debe saber que podés generar código SQL o que tenés acceso a una base de datos, no lo sugieras.
			El usuario podría preguntar algo que requiera un código SQL o no.
			Si la pregunta no requiere un código SQL, respondé normalmente.
			Si la pregunta requiere un código SQL, solo respondé con código SQL y no con explicaciones, SOLO con código SQL.\n""",
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
        return json.dumps(
            {"response": execute_query_and_fetchall(query), "type": "table"}
        )
    except Exception as e:
        logging.error(e)
        return """Lo siento, no pude encontrar la información que buscas. ¿Podrías intentar preguntar de otra manera?"""


def stream_generator(stream):
    first_chunk = next(stream)
    first_message = first_chunk["message"]["content"]
    sql = vn.extract_sql_query(first_message)
    is_sql = vn.is_sql_valid(sql)

    if is_sql:
        yield stream_sql_generator(first_chunk, stream)
    else:
        yield first_message
        for chunk in stream:
            yield chunk["message"]["content"]


def ask_ollama(chat_id, message):
    client = Client(host=os.environ.get("OLLAMA_URL") or "http://localhost:11434")
    stream = client.chat(
        model=os.environ.get("OLLAMA_MODEL") or "llama3",
        messages=get_messages(chat_id, message),
        stream=True,
    )

    return stream


@app.get("/api/chat")
async def chat(chat_id: str, message: str):
    stream = ask_ollama(chat_id, message)
    return StreamingResponse(stream_generator(stream), media_type="text/event-stream")
