FROM nginx:1.27.0-alpine

USER root

# Install supervisor
RUN apk add supervisor
ADD ./config/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install nodejs and npm
RUN apk add nodejs npm

# Install dependencies required for compiling Python
RUN apk add --no-cache build-base libffi-dev openssl-dev bzip2-dev zlib-dev xz-dev sqlite-dev

# Download Python 3.11 source
RUN wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz

# Extract the source code
RUN tar -xzf Python-3.11.0.tgz

# Compile and install Python 3.11
WORKDIR /Python-3.11.0
RUN ./configure --enable-optimizations
RUN make
RUN make altinstall

# Set the path to include the newly installed Python version
ENV PATH="/usr/local/bin:$PATH"

# Verify Python version
RUN python3.11 --version

# Install python package manager
RUN apk add py3-pip

# Build the frontend
WORKDIR /opt/iada/frontend

ADD ./src/frontend/package.json .
ADD ./src/frontend/package-lock.json .

RUN npm ci

ADD ./src/frontend .

RUN npm run build
RUN mkdir -p /var/www/html/chat
RUN cp -r ./dist/* /var/www/html/chat

# Install the backend
WORKDIR /opt/iada/backend

RUN python3.11 -m venv ./.venv

ENV PATH="/opt/iada/backend/.venv/bin:$PATH"

ADD ./src/backend/requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
	pip install -v -r requirements.txt

COPY . .

RUN python3.11 -c "import chromadb;client = chromadb.Client();collection = client.create_collection('all-my-documents');collection.add(documents=['This is document1'], ids=['doc1']);results = collection.query(query_texts=['This is a query document'],n_results=1)"

# Configurattion
WORKDIR /opt/iada

ADD ./config/nginx/nginx.conf /etc/nginx/nginx.conf
ADD ./storage/www /var/www/html

EXPOSE 80

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
