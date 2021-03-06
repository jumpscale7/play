
from JumpScale import j
from fabric.api import *

import JumpScale.baselib.remote.cuisine
import JumpScale.lib.docker


def dockers():
    res={}
    
    agentcontrollerIp=docker.getIp("master")

    #create agent docker machines starting from the mybase_js basis
    for i in range(2):
        res[i]=j.tools.docker.create(name="agent_%s"%i,stdout=True,base="mybase_js",ports="",vols="/opt/code:/opt/code",volsro="")
        agentOn1Node(res[i],agentcontrollerIp)
    

def agentOn1Node(sshport,agentcontrollerIp):
    """
    """
    ssh=j.remote.cuisine.connect("localhost",sshport)
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
    ssh.run(cmd)



