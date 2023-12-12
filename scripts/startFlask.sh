#!/bin/bash

cd ./backend
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

sudo python main.py production
