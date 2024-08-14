#!/bin/bash

# Load config and virtualenv
source .env
if [ -z "${VIRTUAL_ENV}" ]; then
#  source venv/bin/activate;
  source venv/local/bin/activate;
fi

mkdir -p logs

# Start llamafiles
echo "Starting llamafile servers..."

if [[ "$1" == "e" ]]; then
  "models/embedding_model.llamafile" \
  --server \
  --nobrowser \
  --port "${EMBEDDING_MODEL_PORT}" > logs/embedding_model.log 2>&1 &
  pid=$!

  #"models/embedding_model.llamafile" \
  #--server \
  #--nobrowser \
  #--port "${EMBEDDING_MODEL_PORT}" \
  #-m models/exaone.gguf -ngl 9999 > logs/embedding_model.log 2>&1 &
  #pid=$!

  sleep 20
  err=$?
  if [ "${err}" -ne 0 ]; then
    echo "Failed to start embedding model llamafile"
    exit 1
  fi
  echo "${pid}" > .pid_embedding_model
  echo "started embedding model"

  while true; do echo $(date -u) >> out.txt; sleep 5; done
else
  "models/generation_model.llamafile" \
  --server \
  --nobrowser \
  --port "${GENERATION_MODEL_PORT}" > logs/generation_model.log 2>&1 &
  pid=$!
  sleep 20
  err=$?
  if [ "${err}" -ne 0 ]; then
    echo "Failed to start generation model llamafile"
    exit 1
  fi
  echo "${pid}" > .pid_generation_model
  echo "started generation model"

  # Run RAG app
#  python app.py "$@"

  while true; do echo $(date -u) >> out.txt; sleep 5; done
fi

## Shut down the llamafiles
kill "$(cat .pid_embedding_model)"
kill "$(cat .pid_generation_model)"

echo "exited."
