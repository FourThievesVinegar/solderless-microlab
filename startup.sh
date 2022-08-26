#!/bin/bash
#TODO: Update this to use env vars for users locations.


cd ./backend && \
	virtualenv -p python3 env && source env/bin/activate && \
	pip install -r requirements.txt && \
	export FLASK_APP=main.py && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=0 && \
	python main.py &

cd ./backend && \
	source env/bin/activate && \
	celery -A recipes worker --loglevel=INFO &

cd ./gui && yarn start
