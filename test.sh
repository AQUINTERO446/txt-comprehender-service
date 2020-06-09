#!/bin/bash
docker run -dit --rm --name test_tpkutils -p 9999:80 $DOCKER_REPO
sleep 5
# curl -X POST -F 'tpk_file=@/tests/alt_root_name.tpk' 'http://localhost:9999/convert'
curl -X GET 'http://localhost:9999/health'
docker stop test_tpkutils
