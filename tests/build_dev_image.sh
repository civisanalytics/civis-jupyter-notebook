#!/bin/bash

cp tests/python3/Dockerfile .
docker build -t py3 .
rm Dockerfile
