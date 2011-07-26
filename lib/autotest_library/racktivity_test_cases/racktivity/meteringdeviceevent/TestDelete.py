from nose.tools import *
from pymonkey import i, q
from . import getCloudApi

def testDelete_1():
    """
    @description: [0.30.03.01] Test meteringdeviceevent delete
    @id: 0.30.03.01
    @timestamp: 1293360198
    @signature: mina_magdy
    @params:  ca.meteringdeviceevent.delete(mdeguid)
    @expected_result: A meteringdeviceevent is created and deleted successfully 
    """
    ca = getCloudApi()
    mdeguid = ca.meteringdeviceevent.create(None)["result"]["guid"]
    ca.meteringdeviceevent.delete(mdeguid)
