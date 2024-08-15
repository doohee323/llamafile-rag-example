#!/usr/bin/env bash

set -x

export PATH="$PATH:/home/vagrant/.local/bin:."; echo $PATH

opentelemetry-bootstrap --action=install

opentelemetry-instrument python app/server.py

