__author__ = 'aserver'
__tags__ = 'rack', 'getViewData'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False, "data" :list()}
    meteringUnits = {"Voltage":"V", "Power":"W", "Current":"A", "PowerFactor":"", "ActiveEnergy":"kwh"}
    from rootobjectaction_lib import rootobjectaction_find
    ca = i.config.cloudApiConnection.find("main")
    data = ca.rack.getAggregatedData(params["rootobjectguid"] , "all")['result']['value']
    for key in data:
        if key in meteringUnits:
            params['result']["data"].append({"viewdatatype":key,"viewdatavalue":data[key], "viewdataunit":meteringUnits[key]})
    params['result']['meteringdevices'] = len(rootobjectaction_find.meteringdevice_find(rackguid=params['rootobjectguid']))
    params['result']['returncode'] = True

def match(q, i, params, tags):
    return True
