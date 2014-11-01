#fabric install script (not using jumpscale)

from fabric.api import *

@task
def osis():
    """
    install osis    
    """
    # run ("jscode update -a '*' -r '*' ")

    #install mongodb (if local install)    
    cmd="""
jpackage install -n mongodb -i main -r --data="\
mongodb.host=127.0.0.1 #\
mongodb.port=27017 #\
mongodb.replicaset=EMPTY #\
mongodb.name=main"
"""
    run(cmd)

    cmd="""
jpackage install -n mongodb_client -i main -r --data="\
mongodb.client.addr=localhost #\
mongodb.client.port=27017 #\
mongodb.client.login= #\
mongodb.client.passwd=EMPTY"
"""
    run(cmd)

    cmd="""
#install influxdb (if local install)
jpackage install -n influxdb -i main -r --data="influxdb.seedservers:"
"""
    run(cmd)

    cmd="""
#install influxdb client
jpackage install -n influxdb_client -i main -r --data="\
influxdb.client.addr=localhost #\
influxdb.client.port=8086 #\
influxdb.client.login=root #\
influxdb.client.passwd=root"
"""
    run(cmd)

    cmd="""
#install osis (if local install)
jpackage install -n osis -i main -r --data="\
osis.key= EMPTY#\
osis.connection=mongodb:main influxdb:main #\
osis.superadmin.passwd=rooter"
"""
    run(cmd)

    cmd="""
#install osis client (if remote install, then no mongodb client nor server required)
jpackage install -n osis_client -i main -r --data="\
osis.client.addr=localhost #\
osis.client.port=5544 #\
osis.client.login=root #\
osis.client.passwd=rooter"
"""
    run(cmd)

@task
def portal():
    """
    install osis    
    """    

    cmd="""
#create admin user for e.g. portal
jsuser set --hrd="\
user.name=admin #\
user.domain=incubaid.com #\
user.passwd=admin #\
user.roles=admin #\
user.active=1 #\
user.description=EMPTY #\
user.emails=kristof@incubaid.com #\
user.xmpp=EMPTY #\
user.mobile=+??? #\
user.authkeys=2354345345,436346346 #\
user.groups=admin"
"""
    run(cmd)

    cmd="""
#install portal (depends on osis)
jpackage install -n portal -i main -r --data="\
portal.port=82 #\
portal.ipaddr=localhost #\
portal.admin.passwd=admin #\
portal.name=main #\
osis.connection=main"
"""
    run(cmd)

    cmd="""
#install portal for jumpscale docs
jpackage install -n doc_jumpscale -r --data="\
portal.instance=main #\
"
"""
    run(cmd)

@task
def grafana():
    run("jpackage install -n grafana")   

    cmd="""
#install portal for jumpscale docs
jpackage install -n grafana_portal -r --data="\
influxdb.connection=main#\
"
"""
    run(cmd)

    run("jsprocess restart -n portal")
