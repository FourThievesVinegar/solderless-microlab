#!/bin/bash

cd ./backend
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

sudo python main.py production
