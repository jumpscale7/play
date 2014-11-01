#fabric install script (not using jumpscale)

from JumpScale import j

from fabric.api import *

import JumpScale.lib.docker

docker=j.tools.docker

@task 
def js():
    res={}
    
    agentcontrollerIp=docker.getIp("mydocker")

    for i in range(2):
        res[i]=docker.create(name="agent_%s"%i,stdout=True,base="ubuntu_js",ports="",vols="/opt/code:/opt/code",volsro="")
        agentOn1Node(res[i],agentcontrollerIp)
    

def agentOn1Node(sshport,agentcontrollerIp):
    """
    """

    cmd="""
jpackage install -n jsagent -i main --data="\
ac.ipaddress=$ip #\
ac.port=4444 #\
ac.login=node #\
ac.passwd=EMPTY #\
osis.connection=main #\
webdis.connection=main #\
grid.id=6 #\
agentcontroller.connection=main #\
agentcontroller.webdiskey=1234 #\
grid.node.roles=grid.master,agentcontroller"
"""
    cmd=cmd.replace("$ip",str(agentcontrollerIp))
    run(cmd)



