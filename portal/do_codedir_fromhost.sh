set -ex

#create new docker
#jsdocker new -n mydocker -b ubuntu_js --ports "8086:8086 8083:8083 28017:28017 27017:27017 5544:5544 82:82" \
#    --vols "/opt/jumpscale/var/influxdb:/var/mydocker/influxdb # /opt/jumpscale/var/mongodb:/var/mydocker/mongodb # /opt/code:/opt/code"

#fab deploy.osis -H localhost:9022

fab deploy.portal -H localhost:9022

fab deploy.grafana -H localhost:9022

jsdocker commit -n mydocker -b ubuntu_jsportal