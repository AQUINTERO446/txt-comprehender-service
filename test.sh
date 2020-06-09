#!/bin/bash
docker run -dit --rm --name test_comprehend -p 9999:80 $DOCKER_REPO
sleep 10
curl -X GET 'http://localhost:9999/health'
docker stop test_comprehend
