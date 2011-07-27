from nose.tools import *
import xmlrpclib
import racktivity_test_library
from pylabs import i,q

def setup():
    global ca
    ca = p.api.action.racktivity
    ca.ipaddress.create("Backup_original_IP", "192.168.20.5")

def TestBackup():
    """
    @description: Making a backup and then deleting the IPAddress
    @id: BKUP.1.1
    @timestamp: 1301846034
    @signature: mina
    """
    global ca,filename
    filename = ca.racktivity.backup("/tmp")["result"]["filename"]
    ok_(filename.startswith("/tmp/"))
    ipguid = ca.ipaddress.find(name = "Backup_original_IP")["result"]["guidlist"][0]
    ca.ipaddress.delete(ipguid)
    #Make sure the ip is gone
    assert_equals(len(ca.ipaddress.find(name = "Backup_original_IP")["result"]["guidlist"]), 0)

def TestRestore():
    """
    @description: Restoring the backup file and make sure the IPAddress is back
    @id: BKUP.1.2
    @timestamp: 1301846034
    @signature: mina
    """
    global filename
    import os
    returncode =  os.system("restore.sh '%s' &> /dev/null"%filename)
    assert_equals(returncode, 0, "restore script failed re-run it manually by calling\nrestore.sh '%s'"%filename)
    #Make sure the ip is back
    assert_equals(len(ca.ipaddress.find(name = "Backup_original_IP")["result"]["guidlist"]), 1)
    ipguid = ca.ipaddress.find(name = "Backup_original_IP")["result"]["guidlist"][0]
    ip = ca.ipaddress.getObject(ipguid)
    assert_equals(ip.address, "192.168.20.5")
    ca.ipaddress.delete(ipguid)

def teardown():
    q.system.fs.unlink(filename)
