set -ex

#make sure latest docker is downloaded (is ubuntu 14.04 with mc preinstalled)
##the -b is for the base image
jsdocker pull -b despiegk/mc

#create new docker
jsdocker new -n mydocker -b despiegk/mc --vols "/opt/code:/opt/code"

#make sure docker is updated (ubuntu update) & right packages installed
fab deploy.base -H localhost:9022

#commit to new local docker image (so we can use in future)
jsdocker commit -n mydocker -b ubuntu_base

#this installs jumpscale in development mode
fab deploy.js -H localhost:9022

#commit to new local docker image (so we can use in future)
jsdocker commit -n mydocker -b ubuntu_js

# ssh localhost -p 9022

