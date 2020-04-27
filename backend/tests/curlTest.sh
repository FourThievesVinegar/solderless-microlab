#!/bin/bash

curl http://localhost:5000/stop
curl http://localhost:5000/start/boilegg
curl http://localhost:5000/select/option/Done
curl http://localhost:5000/select/option/Done
curl http://localhost:5000/status
sleep 2
curl http://localhost:5000/status
