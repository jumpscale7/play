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
