__author__ = 'aserver'
__tags__ = 'datacenter', 'getViewData'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False, "data" :list()}
    meteringUnits = {"Voltage":"V", "Power":"W", "Current":"A", "PowerFactor":"", "ActiveEnergy":"kwh"}
    from rootobjectaction_lib import rootobjectaction_find
    ca = i.config.cloudApiConnection.find("main")
    data = ca.datacenter.getAggregatedData(params["rootobjectguid"] , "all")['result']['value']
    for key in data:
        if key in meteringUnits:
            params['result']["data"].append({"viewdatatype":key,"viewdatavalue":data[key], "viewdataunit":meteringUnits[key]})
    params['result']['rooms'] = len(rootobjectaction_find.room_find(datacenterguid=params['rootobjectguid']))
    params['result']['returncode'] = True

def match(q, i, params, tags):
    return True
