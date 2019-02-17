#!/bin/bash -euxo pipefail

export FLASK_APP=main.py
export FLASK_ENV=development

echo "Starting Server"
flask run --host=0.0.0.0
