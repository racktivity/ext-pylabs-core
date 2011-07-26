__tags__= "test", "setup"
__priority__ = 100
import uuid

def main(q, i, params, tags):
    write = q.system.fs.writeFile

    params.update(password = str(uuid.uuid4()))

    print "Writing configuration files for automatic installation"
    
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
amf_ip = 0.0.0.0
rest_improved_ip = 127.0.0.1
rest_improved_port = 8999""" % params)

    
    write("/opt/qbase3/cfg/qconfig/osisconnection.cfg","""[main]
service = osis_service
passwd = 
server = 127.0.0.1
model_path = /opt/qbase3/libexec/osis
path = /appserver/xmlrpc/
login = 
port = 8888""" % params)


    write("/opt/qbase3/cfg/qconfig/drpdb.cfg", """[main]
database = osis
ipaddress = 127.0.0.1""" % params)

    write("/opt/qbase3/cfg/qconfig/qbaseusermanagement.cfg", """[main]
app_root_passwd = %s
app_root_user = qbase
local_daemon_user = qbase""")    

def match(q, i, params, tags):
    return params['stage'] == 1