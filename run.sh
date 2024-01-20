#! /bin/bash

docker build -t adapter ./code/
docker swarm init
docker stack deploy -c stack.yml sprc3 