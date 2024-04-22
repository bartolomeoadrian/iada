FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# RUN ollama pull llama3

ENTRYPOINT ["/usr/local/bin/ollama"]

CMD [ "serve" ]
