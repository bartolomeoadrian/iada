FROM ollama/ollama:latest as ollama

ENTRYPOINT [ "/bin/ollama" ]

CMD [ "serve" ]
