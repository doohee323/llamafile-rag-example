#!/usr/bin/env bash

set -x

#bash build.sh latest
#bash build.sh debug2

#bash /vagrant/projects/sl-devops-admin/build.sh debug3

SL-PROJECT=sl-devops-admin
cd /vagrant/sl-local/resource/${SL-PROJECT}

VERSION='latest'
if [[ "$1" != "" ]]; then
  VERSION=$1
fi

echo "## [ Make an jenkins env ] #############################"
if [[ -f "/vagrant/sl-local/resource/dockerhub" ]]; then
  export DOCKER_ID=`grep 'docker_id' /vagrant/sl-local/resource/dockerhub | awk '{print $3}'`
  export DOCKER_PASSWD=`grep 'docker_passwd' /vagrant/sl-local/resource/dockerhub | awk '{print $3}'`

  docker build -t ${SL-PROJECT}:${VERSION} .
  docker login -u="$DOCKER_ID" -p="$DOCKER_PASSWD"
  docker tag ${SL-PROJECT}:${VERSION} ${DOCKER_ID}/${SL-PROJECT}:${VERSION}
  docker push ${DOCKER_ID}/${SL-PROJECT}:${VERSION}
fi

exit 0

docker rmi sl-devops-admin:latest
docker rmi slkr/sl-devops-admin:latest

docker run -d -v `pwd`:/app -p 8000:8000 sl-devops-admin
docker run -v `pwd`:/app -p 8000:8000 sl-devops-admin
#docker exec -it kind_benz /bin/bash

#docker image ls
#python /app/server.py &

curl -XGET http://localhost:8000/health

