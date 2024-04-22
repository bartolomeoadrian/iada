FROM python:3.12

WORKDIR /api

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache \
	pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
