import sys
from JumpScale import j


import JumpScale.lib.ms1

import JumpScale.baselib.redis
redis=j.clients.redis.getRedisClient("localhost",9999)

secret=j.tools.ms1.getClouspaceSecret(\
            login=j.console.askString("ms1 login"),\
            password=j.console.askString("ms1 passwd"), \
            cloudspace_name=j.console.askString("cloudspace name",defaultparam="default"),\
            location=j.console.askString("location (ca1,us2)",defaultparam="ca1"))

redis.set("ms1:secret",secret)