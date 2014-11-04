play
====

play with jumpscale
Each subdir will create a full environment with 

install on mothership1 (recommended)
------------------------------------
see $play/jumpscale_ms1/ directory
make sure you install jupmpscale in development mode first
install libs
look at do.py page
execute by using python do.py

its a script which automatically configures on MS1 a full JS environment in development mode.

manual install on ubuntu (BROKEN FOR NOW, use mothership1 example)
------------------------------------------------------------------

This should work on ubuntu 14.04+

before using this repo install jumpscale in production mode 
```
curl http://install.jumpscale.org:85/cmds/jsbox_unstable.sh > /tmp/init.sh;sh /tmp/init.sh
source /opt/jsbox/activate
```

to test type 'js'
```
(JSBOX)root@mylinux:/# js
sandbox:/opt/jsbox
Python 2.7.5+ (default, Sep 19 2013, 13:48:49) 
Type "copyright", "credits" or "license" for more information.

IPython 0.13.2 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: 

```

download this repo

```
mkdir -p /code/github/jumpscale
cd /code/github/jumpscale
git clone https://github.com/Jumpscale/play.git
```

install docker & jumpscale docker tools through jumpscale jpackages (make sure you are in the sandbox)
```
jpackage install -n docker
```

now go in eather of the sub directories of this repo & check the readme.md for further instructions

the first one to play with is the 'jumpscale' dir

