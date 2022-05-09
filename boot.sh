#!/bin/bash
#TODO: Update this to use env vars for users locations.


cd /home/ubuntu/workspace/solderless-microlab/backend && \
	virtualenv -p python3 env && source env/bin/activate && \
	pip install -r requirements.txt && \
	export FLASK_APP=main.py && \
	export FLASK_ENV=development && \
	export FLASK_DEBUG=0 && \
	python main.py &
cd /home/ubuntu/workspace/solderless-microlab/gui && yarn start
