#execute this script from a machine which has jumpscale in development mode
#make sure libraries are installed (jpackage install -n libs)
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
secret=redis.get("ms1:secret")

#check if we have already configured a machine if not do it now
if not redis.exists("ms1:currentmachine"):
    import getmachine
    getmachine.main()
addr,port=redis.get("ms1:currentmachine").split(",")

#create connection to the just created machine on ms1
ssh=j.remote.cuisine.connect(addr,port)

#check all commands available on ssh.  (there are lots of)

#INSTALL BASE ENVIRONMENT
def base():
    env.warn_only=True
    run("apt-get update")
    env.warn_only=False
    # ssh.run("apt-get upgrade -y")
    ssh.run("apt-get install mc python-git git ssh python2.7 python-requests python-apt openssl ca-certificates ipython -y")
    ssh.run("wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py")
    ssh.run("python get-pip.py")
    ssh.run("apt-get install byobu tmux libmhash2 libpython-all-dev python-redis python-hiredis -y")

    ssh.run("git config --global user.email \"you@example.com\"")
    ssh.run("git config --global user.name \"Your Name\"")

#INSTALL JUMPSCALE in ms1 vm
def js():
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
    ssh.run("jpackage install -n base -r")
    ssh.run("jpackage install -n core -r --debug")
    ssh.run("jpackage install -n libs -r --debug")

#install docker in ms1 vm
def docker():
    ssh.run("jpackage install -n docker -r")
    ssh.run("jsdocker pull -b despiegk/mc")

#get ms1 vm to play with lots of example environments in jumpscale
def getjumpscale_play_env():    
    if ssh.dir_exists("/opt/code/github/jumpscale/play"):
        ssh.run("cd /opt/code/github/jumpscale/play;git pull")    
    else:
        ssh.run("mkdir -p /opt/code/github/jumpscale")
        ssh.run("cd /opt/code/github/jumpscale;git clone https://github.com/Jumpscale/play.git")

#execute inside the docker
def runplay(category,cmd):
    ssh.run("cd /opt/code/github/jumpscale/play/%s;python %s.py"%(category,cmd))


base()
js()
docker()
getjumpscale_play_env()

#goal of next is to have a docker deployed ontop of ms1 vm
#inside the docker inside the MS1 machine a full portal should be running
runplay("docker_jumpscale_development","do")

#on same docker in ms1 machine agentcontroller will be installed
runplay("docker_agentcontroller","do")

#create x new docker machines which will be agents to previously configured agentcontroller
runplay("docker_agentcontroller","agents")

#the result of all of this should be 
## running portal & agent controller in docker on ms1 vm
## 2 running dockers being agents connected to agentcontroller
## on grid portal all can be looked at


