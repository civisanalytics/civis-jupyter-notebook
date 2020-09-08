#!/bin/bash

cp tests/Dockerfile .
docker build -t py3 .
rm Dockerfile
