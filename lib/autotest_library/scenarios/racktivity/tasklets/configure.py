__tags__= "test", "setup"
__priority__ = 100
import uuid

def main(q, i, params, tags):
    write = q.system.fs.writeFile
    
    fqdn="autotest.racktivity.com" #ejabberd requires lower cased fqdn
    password=str(uuid.uuid4())
    agentcontrollerguid=str(uuid.uuid4())
    agentcontrollerpassword=str(uuid.uuid4())
    agentpassword=str(uuid.uuid4())
    agentguid=str(uuid.uuid4())
    
    params.update(fqdn=fqdn,
                  password=password,
                  agentcontrollerguid=agentcontrollerguid,
                  agentcontrollerpassword=agentcontrollerpassword,
                  agentpassword=agentpassword,
                  agentguid=agentguid)
    
    sources = q.tools.inifile.open("/opt/qbase3/cfg/qpackages4/sources.cfg")
    sources.removeSection("racktivity.com")
    sources.write()
    
    print "Adding racktivity domain for user %(packagelogin)s"
    write("/opt/qbase3/cfg/qpackages4/sources.cfg", """[racktivity.com]
metadatabranch = default
metadatafromtgz = 0
metadatafrommercurial = https://%(packagelogin)s:%(packagepassword)s@bitbucket.org/Krisdepeuter/qp_racktivity_com
bundledownload = %(packageurl)s
""" % params, True)
    
    print "Updating ractivity.com credentials"
    if q.system.fs.isDir("/opt/qbase3/var/qpackages4/metadata/racktivity.com/"):
        q.system.fs.removeDirTree("/opt/qbase3/var/qpackages4/metadata/racktivity.com/")
    
    #read -p "Update /opt/qbase3/cfg/qpackages4/sources.cfg"
    i.qp.updateMetaDataAll()
    i.qp.updateAll()
    q.qp._runPendingReconfigeFiles()
    
    print "Writing configuration files for automatic installation"
    write("/opt/qbase3/cfg/qconfig/agent.cfg", """[main]
domain = %(fqdn)s
subscribed = False
agentcontrollerguid = %(agentcontrollerguid)s
passwd = %(agentpassword)s
hostname = %(fqdn)s
xmppserver = %(fqdn)s
enable_cron = True
cron_interval = 60
agentguid = %(agentguid)s
login = %(agentguid)s
password = %(agentpassword)s""" % params) 
    
    write("/opt/qbase3/cfg/qconfig/cloudapiconnection.cfg", """[main]
passwd = %(password)s
path = /appserver/xmlrpc/
login = admin
port = 8888
server = 127.0.0.1""" % params)
    
    
    write("/opt/qbase3/cfg/qconfig/applicationserver.cfg",  """[main]
xmlrpc_port = 8888
xmlrpc_ip = 127.0.0.1
rest_ip = 127.0.0.1
rest_port = 8889
allow_none = True
amf_port = 8899
mail_incoming_server = 
amf_ip = 0.0.0.0""" % params)
    
    write("/opt/qbase3/cfg/qconfig/Workflowengine.cfg", """[main]
agentcontrollerguid = %(agentcontrollerguid)s
xmppserver = %(fqdn)s
osis_service = osis_service
osis_address = http://127.0.0.1:8888
password = %(agentcontrollerpassword)s
port = 9876""" % params)
    
    
    write("/opt/qbase3/cfg/qconfig/osisconnection.cfg","""[main]
service = osis_service
passwd = 
server = 127.0.0.1
model_path = /opt/qbase3/libexec/osis
path = /appserver/xmlrpc/
login = 
port = 8888""" % params)
    
    write("/opt/qbase3/cfg/qconfig/rabbitmqclient.cfg", """[rabbitmqdefcluster]
virtualhost = /
host = localhost
password = guest
userid = guest
port = 5672

[racktivity_main]
virtualhost = /
host = localhost
password = guest
userid = guest
port = 5672""" % params)
    
    write("/opt/qbase3/cfg/qconfig/confluence.cfg", """[main]
login = admin
password = %(password)s""" % params)
    
    write("/opt/qbase3/cfg/qconfig/drpdb.cfg", """[main]
database = osis
ipaddress = 127.0.0.1""" % params)
    

def match(q, i, params, tags):
    return params['stage'] == 1