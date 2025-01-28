#!/bin/bash

if [[ $DEBUG ]]; then
    uvicorn src.application:application --port 2121 --reload
else
    uvicorn src.application:application --port 2121 
fi