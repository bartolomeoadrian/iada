import logging
from src.ai import vn
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/chat")
def chat(message: Union[str, None] = None):
    type = "text"
    response = vn.generate_sql(message or "")

    if vn.is_sql_valid(response):
        try:
            df = vn.run_sql(response)

            type = "table"
            response = df.to_dict(orient="records")
        except Exception as e:
            logging.error(e)
            type = "text"
            response = """Lo siento, no pude encontrar la información que buscas. ¿Podrías intentar preguntar de otra manera?"""

    return {"response": response, "type": type}
