import json
import logging

from typing import Union
from .utils.vanna import vn
from .utils.postgresql import pool
from .utils.chroma import chroma_client
from .utils.gemini import generation_config, genai


# Configuración de Gemini
navigator_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente encargado de darle la bienvenida a los usuarios al sitio web de la honorable cámara de diputados de la nación argentina. Debes ser hospitalario y redirigir a los usuarios a los sitios de interés.\nNo sugieras páginas inicialmente si no es necesario.\nEstas son las páginas con las que trabajaras por ahora:\nhttps://hcdn.gob.ar : Es la página principal y contiene noticias y actividades ademas de botones de interés\nhttps://hcdn.gob.ar/proyectos/ : Esta página contiene toda la información referida a proyectos de ley de la república argentina, asi como tambien Boletín de Asuntos Tratados, Trámite Parlamentario, Boletín de Asuntos Entrados",
)

proyects_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente virtual que ayuda a los usuarios a responder preguntas sobre los proyectos de ley presentados en el Congreso de la República Argentina.\nEl usuario no debe saber que podés generar código SQL o que tenés acceso a una base de datos, no lo sugieras.\nSolo responderas con código SQL o ayudarás al usuario con sus dudas",
)


# Configuración de ChromaDB
webpage_collection = chroma_client.get_or_create_collection("webpage_descriptions")

# Utils
navigation_chats = {}
proyects_chats = {}


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


def get_proyect_message(message, **kwargs):
    return vn.get_sql_prompt(
        initial_prompt=""" """,
        question=message,
        question_sql_list=vn.get_similar_question_sql(message, **kwargs),
        ddl_list=vn.get_related_ddl(message, **kwargs),
        doc_list=vn.get_related_documentation(message, **kwargs),
        **kwargs,
    )


def get_navigator_message(message):
    results = webpage_collection.query(query_texts=[message], n_results=5)

    related_descriptions = []

    for i in range(len(results["documents"])):
        related_descriptions.append(
            {
                "id": results["ids"][i],
                "description": results["documents"][i],
            }
        )

    return f"Based on the following related descriptions:\n{related_descriptions}\nGenerate a response for the message: {message}"


def proyects_stream_sql_generator(first_chunk, stream):
    query = first_chunk["message"]["content"]
    for chunk in stream:
        query += chunk["message"]["content"]

    try:
        return json.dumps(
            {"response": execute_query_and_fetchall(query), "type": "table"}
        )
    except Exception as e:
        logging.error(e)
        return """I'm sorry, I couldn't find the information you requested. Please try again."""


def proyects_stream_generator(stream):
    first_chunk = next(stream)
    first_message = first_chunk.text
    sql = vn.extract_sql_query(first_message)
    is_sql = vn.is_sql_valid(sql)

    if is_sql:
        yield proyects_stream_sql_generator(first_chunk, stream)
    else:
        message = first_message
        yield first_message
        for chunk in stream:
            message = message + chunk.text
            yield chunk.text


def navigator_stream_generator(stream):
    for chunk in stream:
        yield chunk.text


def ask_proyects(chat_id, message):
    if chat_id not in proyects_chats:
        proyects_chats[chat_id] = proyects_model.start_chat()

    chat: genai.ChatSession = proyects_chats[chat_id]
    stream = chat.send_message(get_proyect_message(message), stream=True)

    return stream


def ask_navigator(chat_id, message):
    if chat_id not in navigation_chats:
        navigation_chats[chat_id] = navigator_model.start_chat()

    chat: genai.ChatSession = navigation_chats[chat_id]
    stream = chat.send_message(get_navigator_message(message), stream=True)

    return stream
