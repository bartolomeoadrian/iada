#!/bin/sh

ollama serve &

sleep 5

curl -X POST http://localhost:11434/api/pull -d '{"name": "llama3"}'

sleep 10

tail -f /dev/null
