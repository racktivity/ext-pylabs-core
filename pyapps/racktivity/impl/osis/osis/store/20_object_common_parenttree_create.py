__author__ = 'racktivity'
__tags__ ='osis', 'store'

from rootobjectaction_lib import rootobjectaction_find

def getEnterprise(obj):
    global osis
    #Update child locations
    return {"parentguid":"00000000-0000-0000-0000-000000000000", "parenttype":""}

def getLocation(obj):
    return {"parentguid":"00000000-0000-0000-0000-000000000000", "parenttype":"enterprise"}

def getDatacenter(obj):
    return {"parentguid":obj.locationguid , "parenttype":"location"}

def getFloor(obj):
    return {"parentguid":obj.datacenterguid , "parenttype":"datacenter"}

def getRoom(obj):
    return {"parentguid":obj.floor, "parenttype":"floor"}

def getPod(obj):
    global osis
    #Update child racks
    for guid in obj.racks:
        osis.runQuery("UPDATE public.parenttree SET parenttype='pod', parentguid = '%s' WHERE guid = '%s'"%(obj.guid, guid))
    
    return {"parentguid":obj.room, "parenttype":"room"}

def getRow(obj):
    global osis
    #Update child racks
    for guid in obj.racks:
        osis.runQuery("UPDATE public.parenttree SET parenttype='row', parentguid = '%s' WHERE guid = '%s'"%(obj.guid, guid))

    if obj.pod:
        return {"parentguid":obj.pod, "parenttype":"pod"}
    else:
        return {"parentguid":obj.room, "parenttype":"room"}

def getRack(obj):
    row = rootobjectaction_find.row_find(rack = obj.guid)
    if row:
        return {"parentguid":row[0], "parenttype":"row"}
    pod = rootobjectaction_find.pod_find(rack = obj.guid)
    if pod:
        return {"parentguid":pod[0], "parenttype":"pod"}
    elif obj.roomguid:
        return {"parentguid":obj.roomguid, "parenttype":"room"}
    elif obj.floor:
        return {"parentguid":obj.floor, "parenttype":"floor"}
    else:
        return {"parentguid":obj.datacenterguid, "parenttype":"datacenter"}

def getMeteringdevice(obj):
    if obj.parentmeteringdeviceguid:
        return {"parentguid":obj.parentmeteringdeviceguid, "parenttype":"meteringdevice"}
    else:
        return {"parentguid":obj.rackguid, "parenttype":"rack"}

def getDevice(obj):
    if obj.parentdeviceguid:
        return {"parentguid":obj.parentdeviceguid, "parenttype":"device"}
    elif obj.rackguid:
        return {"parentguid":obj.rackguid, "parenttype":"rack"} 
    else:
        return {"parentguid":obj.datacenterguid, "parenttype":"datacenter"}

def main(q, i, p, params, tags):
    """
    Create tree entry in parenttree table
    """
    return
    global osis
    osis = p.application.getOsisConnection(p.api.appname)
    objtype = params['rootobjecttype']
    root = params['rootobject']
    getterFuncs = {"rack":getRack, "pod":getPod, "row":getRow, "room":getRoom, "floor":getFloor, "enterprise":getEnterprise,
                   "datacenter":getDatacenter, "location":getLocation, "meteringdevice": getMeteringdevice, "device":getDevice}
    func = getterFuncs[objtype]
    info = func(root)
    info["name"] = root.name
    info["type"] = objtype
    info["tags"] = root.tags
    osis.viewSave(params['domain'], 'public', 'parenttree', root.guid, root.version, info)

def match(q, i, p, params, tags):
    return params['rootobjecttype'] in ("device", "rack", "pod", "row", "room", "floor", "datacenter", "location", "meteringdevice", "enterprise")
