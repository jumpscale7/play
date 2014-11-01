set -ex

#create new docker
jsdocker new -n mydocker -b ubuntu_jsportal --ports "8086:8086 8083:8083 28017:28017 27017:27017 5544:5544 82:82 7779:7779" \
    --vols "/opt/jumpscale/var/influxdb:/var/mydocker/influxdb # /opt/jumpscale/var/mongodb:/var/mydocker/mongodb"

fab deploy.main -H localhost:9022

jsdocker commit -n mydocker -b ubuntu_agentcontroller

