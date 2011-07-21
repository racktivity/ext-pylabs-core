__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    from rootobjectaction_lib import rootobject_search, rootobject_authorization, rootobject_tree
    
    #sample search: "types:{energyswitch,datacenter}, parenttree:{datacenter: 'LOCHRISTI'}, name:{DCMU* || TESTENVIRONMENT* && Mina*}, tags_labels:{DCLOC && usage:storage}"
    import re
    
    guid = params["guid"]
    lview = p.api.model.racktivity.logicalview.get(guid)
    searchstr = lview.viewstring
    params["result"] = {"returncode":False, "viewname": lview.name, "viewguid":lview.guid,"description":lview.description, "info":list()}
    
    result = list()
    allmdguids = set()
    for objinfo in rootobject_search.search(lview.viewstring):
        ro = getattr(p.api.action.racktivity, objinfo["type"])
        login = params["request"]["username"]
        if not rootobject_authorization.isAuthorized(login, ro.getObject(objinfo["guid"]), "getViewData"):
            continue
        #Get the meteringdevices related to this object and append it to the list
        mdguids = rootobject_tree.getMeteringDevices(objinfo["guid"], objinfo["type"])
        allmdguids = allmdguids.union(mdguids)
        result.append(objinfo)
    #filter the meteringdevices, remove mds that the user has no access to
    allmdguids = rootobject_authorization.getAuthorizedGuids(params["request"]["username"],allmdguids, p.api.model.racktivity.meteringdevice, "getPduHealthStatus")
    pduStatus = [0,0,0]
    for mdguid in allmdguids:
        mdresult = p.api.action.racktivity.meteringdevice.getPduHealthStatus(mdguid, params["timing"])["result"]["healthstatus"]
        pduStatus = [a+b for a,b in zip(mdresult,pduStatus)]
    
    params["result"]["returncode"] = True
    params["result"]["healthstatus"] = pduStatus
    
def match(q, i, params, tags):
    return True


