#!/bin/sh

docker build -t test .
docker run -p 80:5000 -d -v $PWD/src:/app/src --name myapp test:latest
