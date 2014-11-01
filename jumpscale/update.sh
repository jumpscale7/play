set -ex

#create new docker to update
jsdocker new -n mydocker -b ubuntu_js

#make sure docker is updated (ubuntu update) & right packages installed
fab update.js -H localhost:9022

#commit to new local docker image (so we can use in future)
jsdocker commit -n mydocker -b ubuntu_js

jsdocker destroy -n mydocker
