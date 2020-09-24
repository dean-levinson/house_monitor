#!/bin/sh

docker build -t test .
docker run -p 80:5000 -d -v $PWD/src:/app/ --name myapp test:latest
