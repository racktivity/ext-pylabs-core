__author__ = 'racktivity'
__tags__ = 'logicalview', 'getViewResult'
__priority__= 3

def main(q, i, params, tags):
    from rootobjectaction_lib import rootobject_search
    from rootobjectaction_lib import  rootobject_authorization
    #sample search: "types:{energyswitch,datacenter}, parenttree:{datacenter: 'LOCHRISTI'}, name:{DCMU* || TESTENVIRONMENT* && Mina*}, tags_labels:{DCLOC && usage:storage}"
    import re
    
    guid = params["logicalviewguid"]
    lview = q.drp.logicalview.get(guid)
    searchstr = lview.viewstring
    params["result"] = {"returncode":False, "viewname": lview.name, "viewguid":lview.guid,"description":lview.description, "info":list()}
    
    result = list()
    for objinfo in rootobject_search.search(lview.viewstring):
        ro = getattr(q.actions.rootobject, objinfo["type"])
        login = params["request"]["username"]
        if not rootobject_authorization.isAuthorized(login, ro.getObject(objinfo["guid"]), "getViewData"):
            continue
        if "getViewData" in dir(ro):
            objinfo["data"] = ro.getViewData(objinfo["guid"])["result"]["data"]
        else:
            objinfo["data"] = dict()
        result.append(objinfo)
        
    
    params["result"]["info"] = result
    params["result"]["returncode"] = True

def match(q, i, params, tags):
    return True
