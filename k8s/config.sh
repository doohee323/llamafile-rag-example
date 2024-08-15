#!/usr/bin/env bash

set -x

GIT_BRANCH=$1
STAGING=$2

export GIT_BRANCH=$(echo ${GIT_BRANCH} | sed 's/\//-/g')
GIT_BRANCH=$(echo ${GIT_BRANCH} | cut -b1-21)

bash /var/lib/jenkins/vault.sh get devops-prod sl-devops-admin resources
tar xvfz resources.zip && rm -Rf resources.zip

cp -Rf resources/config config
cp -Rf resources/credentials credentials
cp -Rf resources/sl_eks-main-t eks-main-t
cp -Rf resources/auth.env auth.env

exit 0

- push
#export vault_token=xxx
#cd /vagrant/projects/sl-devops-admin
#bash /vagrant/sl-local/docker/vault.sh put devops-prod sl-devops-admin resources

- get
bash /var/lib/jenkins/vault.sh get devops-prod sl-devops-admin resources
tar xvfz resources.zip && rm -Rf resources.zip

#rm -Rf ./.env
#bash /var/lib/jenkins/k8s.sh vault_config ${NAMESPACE}-${STAGING} dbinfo > ./.env
