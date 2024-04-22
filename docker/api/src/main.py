import logging
from src.ai import vn
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/chat")
def chat(message: Union[str, None] = None):
    auto_train = False

    response = vn.generate_sql(message or "")
    is_sql = vn.is_sql_valid(response)

    if is_sql:
        try:
            df = vn.run_sql(response)
            response = df.to_dict(orient="records")

            if len(df) > 0 and auto_train:
                vn.add_question_sql(question=message, sql=response)

        except Exception as e:
            logging.error(e)
            response = """Lo siento, no pude encontrar la información que buscas. ¿Podrías intentar preguntar de otra manera?"""

    return {"response": response}
