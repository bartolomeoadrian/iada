FROM python:3.12

WORKDIR /api

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache \
	pip install -r requirements.txt

COPY . .

RUN python -c "import chromadb;client = chromadb.Client();collection = client.create_collection('all-my-documents');collection.add(documents=['This is document1'], ids=['doc1']);results = collection.query(query_texts=['This is a query document'],n_results=1)"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
