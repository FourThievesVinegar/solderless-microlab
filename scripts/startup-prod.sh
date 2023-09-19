#!/bin/bash
# TODO: Update this to use env vars for users locations.
# Probably this is reduntant and wants to call the other scripts

cd ../backend && \
	virtualenv -p python3 --system-site-packages env && source env/bin/activate && \
	pip install -r requirements.txt && \
	export FLASK_APP=main.py && \
	export FLASK_ENV=production && \
	export FLASK_DEBUG=0 && \
	python main.py production &

cd ../backend && \
	source env/bin/activate && \
	celery -A recipes worker --loglevel=INFO &

# If there is no build directory, then build the GUI. 
if [ ! -d "../gui/build" ]
then
	cd ../gui && yarn build
fi

# Start the GUI in serve mode, which is more performant than 'yarn start' dev mode
cd ../gui && serve -s build &

# Start a Browser going to localhost:3000
xdg-open http://localhost:3000
