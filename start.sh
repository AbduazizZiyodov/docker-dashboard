#!/bin/bash

. .env

if [[ $DEBUG ]]; then
    uvicorn server.application:application --port 2121 --reload
else
    uvicorn server.application:application --port 2121 
fi