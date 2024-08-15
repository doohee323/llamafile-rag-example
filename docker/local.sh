#!/usr/bin/env bash

brew install python
brew info python

#sudo /usr/local/Cellar/python@3.9/3.9.1/bin/easy_install-3.9 virtualenv
virtualenv venv --python=python3.9
#virtualenv venv
source venv/bin/activate
python --version

#pip3 freeze > requirements.txt
pip3 install --upgrade -r requirements.txt

#pip install pytest

exit 0

# make docker image
cd sl-k8s-vagrant/projects/sl-devops-admin
#vi Dockerfile
#CMD [ "python", "/app/server.py" ]
#sudo chown -Rf vagrant:vagrant /var/run/docker.sock
#docker login -u="$USERNAME" -p="$PASSWD"
#docker rmi sl-devops-admin -f
#docker build -t sl-devops-admin .
#docker image ls
#docker tag sl-devops-admin:latest slkr/sl-devops-admin:latest
#docker push slkr/sl-devops-admin:latest

docker run -p 8000:8000 sl-devops-admin

docker run -d -v `pwd`:/app -p 8000:8000 sl-devops-admin
#docker ps
#docker exec -it a7757a1e1c99 /bin/bash

curl -X GET http://localhost:8000/health

#docker image ls
#docker container run -it --rm --name=debug2 -v `pwd`:/app -p 8000:8000 cd0dad6e335a /bin/sh
docker run --rm -it --name=debug2 -v `pwd`:/app -p 8000:8000 366853331b20  /bin/sh

#python /app/server.py &
#cat /app/ioNng23DkIM.csv
