#fabric install script (not using jumpscale)

#install jumpscale (from code)
#install influxdb (jpackage)
#install hekad (jpackage)

from fabric.api import *

@task
def base():
    """
    update ubuntu & install required packages
    """
    env.warn_only=True
    run("apt-get update")
    env.warn_only=False
    run("apt-get upgrade -y")
    run("apt-get install mc python-git git ssh python2.7 python-requests python-apt openssl ca-certificates python-pip ipython -y")
    run("apt-get install byobu tmux libmhash2 -y")

@task
def js():
    """
    install jumpscale
    """
    run("pip install https://github.com/Jumpscale/jumpscale_core/archive/master.zip")
    run("jpackage mdupdate")
    run("jpackage install -n base -r")
    run("jpackage install -n core -r --debug")
    run("jpackage install -n libs -r --debug")

