from pylabs import q
from nose.tools import *
from bootloader.BootLoaderLib import *
import os

#configurable variables
DEVICE_IP = '192.168.14.148'
DEVICE_USERNAME = 'admin'
DEVICE_PASSWORD = '1234'
FIRMWARE_MASTER = 'http://qpackages.racktivity.com/firmware_releases/RTF0023.rfw'
FIRMWARE_POWER = 'http://qpackages.racktivity.com/firmware_releases/RTF0009.rfw'

b = None

def setup():
    q.logger.log('Setup in BootLoaderTest')
    global b
    b = BootLoader()
    b.setIp(DEVICE_IP, DEVICE_USERNAME, DEVICE_PASSWORD)

def teardown():
    q.logger.log('Teardown in BootLoaderTest')
    global b
    b = None

@raises(NackException)
def testErase():
    """
    @description: [0161000] erasing while not in bootloader mode
    @id: 0161000
    @timestamp: 1299160120
    @signature: kneirinc
    @params: bootloader.sendErase('M\x01', 1)
    @expected_result: erase function should fail when not in bootloader
    """
    b.sendErase('M\x01', 1)

@raises(NackException)
def testXtea():
    """
    @description: [0161001] sending XTEA while not in bootloader mode
    @id: 0161001
    @timestamp: 1299160392
    @signature: kneirinc
    @params: bootloader.sendXtea('M\x01', 'data')
    @expected_result: XTEA function should fail when not in bootloader
    """
    b.sendXtea('M\x01', 'data')

def testModuleCount():
    """
    @description: [0161002] the module count should always be at least 2
    @id: 0161002
    @timestamp: 1299160626
    @signature: kneirinc
    @params: bootloader.getModuleCount()
    @expected_result: we should always have at least 2 modules
    """
    assert_true(b.getModuleCount() >= 2)

def testModeSwitch_1():
    """
    @description: [0161003] switching M1 from bootloader to application
    @id: 0161003
    @timestamp: 1299160979
    @signature: kneirinc
    @params: bootloader.setBoot('M\x01') bootloader.setApplication('M\x01')
    @expected_result: we should succeed in doing a full switch cycle
    """
    try:
        b.setBoot('M\x01')
    finally:
        b.setApplication('M\x01')

def testModeSwitch_2():
    """
    @description: [0161004] switching P1 from bootloader to application
    @id: 0161004
    @timestamp: 1299161087
    @signature: kneirinc
    @params: bootloader.setBoot('P\x01') bootloader.setApplication('P\x01')
    @expected_result: we should succeed in doing a full switch cycle
    """
    try:
        b.setBoot('P\x01')
    finally:
        b.setApplication('P\x01')

def testGetId_1():
    """
    @description: [0161005] getting the id of M1
    @id: 0161005
    @timestamp: 1299161233
    @signature: kneirinc
    @params: bootloader.getId('M\x01')
    @expected_result: we should get an id string back
    """
    firmwareId = b.getId('M\x01')
    assert_true(isinstance(firmwareId, basestring))

@raises(NackException)
def testGetId_2():
    """
    @description: [0161006] getting the id of X1
    @id: 0161006
    @timestamp: 1299161324
    @signature: kneirinc
    @params: bootloader.getId('X\x01')
    @expected_result: we shouldn't get a result as X\x01 is non existent
    """
    b.getId('X\x01')

@raises(NackException)
def testGetPageRange_1():
    """
    @description: [0161007] getting the page range of M1 in application mode
    @id: 0161007
    @timestamp: 1299161702
    @signature: kneirinc
    @params: bootloader.getPageRange('M\x01')
    @expected_result: we shouldn't get a page range when in application mode
    """
    b.getPageRange('M\x01')

def testGetPageRange_2():
    """
    @description: [0161008] getting the page range of M1 in boot mode
    @id: 0161008
    @timestamp: 1299161743
    @signature: kneirinc
    @params: bootloader.getPageRange('M\x01')
    @expected_result: we should get a tuple of 2 ints
    """
    try:
        b.setBoot('M\x01')
        pageRange = b.getPageRange('M\x01')
    finally:
        b.setApplication('M\x01')
        
    assert_equals(len(pageRange), 2)
    assert_true(isinstance(pageRange[0], int))
    assert_true(isinstance(pageRange[1], int))

