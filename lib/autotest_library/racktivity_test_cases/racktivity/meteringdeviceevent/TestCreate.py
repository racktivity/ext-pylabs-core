from nose.tools import *
from pylabs import i,q,p
from . import getCloudApi
    
def testCreate_1():
    """
    @description: [0.30.02.01] Test Create a meteringdeviceevent
    @id: 0.30.02.01
    @timestamp: 1293360198
    @signature: mina_magdy
    @params: ca.meteringdeviceevent.create(None)
    @expected_result: meteringdeviceevent is created, then deleted
    """
    global mdeguid
    ca = p.api.action.racktivity
    mdeguid = ca.meteringdeviceevent.create(None)["result"]["guid"]

def teardown():
    global mdeguid
    ca = p.api.action.racktivity
    ca.meteringdeviceevent.delete(mdeguid)