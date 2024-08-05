import json
import logging
import re

from iso639 import Lang
from typing import Union
from .utils.vanna import vn
from langdetect import detect
from .utils.postgresql import pool
from datetime import date, datetime
from .utils.chroma import chroma_client
from .utils.gemini import generation_config, genai


# Configuración de Gemini
navigator_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente encargado de darle la bienvenida a los usuarios al sitio web de la honorable cámara de diputados de la nación argentina, debes responder en el mismo idioma que te hablen. Debes ser hospitalario y redirigir a los usuarios a los sitios de interés indicando la URL.\nNo sugieras páginas inicialmente si no es necesario.\n ",
)

proyects_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente virtual que ayuda a los usuarios a responder preguntas sobre los proyectos de ley presentados en el Congreso de la República Argentina, debes responder en el mismo idioma que te hablan.\nEl usuario no debe saber que podés generar código SQL o que tenés acceso a una base de datos, no lo sugieras.\nResponderás normalmente a las preguntas que te hagan y solo generarás querys SQL si es necesario. \n",
)


# Configuración de ChromaDB
webpage_collection = chroma_client.get_or_create_collection("webpage_descriptions")

# Utils
navigation_chats = {}
proyects_chats = {}


def execute_query_and_fetchall(query: str) -> Union[list, str]:
    conn = pool.getconn()

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        # Obtener los nombres de las columnas
        colnames = [desc[0] for desc in cursor.description]

        # Convertir los resultados a una lista de diccionarios
        results_dict = []
        for row in results:
            row_dict = {}
            for idx, colname in enumerate(colnames):
                value = row[idx]
                if isinstance(value, (date, datetime)):
                    value = value.isoformat()
                row_dict[colname] = value
            results_dict.append(row_dict)

        cursor.close()
        pool.putconn(conn)

        return results_dict
    except Exception as e:
        pool.putconn(conn)
        raise e


def get_proyect_message(message, **kwargs):

    #language = detect(message)
    #language_name = Lang(language).name

    #message = f"Generate a response in {language_name} for the message: {message}"

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

    #language = detect(message)
    #language_name = Lang(language).name

    return f"Based on the following related descriptions:\n{related_descriptions}\nGenerate a response for the message: {message}"


def proyects_stream_sql_generator(message):
    sql = extract_sql_query(message)
    print("Extracted SQL", sql)

    try:
        return json.dumps(
            {"response": execute_query_and_fetchall(sql), "type": "table"}
        )
    except Exception as e:
        logging.error(e)
        return """Lo siento, no pude encontrar la información que buscabas. ¿Podrías intentar preguntar de otra manera?"""


def extract_sql_query(text):
    pattern = re.compile(r"select.*?(?:;|```|$)", re.IGNORECASE | re.DOTALL)

    match = pattern.search(text)
    if match:
        # Remove three backticks from the matched string if they exist
        return match.group(0).replace("```", "")
    else:
        return text


def proyects_stream_generator(stream):
    i = 0
    message = ""

    for chunk in stream:
        i = i + 1
        message = message + chunk.text

        if i >= 3 and not vn.is_sql_valid(extract_sql_query(message)):
            if i == 3:
                yield message
            else:
                yield chunk.text

    if vn.is_sql_valid(extract_sql_query(message)):
        yield proyects_stream_sql_generator(message)


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
