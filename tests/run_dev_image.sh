#!/bin/bash

# the first argument to the script needs to be a Civis Platform notebook ID
docker run --rm -p 8888:8888 \
-e PLATFORM_OBJECT_ID=$1 -e CIVIS_API_KEY=${CIVIS_API_KEY} py3
