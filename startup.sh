#!/bin/bash
# TODO: Update this to use env vars for users locations.

# This file has been left in place but is superseded by startup-dev.sh and startup-prod.sh
# Use:
#	./startup.sh dev
#		Start a development server

environment=$1;
if ! [ -z "$environment" ]
then
	echo "Starting the Microlab in $environment mode";
fi

if ! [[ "$environment" =~ ^(dev|prod)$ ]]
then
	echo "The options are \"dev\" and \"prod\" so you are getting dev mode, you silly goose!";
fi

if [[ "$environment" == "prod" ]] 
then
	cd ./scripts/ && ./startup-prod.sh
else
	cd ./scripts/ && ./startup-dev.sh
fi
