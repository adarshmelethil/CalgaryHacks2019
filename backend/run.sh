#!/bin/bash -euxo pipefail

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0
