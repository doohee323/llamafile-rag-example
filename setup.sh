#!/bin/bash

# Create virtualenv
if [ ! -d "venv" ]; then
  # curl https://pyenv.run | bash
  # pyenv install --list |grep 3.1      pyenv install 3.11.0
#  pyenv local 3.11.0
#  python3 -m venv venv
#  source venv/bin/activate

  # pip3 install virtualenv
  virtualenv venv --python=python3.10
  source venv/local/bin/activate

  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
fi

# Create .env to store app settings (see also settings.py)
if [ ! -f ".env" ]; then cp -v .env.example .env; fi

#
# Download llamafiles then symlink them to
# - models/embedding_model.llamafile
# - models/generation_model.llamafile
#
# https://github.com/Mozilla-Ocho/llamafile
EMBEDDING_MODEL_URL="https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-llamafile/resolve/main/Meta-Llama-3.1-8B.Q6_K.llamafile"
GENERATION_MODEL_URL="https://huggingface.co/Mozilla/Meta-Llama-3-8B-Instruct-llamafile/resolve/main/Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile"
#GENERATION_MODEL_URL="https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-Instruct-llamafile/resolve/main/Meta-Llama-3.1-8B-Instruct.Q6_K.llamafile"

function url_to_filename() {
  url=$1
  filename="${url##*/}"
  echo "${filename}"
}

mkdir -pv models
cd models # || exit

if [ ! -f "embedding_model.llamafile" ]
then
  # Download and symlink embedding model
  filename="$(url_to_filename "${EMBEDDING_MODEL_URL}")"
  curl -L -o "${filename}" "${EMBEDDING_MODEL_URL}"
  chmod +x "${filename}"
  rm -Rf embedding_model.llamafile
  ln -s "${filename}" embedding_model.llamafile
fi

if [ ! -f "generation_model.llamafile" ]
then
  # Download and symlink generation model
  filename="$(url_to_filename "${GENERATION_MODEL_URL}")"
  curl -o "${filename}" "${GENERATION_MODEL_URL}" -L
  chmod +x "${filename}"
  rm -Rf generation_model.llamafile
  ln -s "${filename}" generation_model.llamafile
fi

cd - || exit