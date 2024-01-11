#!/bin/bash

cd ./backend
virtualenv -p python3 --system-site-packages env
source env/bin/activate
pip install -r requirements.txt

sudo python main.py production
