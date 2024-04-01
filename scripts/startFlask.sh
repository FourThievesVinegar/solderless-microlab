#!/bin/bash

cd ./backend
python3 -m venv env
source env/bin/activate
sudo pip3 install -r requirements.txt

sudo python3 main.py production
