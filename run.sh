#! /bin/bash

source activate backend
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development

flask run