def testGetModuleInfo_1():
    """
    @description: [0161009] getting the info of module 1
    @id: 0161009
    @timestamp: 1299162019
    @signature: kneirinc
    @params: bootloader.getModuleInfo('\x01\x01')
    @expected_result: we should get a list with 1 module inside
    """
    modules = b.getModuleInfo('\x01\x01')
    assert_equals(len(modules), 1)
    assert(modules[0])

def testGetModuleInfo_2():
    """
    @description: [01610010] getting the info of modules 1 & 2
    @id: 01610010
    @timestamp: 1299162077
    @signature: kneirinc
    @params: bootloader.getModuleInfo('\x01\x02')
    @expected_result: we should get a list with 2 modules inside
    """
    modules = b.getModuleInfo('\x01\x02')
    assert_equals(len(modules), 2)
    assert(modules[0])
    assert(modules[1])

@raises(ValidationException)
def testGetModuleInfo_3():
    """
    @description: [01610011] getting the info of module 0
    @id: 01610011
    @timestamp: 1299162104
    @signature: kneirinc
    @params: bootloader.getModuleInfo('\x00\x00')
    @expected_result: we should fail to get any info
    """
    b.getModuleInfo('\x00\x00')

def testUpdate_1():
    """
    @description: [01610012] doing a full upgrade of a device
    @id: 01610012
    @timestamp: 1299162181
    @signature: kneirinc
    @params: bootloader.update(firmwareFiles, True)
    @expected_result: we should succeed into doing a full upgrade of the device
    """
    master = '/opt/qbase3/var/tmp/' + FIRMWARE_MASTER.split('/')[-1]
    power = '/opt/qbase3/var/tmp/' + FIRMWARE_POWER.split('/')[-1]
    q.system.net.download(FIRMWARE_MASTER, master)
    q.system.net.download(FIRMWARE_POWER, power)

    try:
        b.update((master, power), True)
    finally:
        q.system.fs.remove(master)
        q.system.fs.remove(power)

@raises(InvalidFirmwareException)
def testUpdate_2():
    """
    @description: [01610013] doing a full upgrade of a device with invalid firmware files
    @id: 01610013
    @timestamp: 1299573156
    @signature: kneirinc
    @params: bootloader.update(('/dev/null', '/dev/random'), True)
    @expected_result: we should fail into doing a full upgrade of the device
    """
    firmwareFiles = ('/dev/null', '/dev/random')
    
    b.update(firmwareFiles, True)

@raises(UnusedFirmwareException)
def testUpdate_3():
    """
    @description: [01610014] doing a full upgrade of a device with older firmware files
    @id: 01610014
    @timestamp: 1299573313
    @signature: kneirinc
    @params: bootloader.update(firmwareFiles)
    @expected_result: we should fail into doing a full upgrade of the device
    """
    master = '/opt/qbase3/var/tmp/' + FIRMWARE_MASTER.split('/')[-1]
    power = '/opt/qbase3/var/tmp/' + FIRMWARE_POWER.split('/')[-1]
    q.system.net.download(FIRMWARE_MASTER, master)
    q.system.net.download(FIRMWARE_POWER, power)

    try:
        b.update((master, power))
    finally:
        q.system.fs.remove(master)
        q.system.fs.remove(power)

def testUpdate_4():
    """
    @description: [01610015] doing a full upgrade of a device through the extension
    @id: 01610015
    @timestamp: 1299578042
    @signature: kneirinc
    @params: q.clients.racktivity_bootloader.update(ip, username, password, (firmwareFiles), True)
    @expected_result: we should succeed into doing a full upgrade of the device
    """
    master = '/opt/qbase3/var/tmp/' + FIRMWARE_MASTER.split('/')[-1]
    power = '/opt/qbase3/var/tmp/' + FIRMWARE_POWER.split('/')[-1]
    q.system.net.download(FIRMWARE_MASTER, master)
    q.system.net.download(FIRMWARE_POWER, power)

    try:
        q.clients.racktivity_bootloader.update(DEVICE_IP, DEVICE_USERNAME, \
            DEVICE_PASSWORD, (master, power), True)
    finally:
        q.system.fs.remove(master)
        q.system.fs.remove(power)
