FROM python:3.12

USER root

# Install required dependencies
RUN apt-get update && apt-get install -y \
	nginx \
	nodejs \
	npm \
	supervisor

# Build the frontend
WORKDIR /opt/iada/frontend

ADD ./src/frontend/package.json .
ADD ./src/frontend/package-lock.json .

RUN npm ci

ADD ./src/frontend .

RUN npm run build \
	&& mkdir -p /var/www/html/chat \
	&& cp -r ./dist/* /var/www/html/chat

# Install the backend
WORKDIR /opt/iada/backend

ADD ./src/backend/requirements.txt .

RUN python3 -m pip install -v -r requirements.txt \
	&& python3 -c "import chromadb;client = chromadb.Client();collection = client.create_collection('all-my-documents');collection.add(documents=['This is document1'], ids=['doc1']);results = collection.query(query_texts=['This is a query document'],n_results=1)"

COPY . .

# Configurattion
WORKDIR /opt/iada

ADD ./config/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD ./config/nginx/nginx.conf /etc/nginx/nginx.conf
ADD ./storage/www /var/www/html

EXPOSE 80

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
