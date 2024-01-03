#!/bin/bash
#TODO: Update this to use env vars for users locations.
# Probably this is reduntant and wants to call the other scripts

cd ../backend && \
	virtualenv -p python3 --system-site-packages env && source env/bin/activate && \
	pip install -r requirements.txt && \
	export FLASK_APP=main.py && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=0 && \
	python main.py development &

cd ../gui && yarn start
