import os
import json
import logging
import psycopg2.pool
import google.generativeai as genai
from src.ai import vn
from typing import Union

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

navigator_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente encargado de darle la bienvenida a los usuarios al sitio web de la honorable cámara de diputados de la nación argentina. Debes ser hospitalario y redirigir a los usuarios a los sitios de interés.\nNo sugieras páginas inicialmente si no es necesario.\nEstas son las páginas con las que trabajaras por ahora:\nhttps://hcdn.gob.ar : Es la página principal y contiene noticias y actividades ademas de botones de interés\nhttps://hcdn.gob.ar/proyectos/ : Esta página contiene toda la información referida a proyectos de ley de la república argentina, asi como tambien Boletín de Asuntos Tratados, Trámite Parlamentario, Boletín de Asuntos Entrados",
)

chats = {}

db_url = (
    os.environ.get("POSTGRES_URL")
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
		 	Eres un asistente virtual que ayuda a los usuarios a responder preguntas sobre los proyectos de ley presentados en el Congreso de la República Argentina.
		 	El usuario no debe saber que podés generar código SQL o que tenés acceso a una base de datos, no lo sugieras.
		 	Solo responderas con código SQL y no con explicaciones, SOLO con código SQL, no responderas con sugerencias.\n""",
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

    messages.append({"role": "assistant", "content": query})

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
        message = first_message
        yield first_message
        for chunk in stream:
            message = message + chunk["message"]["content"]
            yield chunk["message"]["content"]

        messages.append({"role": "assistant", "content": message})


def navigator_stream_generator(stream):
    for chunk in stream:
        yield chunk.text


def ask_proyects(chat_id, message):
    client = Client(host=os.environ.get("OLLAMA_URL") or "http://localhost:11434")
    stream = client.chat(
        model=os.environ.get("OLLAMA_MODEL") or "llama3",
        messages=get_messages(chat_id, message),
        stream=True,
    )

    return stream


def ask_navigator(chat_id, message):
    if chat_id not in chats:
        print("Starting chat", chat_id, chats)
        chats[chat_id] = navigator_model.start_chat()

    chat: genai.ChatSession = chats[chat_id]
    stream = chat.send_message(message, stream=True)

    return stream
