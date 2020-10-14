#!/bin/bash

# If the environment variable DOTENV provides a valid .env file, then override .env with its content
if [ -n "$DOTENV" ]; then
    if [ -f "$DOTENV" ]; then
        echo "Overriding .env with ${DOTENV}"
        cp ${DOTENV} .env
    else
        echo "Provided dotenv file [${DOTENV}] is not a vaild file."
        exit 1
    fi
fi
