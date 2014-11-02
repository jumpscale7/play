to get started:
===============

make sure instructions on home page of this repo are followed to be able to boostrap this.

this section shows you how to connect to mothership1 cloud & automate a jumpscale deployment


see
[do.py](do.py) for how to use

do 
```
python do.py
```

do
```
ssh localhost -p 9022
```
to login

to destroy
```
jsdocker destroy -n mydocker
```

Some details
-------------

```
#make sure latest docker is downloaded (is ubuntu 14.04 with mc preinstalled)
jsdocker pull -b despiegk/mc

#create new docker
jsdocker new -n mydocker --ports "7766:9766"

#to login
ssh localhost -p 9022

#to use fab, passwd does not have to be specified
fab test.hostname -H localhost:9022
```

example fab usage
-----------------
```
fab deploy.installjs -p rooter -H localhost
fab -l #lists the different available commands

-p = passwd
-H = ipaddr
```
