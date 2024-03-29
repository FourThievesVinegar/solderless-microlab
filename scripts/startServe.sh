#!/bin/bash
# If there is no build directory, then build the GUI. 
if [ ! -d "./gui/build" ]
then
	cd ./gui && yarn build
fi

# Start the GUI in serve mode, which is more performant than 'yarn start' dev mode
cd ./gui && serve -s build &
