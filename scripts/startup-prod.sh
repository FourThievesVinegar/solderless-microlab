#!/bin/bash
#TODO: Update this to use env vars for users locations.

cd ../backend && \
	virtualenv -p python3 --system-site-packages env && source env/bin/activate && \
	pip install -r requirements.txt && \
	export FLASK_APP=main.py && \
	export FLASK_ENV=production && \
	export FLASK_DEBUG=0 && \
	python main.py &

cd ../backend && \
	source env/bin/activate && \
	celery -A recipes worker --loglevel=INFO &

# TODO: This should run a pre-built version
cd ../gui && yarn start
