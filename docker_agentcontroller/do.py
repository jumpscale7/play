
from JumpScale import j
from fabric.api import *

import JumpScale.baselib.remote.cuisine
import JumpScale.lib.docker
import JumpScale.baselib.redis

# codedirFromHost=""  #to not map the code dir
codedirFromHost="# /opt/code:/opt/code"

redis=j.clients.redis.getRedisClient("localhost",9999)

secret=redis.get("ms1:secret")

def docker_create_machine(reset=False,image='mybase_js'):
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
    ssh.run("jpackage mdupdate")
    ssh.run("cd /opt/code/github/jumpscale/jumpscale_core/;git pull")
    #todo complete
    #would be better to use jscode update ... but need better support to update all now bug

def agentcontroller():
    """
    install osis    
    """
    run=ssh.run

    cmd="""
#install grid portal parts
jpackage install -n grid_portal -r --data="\
portal.instance=main #\
"
"""
    run(cmd)

    cmd="""
#install webdis
jpackage install -n webdis -i main
"""
    run(cmd)

    cmd="""
#install webdis_client
jpackage install -n webdis_client -i main --data="\
addr=127.0.0.1 #\
port=7779"    
"""
    run(cmd)

    cmd="""
#redis for agentcontroller
jpackage install -n redis -i ac --data="\
redis.name=ac #\
redis.port=9999 #\
redis.mem=200 #\
redis.disk=1"    
"""
    run(cmd)

    cmd="""
#agentcontroller
jpackage install -n agentcontroller -i main --data="\
osis.connection=main #\
grid.master.superadminpasswd=rooter #\
agentcontroller.webdiskey=1234 #\
webdis.connection=main #\
grid.id=6 "
"""
    run(cmd)


    cmd="""
#agentcontrolller client
jpackage install -n agentcontroller_client -i main --data="\
agentcontroller.client.addr=127.0.0.1 #\
agentcontroller.client.login=node #\
agentcontroller.client.port=4444"
"""
    run(cmd)

    #restart portal
    run("jsprocess restart -n portal")    

    cmd="""
jpackage install -n jsagent -i main --data="\
ac.ipaddress=localhost #\
ac.port=4444 #\
ac.login=node #\
ac.passwd=EMPTY #\
osis.connection=main #\
webdis.connection=main #\
agentcontroller.connection=main #\
grid.id=6 #\
grid.node.roles=grid.master,agentcontroller"
"""
    run(cmd)




###################################################################################

#id reset True will recreate machine
port=docker_create_machine(reset=False)

ssh=j.remote.cuisine.connect("localhost",port)
#check all commands available on ssh.  (there are lots of)

agentcontroller()

print "port of docker is: %s"%port


