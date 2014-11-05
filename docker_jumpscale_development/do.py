
from JumpScale import j
from fabric.api import *

import JumpScale.baselib.remote.cuisine
import JumpScale.lib.docker
import JumpScale.baselib.redis

# codedirFromHost=""  #to not map the code dir
codedirFromHost="# /opt/code:/opt/code"

redis=j.clients.redis.getRedisClient("localhost",9999)

secret=redis.get("ms1:secret")

def docker_create_machine(reset=False,image='despiegk/mc'):
    name='master'
    key="play:docker:%s:%s"%(name,image)
    if reset or not redis.exists(key):
        ports="8086:8086 8083:8083 28017:28017 27017:27017 5544:5544 82:82"
        vols="/opt/jumpscale/var/influxdb:/var/mydocker/influxdb # /opt/jumpscale/var/mongodb:/var/mydocker/mongodb %s"%codedirFromHost
        port=j.tools.docker.create(name=name, ports=ports, vols=vols, volsro='', stdout=True, base=image, nameserver='8.8.8.8', \
            replace=True, cpu=None, mem=0)
        redis.set(key,str(port))
    return int(redis.get(key))

def update():
    run("""
        pip uninstall JumpScale-core
killall tmux  #dangerous
killall redis-server
rm -rf /usr/local/lib/python2.7/dist-packages/jumpscale*
rm -rf /usr/local/lib/python2.7/site-packages/jumpscale*
rm -rf /usr/local/lib/python2.7/dist-packages/JumpScale*
rm -rf /usr/local/lib/python2.7/site-packages/JumpScale*
rm -rf /usr/local/lib/python2.7/site-packages/JumpScale/
rm -rf /usr/local/lib/python2.7/site-packages/jumpscale/
rm -rf /usr/local/lib/python2.7/dist-packages/JumpScale/
rm -rf /usr/local/lib/python2.7/dist-packages/jumpscale/
rm -rf /opt/jumpscale
rm /usr/local/bin/js*
rm /usr/local/bin/jpack*
killall python
rm -rf /opt/sentry/
sudo stop redisac
sudo stop redisp
sudo stop redism
sudo stop redisc
killall redis-server
rm -rf /opt/redis/
        """)
    run("pip install https://github.com/Jumpscale/jumpscale_core/archive/master.zip")
    ssh.run("jpackage mdupdate")
    ssh.run("cd /opt/code/github/jumpscale/jumpscale_core/;git pull")

#INSTALL BASE ENVIRONMENT
def base():
    ssh=j.remote.cuisine.connect("localhost",port)
    env.warn_only=True
    ssh.run("apt-get update")
    env.warn_only=False
    ssh.run("apt-get upgrade -y")
    ssh.run("apt-get install mc python-git git ssh python2.7 python-requests python-apt openssl ca-certificates python-pip ipython -y")
    ssh.run("apt-get install byobu tmux libmhash2 libpython-all-dev python-redis python-hiredis -y")
    j.tools.docker.commit("master","mybase")

#INSTALL JUMPSCALE
def js():
    ssh.run("jpackage install -n base -r")
    ssh.run("jpackage install -n core -r --debug")
    ssh.run("jpackage install -n libs -r --debug")
    j.tools.docker.commit("master","mybase_js")

def portal():
    """
    install osis    
    """
    run=ssh.run

    #install mongodb (if local install)    
    cmd="""
jpackage install -n mongodb -i main -r --data="\
mongodb.host=127.0.0.1 #\
mongodb.port=27017 #\
mongodb.replicaset=EMPTY #\
mongodb.name=main"
"""
    run(cmd)

    cmd="""
jpackage install -n mongodb_client -i main -r --data="\
mongodb.client.addr=localhost #\
mongodb.client.port=27017 #\
mongodb.client.login= #\
mongodb.client.passwd=EMPTY"
"""
    run(cmd)

    cmd="""
#install influxdb (if local install)
jpackage install -n influxdb -i main -r --data="influxdb.seedservers:"
"""
    run(cmd)

    cmd="""
#install influxdb client
jpackage install -n influxdb_client -i main -r --data="\
influxdb.client.addr=localhost #\
influxdb.client.port=8086 #\
influxdb.client.login=root #\
influxdb.client.passwd=root"
"""
    run(cmd)

    cmd="""
#install osis (if local install)
jpackage install -n osis -i main -r --data="\
osis.key= EMPTY#\
osis.connection=mongodb:main influxdb:main #\
osis.superadmin.passwd=rooter"
"""
    run(cmd)

    cmd="""
#install osis client (if remote install, then no mongodb client nor server required)
jpackage install -n osis_client -i main -r --data="\
osis.client.addr=localhost #\
osis.client.port=5544 #\
osis.client.login=root #\
osis.client.passwd=rooter"
"""
    run(cmd)

    cmd="""
#create admin user for e.g. portal
jsuser set --hrd="\
user.name=admin #\
user.domain=incubaid.com #\
user.passwd=admin #\
user.roles=admin #\
user.active=1 #\
user.description=EMPTY #\
user.emails=kristof@incubaid.com #\
user.xmpp=EMPTY #\
user.mobile=+??? #\
user.authkeys=2354345345,436346346 #\
user.groups=admin"
"""
    run(cmd)

    cmd="""
#install portal (depends on osis)
jpackage install -n portal -i main -r --data="\
portal.port=82 #\
portal.ipaddr=localhost #\
portal.admin.passwd=admin #\
portal.name=main #\
osis.connection=main"
"""
    run(cmd)

    cmd="""
#install portal for jumpscale docs
jpackage install -n doc_jumpscale -r --data="\
portal.instance=main #\
"
"""
    run(cmd)


    run("jpackage install -n grafana")   

    cmd="""
#install portal for jumpscale docs
jpackage install -n grafana_portal -r --data="\
influxdb.connection=main#\
"
"""
    run(cmd)

    run("jsprocess restart -n portal")


###################################################################################

port=docker_create_machine(False)

ssh=j.remote.cuisine.connect("localhost",port)
#check all commands available on ssh.  (there are lots of)

update()
base()
js()

# port=docker_create_machine(False,"mybase_js")
portal()
print "port of docker is: %s"%port


