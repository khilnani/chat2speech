#!/bin/sh

# USE: docker run --network="docker-test"
docker network create -d bridge "local"
