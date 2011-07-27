from nose.tools import *
import xmlrpclib
from pylabs import i,q,p
import pg

def setup():
    global ca, conn
    ca = p.api.action.racktivity
    POSTGRESS_IP = q.config.getConfig("cloudapiconnection")["main"]["server"]
    conn = pg.connect("audit", POSTGRESS_IP, 5432,None, user="qbase", passwd="qbase")

def teardown():
    conn.close()

def getLastRow(model):
    id=conn.query("select max(id) from audit where model = 'ipaddress'").getresult()[0][0]
    id=int(id) - 20
    rows = conn.query("""SELECT guid,"name","action","valName","old","new"
                         FROM audit as a LEFT OUTER JOIN "values" as v ON ("eventId" = "a"."id")
			 WHERE "a"."id" > %d and model = '%s'"""%(id,model)).getresult()
    row = list(rows[-1])
    for idx,cell in enumerate(row):
        if type(cell) is str:
	    row[idx] = cell.strip()
    return row

def testCreate():
    """
    @description: Creating an IPAddress and validating its log
    """
    ip1Guid = ca.ipaddress.create("TestIP1", "192.192.192.192")["result"]["ipaddressguid"]
    row = getLastRow("ipaddress")
    assert_equal(row[1],"TestIP1")
    assert_equal(row[2],"create")
    ca.ipaddress.delete(ip1Guid)

def testDelete():
    """
    @description: deleting ipaddress and validating its log
    """
    ip1Guid = ca.ipaddress.create("TestIP2", "192.192.192.192")["result"]["ipaddressguid"]
    ca.ipaddress.delete(ip1Guid)
    row = getLastRow("ipaddress")
    assert_equal(row[0],ip1Guid)
    assert_equal(row[1],"TestIP2")
    assert_equal(row[2],"delete")


def testUpdate():
    """
    @description: updating ipaddress and validating its log
    """
    ip1Guid = ca.ipaddress.create("oldIPName", "192.192.192.192", "oldIPDesc")["result"]["ipaddressguid"]
    oldkeyval = {"name":"oldIPName", "description":"oldIPDesc", "address": "192.192.192.192"}
    newkeyval = {"name":"newIPName", "description":"newIPDesc", "address": "192.192.192.193"}
    for prop in ("name", "description", "address"):
        param = {prop:newkeyval[prop]}
        ca.ipaddress.updateModelProperties(ip1Guid, **param)
        row = getLastRow("ipaddress")
        assert_equal(row[0],ip1Guid)
        assert_equal(row[2],"updateModelProperties")
        assert_equal(row[3], prop)
	#import rpdb2
	#rpdb2.start_embedded_debugger("1234")
        assert_equal(eval(row[4]), oldkeyval[prop])
        assert_equal(eval(row[5]), newkeyval[prop])
    ca.ipaddress.delete(ip1Guid)
