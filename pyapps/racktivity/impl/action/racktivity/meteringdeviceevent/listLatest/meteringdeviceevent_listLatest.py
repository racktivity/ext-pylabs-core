__author__ = 'racktivity'

from pg import escape_string
import time
from rootobjectaction_lib import rootobjectaction_find

def searchLocation(q, guid):
    mds = []
    for dcguid in rootobjectaction_find.datacenter_find(guid):
        for floor in rootobjectaction_find.floor_find(datacenterguid=dcguid):
            for rack in rootobjectaction_find.rack_find(floor=floor):
                mds += searchRack(q, rack)
    return mds

def searchDatacenter(q, guid):
    mds = []
    for floor in rootobjectaction_find.floor_find(datacenterguid=guid):
        for rack in rootobjectaction_find.rack_find(floor=floor):
            mds += searchRack(q, rack)
            
    return mds

def searchFloor(q, guid):
    mds = []
    for rack in rootobjectaction_find.rack_find(floor=guid):
        mds += searchRack(q, rack)
    return mds

def searchRoom(q, guid):
    mds = []
    for rack in rootobjectaction_find.rack_find(roomguid=guid):
        mds += searchRack(q, rack)
    return mds


def searchPod(q, guid):
    pod = p.api.model.racktivity.pod.get(guid)
    mds = []
    for rack in pod.racks:
        mds += searchRack(q, rack)
    
    for row in rootobjectaction_find.row_find(pod=guid):
        mds += searchRow(q, row)
    
    return mds

def searchRow(q, guid):
    row = p.api.model.racktivity.row.get(guid)
    mds = []
    for rack in row.racks:
        mds += searchRack(q, rack)
        
    return mds

def searchRack(q, guid):
    return rootobjectaction_find.find("meteringdevice",rackguid=guid)

def searchMeteringDevice(q, guid):
    return [guid]

SEARCHMETHODS = {'datacenterguid': searchDatacenter,
                 'floorguid': searchFloor,
                 'roomguid': searchRoom,
                 'podguid': searchPod,
                 'rowguid': searchRow,
                 'rackguid': searchRack,
                 'meteringdeviceguid': searchMeteringDevice}

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False,
                        'racktivitydeviceeventinformation': []}
    
    limit = params['limit']
    
    sql = """
    select event.errormessagepublic, event.eventtype, event."guid", event.level,
       event.meteringdeviceguid, event.portsequence, event.sensorsequence, event.tags, event.thresholdguid, event."timestamp"
        from meteringdeviceevent.view_meteringdeviceevent_list as event 
        %(where)s
        order by event."timestamp" desc limit %(limit)s
    """
    if params["level"] is None:
        params["level"] = ""
    else:
        params["level"] = str(params["level"])
    
    eventkeys = ('portsequence', 'sensorsequence', 'eventtype', 'level', 'thresholdguid')
    
    where = list()
    for k in eventkeys:
        if k in params and params[k]:
            where.append("""event."%s" = '%s'""" % (k, escape_string(params[k])))
    
    mds = set()
    for key, searchmethod in SEARCHMETHODS.iteritems():
        guid = params.get(key)
        if guid:
            mds = mds.union(searchmethod(q, guid))
    
    if not mds:
        return
    
    where.append("""event.meteringdeviceguid in (%s)""" % ", ".join(["'%s'" % g for g in mds])) 
    
    
    results = p.api.model.racktivity.meteringdeviceevent.query(sql % {'where': "where %s" % " and ".join(where) if where else '',
                                                     'limit': limit})
    
    levelmap = {1: 'CRITICAL', 3: 'ERROR', 5: 'INFO', 0: 'UNKNOWN', 2: 'URGENT', 4: 'WARNING'}
    
    for result in results:
        tags = q.base.tags.getObject(result['tags'])
        if result["meteringdeviceguid"]:
            md = p.api.model.racktivity.meteringdevice.get(result["meteringdeviceguid"])
            rack = p.api.model.racktivity.rack.get(md.rackguid)
            result["meteringdevice"] = md.name
            result["rack"] = rack.name
            result["rackguid"] = rack.guid
        else:
            result["meteringdevice"] = "Unknown"
            result["rack"] = result["rackguid"] = ""
        result['ipaddress'] = tags.tagGet("ipaddress") if tags.tagExists("ipaddress") else ""
        if result['level'] is None:
            result['leveltxt'] = 'UNKNOWN'
        else:
            result['leveltxt'] = levelmap[result['level']]
        result['time'] = time.ctime(result['timestamp'])
        result['errormessagepublic'] = result['errormessagepublic'] or ''
        
    params['result'] = {'returncode': True,
                        'racktivitydeviceeventinformation': results}

def match(q, i, params, tags):
    return True
