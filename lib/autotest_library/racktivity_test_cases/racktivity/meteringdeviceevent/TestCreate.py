from nose.tools import *
from pymonkey import i, q
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
    ca = getCloudApi()
    mdeguid = ca.meteringdeviceevent.create(None)["result"]["guid"]

def teardown():
    global mdeguid
    ca = getCloudApi()
    ca.meteringdeviceevent.delete(mdeguid)