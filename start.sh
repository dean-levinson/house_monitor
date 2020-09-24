#!/bin/sh

docker build -t test .
docker run -p 80:5000 -d -v $PWD:/app --name myapp test:1.0
