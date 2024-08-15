#!/usr/bin/env bash

shopt -s expand_aliases
alias k='kubectl --kubeconfig ~/.kube/config'

sudo mkdir -p /vagrant/data
sudo chmod -Rf 777 /vagrant/data

cd /vagrant/projects/sl-devops-admin

k delete -f sl-devops-admin_cronJob.yaml
k delete -f sl-devops-admin.yaml
#k delete -f sl-devops-admin-pv.yaml

#k apply -f sl-devops-admin-pv.yaml
#k get pv
#k get pvc

k apply -f sl-devops-admin.yaml

k apply -f sl-devops-admin_cronJob.yaml

sleep 30

k get all

exit 0

python /app/server.py -p 8088

k create deployment sl-devops-admin --image=slkr/sl-devops-admin:latest
#k create deployment sl-devops-admin --image=slkr/sl-devops-admin:debug3
#k expose rc sl-devops-admin --port=8000 --target-port=8000

#k exec -it pod/sl-devops-admin-95cd4c99b-lz47d bash
#k exec -it deployment.apps/sl-devops-admin bash
#k -v=9 exec -it pod/sl-devops-admin-6cc76cdbc9-2fpfx -- sh
#k exec -it pod/sl-devops-admin-job-1608427500-kv4mx -- sh
#/usr/bin/python3 /app/cli.py -l /mnt/list.txt

k get deployment sl-devops-admin -o yaml > sl-devops-admin.yaml
#k delete deployment.apps/sl-devops-admin
#docker rmi slkr/sl-devops-admin:debug1

exit 0


kubectl run -it busybox --image=alpine:3.6 -n devops-dev -- sh
apk update
apk add --no-cache openssh
apk add --no-cache sshpass
sshpass -p root ssh root@10.20.2.125
sshpass -p root ssh root@10.20.2.125 ls -al




