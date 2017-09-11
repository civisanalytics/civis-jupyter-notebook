#!/bin/bash

echo "PLATFORM_OBJECT_ID=<NOTEBOOK ID>
CIVIS_API_KEY=${CIVIS_API_KEY}" > my.env

exec docker run --rm -p 8888:8888 --env-file my.env py3
