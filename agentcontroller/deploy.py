#fabric install script (not using jumpscale)

from fabric.api import *

@task
def ac():
    """
    """
    # run ("jscode update -a '*' -r '*' ")

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

@task
def agentOnAc():
    """
    """

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



