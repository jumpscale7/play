
from JumpScale import j
from fabric.api import *
import JumpScale.baselib.redis
import JumpScale.lib.ms1
import JumpScale.baselib.remote.cuisine

ms1=j.tools.ms1

#redis is memory database which is always running when jumpscale is installed
redis=j.clients.redis.getRedisClient("localhost",9999)

#check if redis has secret key for ms1, if not ask it
if not redis.exists("ms1:secret") or redis.get("ms1:secret")=="":
    import config

#check if we have already configured a machine if not do it now
secret=redis.get("ms1:secret")
if not redis.exists("ms1:currentmachine"):
    import getmachine

addr,port=redis.get("ms1:currentmachine").split(",")

ssh=j.remote.cuisine.connect(addr,port)

#check all commands available on ssh.  (there are lots of)

#INSTALL BASE ENVIRONMENT
def base():
    env.warn_only=True
    run("apt-get update")
    env.warn_only=False
    ssh.run("apt-get upgrade -y")
    ssh.run("apt-get install mc python-git git ssh python2.7 python-requests python-apt openssl ca-certificates python-pip ipython -y")
    ssh.run("apt-get install byobu tmux libmhash2 libpython-all-dev python-redis python-hiredis -y")

#INSTALL JUMPSCALE
def js():
    run("pip install https://github.com/Jumpscale/jumpscale_core/archive/master.zip")
    ssh.run("jpackage mdupdate")
    ssh.run("jpackage install -n base -r")
    ssh.run("jpackage install -n core -r --debug")
    ssh.run("jpackage install -n libs -r --debug")

def docker():
    ssh.run("jpackage install -n docker -r")
    ssh.run("jsdocker pull -b despiegk/mc")

#get environment to play with lots of example environments in jumpscale
def getjumpscale_play_env():    
    if ssh.dir_exists("/opt/code/github/jumpscale/play"):
        ssh.run("cd /opt/code/github/jumpscale/play;git pull")    
    else:
        ssh.run("mkdir -p /opt/code/github/jumpscale")
        ssh.run("cd /opt/code/github/jumpscale;git clone https://github.com/Jumpscale/play.git")

def runplay(category,cmd):
    ssh.run("cd /opt/code/github/jumpscale/%s;python %s.py"%(category,cmd))


#base()
#js()
#docker()
getjumpscale_play_env()
runplay("docker_jumpscale_development","do")
# runplay("portal","do")




