#!/bin/bash

# the first argument to the script needs to be a Civis Platform notebook ID
echo "PLATFORM_OBJECT_ID=$1
CIVIS_API_KEY=${CIVIS_API_KEY}" > my.env

exec docker run --rm -p 8888:8888 --env-file my.env py3
