to get started:
===============

make sure instructions on home page of this repo are followed

```python
jpackage install -n docker

#login (probably not required)
docker login
```

see
[do.py](do.py) for how to use
Its an easy to change script


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
