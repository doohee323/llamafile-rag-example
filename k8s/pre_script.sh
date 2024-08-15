#!/usr/bin/env bash

set -x

GIT_BRANCH=$1
STAGING=$2

export GIT_BRANCH=$(echo ${GIT_BRANCH} | sed 's/\//-/g')
GIT_BRANCH=$(echo ${GIT_BRANCH} | cut -b1-21)

function prop {
  if [[ "${3}" == "" ]]; then
    grep "${2}" "/root/.aws/${1}" | head -n 1 | cut -d '=' -f2 | sed 's/ //g'
  else
    grep "${3}" "/root/.aws/${1}" -A 10 | grep "${2}" | head -n 1 | tail -n 1 | cut -d '=' -f2 | sed 's/ //g'
  fi
}

DEVOPS_ADMIN_PASSWORD=$(prop 'project-t' 'admin_password')
CLUSTER=$(prop 'project-t' 'project')

bash /vault.sh fget devops-dev eks-main-t > devops
bash /vault.sh fget devops-dev eks-main-t.pub > devops.pub
bash /vault.sh fget devops-dev ssh_config > ssh_config
bash /vault.sh fget devops-dev auth.env > auth.env
bash /vault.sh fget devops-dev config > config
bash /vault.sh fget devops-dev credentials > credentials
bash /vault.sh fget devops-dev kubeconfig_eks-main-t > kubeconfig_eks-main-t
