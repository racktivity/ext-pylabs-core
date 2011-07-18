__author__ = 'aserver'
__tags__ = 'floor', 'getViewData'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False, "data" :list()}
    floorguid = params['floorguid']
    meteringUnits = {"Voltage":"V", "Power":"W", "Current":"A", "PowerFactor":"", "ActiveEnergy":"kwh"}
    from rootobjectaction_lib import rootobjectaction_find
    data = q.actions.rootobject.floor.getAggregatedData(floorguid , "all")['result']['value']
    for key in data:
        if key in meteringUnits:
            params['result']["data"].append({"viewdatatype":key,"viewdatavalue":data[key], "viewdataunit":meteringUnits[key]})
    params['result']['rooms'] = len(rootobjectaction_find.room_find(floor=floorguid))
    params['result']['returncode'] = True

def match(q, i, params, tags):
    return True
