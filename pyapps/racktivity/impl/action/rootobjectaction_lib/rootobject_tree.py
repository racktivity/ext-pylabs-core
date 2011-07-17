from pymonkey import q

def _getChildren(result, depth = "INF"):
    result["children"] = q.drp.racktivity.query("select guid, name, type, tags from parenttree where parentguid = '%s'"% result["guid"])
    if depth == "INF":
        for child in result["children"]:
            _getChildren(child)
    else:
        if depth == 0:
            return
        for child in result["children"]:
            _getChildren(child, depth - 1)

def getTree(guid, depth=2):
    result = q.drp.racktivity.query("select guid, name, type, tags from parenttree where guid = '%s'"%guid)
    if not result:
    	raise ValueError("Guid %s does not exist in the parenttree table"%guid)
    result = result[0]
    if depth:
        _getChildren(result, depth - 1)
    else:
        _getChildren(result)
    
    return result

def getChildrenGuids(guid, guidlist = set()):
    result = q.drp.racktivity.query("select guid from parenttree where parentguid = '%s'"% guid)
    #print result
    for r in result:
        guidlist.add(r["guid"])
        getChildrenGuids(r["guid"], guidlist)
    return guidlist

def getObjectGuid(name, type):
    result = q.drp.racktivity.query("select guid from parenttree where name = '%s' and type = '%s'"% (name,type))
    if not result:
        return None
    return result[0]["guid"]

def getMeteringDevices(ro_guid, ro_type):
    """
    Find meteringdevices attached to a specific rootobject
    """
    ro = getattr(q.drp, ro_type)
    obj = ro.get(ro_guid)
    from rootobjectaction_lib import rootobject_search
    mds = rootobject_search.search("types:{meteringdevice} parenttree:{%s:%s}"%(ro_type, obj.name))
    result = list()
    for md in mds:
        mdobj = q.drp.meteringdevice.get(md["guid"])
        #I am only interested in the parents
        if mdobj.parentmeteringdeviceguid:
            continue
        result.append(mdobj.guid)
    return result
