
from JumpScale import j

import JumpScale.baselib.redis
redis=j.clients.redis.getRedisClient("localhost",9999)

import JumpScale.lib.ms1
ms1=j.tools.ms1

#check if secret key is already known
if not redis.exists("ms1:secret") or redis.get("ms1:secret")=="":
    import config

secret=redis.get("ms1:secret")

"""
memsize  #size is 0.5,1,2,4,8,16 in GB
ssdsize  #10,20,30,40,100 in GB
imagename= fedora,windows,ubuntu.13.10,ubuntu.12.04,windows.essentials,ubuntu.14.04
           zentyal,debian.7,arch,fedora,centos,opensuse,gitlab,ubuntu.jumpscale
"""
name="mymachine"
myid,addr,port=ms1.createMachine(secret, name, memsize=8, ssdsize=40, description='',delete=True)

#remember that machine has been created
redis.set("ms1:currentmachine","%s,%s"%(addr,port))
