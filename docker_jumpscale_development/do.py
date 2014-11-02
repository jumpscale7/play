
from JumpScale import j
from fabric.api import *

import JumpScale.baselib.remote.cuisine
import JumpScale.lib.docker
import JumpScale.baselib.redis


redis=j.clients.redis.getRedisClient("localhost",9999)

secret=redis.get("ms1:secret")

def docker_create_machine(reset=False):
    name='master'
    if reset or not redis.exists("play:docker:%s"%name):
        ports="8086:8086 8083:8083 28017:28017 27017:27017 5544:5544 82:82"
        vols="/opt/jumpscale/var/influxdb:/var/mydocker/influxdb # /opt/jumpscale/var/mongodb:/var/mydocker/mongodb"
        port=j.tools.docker.create(name=name, ports=ports, vols=vols, volsro='', stdout=True, base='despiegk/mc', nameserver='8.8.8.8', \
            replace=True, cpu=None, mem=0)
        redis.set("play:docker:%s"%name,str(port))
    return int(redis.get("play:docker:%s"%name))

port=docker_create_machine()
print port
ssh=j.remote.cuisine.connect("localhost",port)
#check all commands available on ssh.  (there are lots of)

def update():
    ssh.run("jpackage mdupdate")
    ssh.run("cd /opt/code/github/jumpscale/jumpscale_core/;git pull")

#INSTALL BASE ENVIRONMENT
def base():
    from IPython import embed
    print "DEBUG NOW ooo"
    embed()
    
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
    run("pip install https://github.com/Jumpscale/jumpscale_core/archive/master.zip")
    ssh.run("jpackage mdupdate")
    ssh.run("jpackage install -n base -r")
    ssh.run("jpackage install -n core -r --debug")
    ssh.run("jpackage install -n libs -r --debug")
    j.tools.docker.commit("master","mybase_js")



base()
js()




