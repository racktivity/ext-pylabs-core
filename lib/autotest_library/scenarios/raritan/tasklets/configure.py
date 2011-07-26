__tags__= "test", "setup"
__priority__ = 100
import uuid

def main(q, i, params, tags):
    write = q.system.fs.writeFile
    
    write("/opt/qbase3/cfg/qconfig/emulatoraddress.cfg", """[main]
ipaddress=%(raritanip)s
port=%(port)s
type=%(type)s""" % params)
    
    

def match(q, i, params, tags):
    return True