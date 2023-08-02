#!/bin/bash
docker stop $(docker ps -aqf "name=ao3-proxy-")
docker rm -f $(docker ps -aqf "name=ao3-proxy-")
