__tags__= "test", "setup"
__priority__ = 100
import uuid

def main(q, i, params, tags):
    write = q.system.fs.writeFile
    
    write("/opt/qbase3/cfg/qconfig/dist_auth.cfg",
          """[main]
access_token_url=%(oauthservice)s
          """ % params)
    
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
    
    write("/opt/qbase3/cfg/qconfig/cloudapiconnection.cfg", """[main]
passwd = %(cloudapipassword)s
path = /appserver/xmlrpc/
login = %(cloudapilogin)s
port = 8888
server = %(cloudapiaddress)s""" % params)
    
    write("/opt/qbase3/cfg/qconfig/emulatoraddress.cfg", """[main]
ipaddress=%(emulatoraddress)s""" % params)
    
    

def match(q, i, params, tags):
    return True
