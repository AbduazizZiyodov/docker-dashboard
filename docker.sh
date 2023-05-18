#!/bin/bash

DOCKERFILE_PATH=./docker/
DOCKERHUB_USERNAME=abduaziz
DOCKER_IMAGE_NAME=docker-dashboard
DOCKER_SOCKET_PATH=/var/run/docker.sock
VERSION=$(cat src/client/package.json | grep version | cut -f2 -d ':' | cut -f2 -d '"')

DOCKER_IMAGE=$DOCKERHUB_USERNAME/$DOCKER_IMAGE_NAME:$VERSION

# Copy files
rsync -av src/server \
  $DOCKERFILE_PATH \
  --exclude env \
  --exclude pytest.ini \
  --exclude tests \
  --exclude .pytest_cache \
  --exclude __pycache__ \
  --exclude test_requirements.txt

cd docker/

# Build docker image, set build date as label
docker build \
  --no-cache=true \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%S') \
  -t $DOCKER_IMAGE .

if [ "$1" = "run" ]; then
  # run container, API url is localhost:2121
  # supervisor(inet http server) localhost:9001
  docker run -d \
    -p 2121:2121 -p 9001:9001 \
    -v $DOCKER_SOCKET_PATH:$DOCKER_SOCKET_PATH \
    $DOCKER_IMAGE

elif [ "$1" = "push" ]; then
  docker push $DOCKER_IMAGE

fi

cd ..

rm -rf $DOCKERFILE_PATH/server/
