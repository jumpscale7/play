to get started:
===============

make sure instructions on home page of this repo are followed

```python
jpackage install -n docker

#login (probably not required)
docker login
```

see
[do.sh](do.sh) for how to use

just execute this bash file and 2 docker local images will be the result
as well as an up and running docker machine which you can use to play with

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
