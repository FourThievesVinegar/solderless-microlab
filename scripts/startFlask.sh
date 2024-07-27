#!/bin/bash

cd ./backend
python3 -m venv env
source env/bin/activate
# We only need to install the packages the first time
# sudo pip3 install -r requirements.txt

sudo python3 main.py production
