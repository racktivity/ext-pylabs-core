__author__ = 'roomtivity'
__tags__ = 'floor', 'getAggregatedData'
__priority__= 3

import collections

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def avg(v1, v2):
    if v1 == 0:
        return v2
    else:
        return (v1 + v2) / 2
    
def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    floorguid = params['floorguid']
    if not exists('view_floor_list', q.drp.floor, "guid", floorguid):
        raise ValueError("No floor with this guid (%s) exists"%floorguid)
    
    meteringtypes = params['meteringtypes']
    from rootobjectaction_lib import rootobjectaction_find
    rackguids = rootobjectaction_find.rack_find(floor=floorguid)
    from rootobjectaction_lib import rootobject_authorization
    rackguids = rootobject_authorization.getAuthorizedGuids(params["request"]["username"], rackguids, q.drp.rack , "getAggregatedData")
    
    result = {'Current': 0.0,
              'Voltage': 0.0,
              'Frequency': 0.0,
              'Power': 0.0,
              'PowerFactor': 0.0,
              'ActiveEnergy': 0.0,
              'ApparentEnergy': 0.0,
              'ApparentPower': 0.0,
              'Co2': 0.0}
    
    averages = {'Current': [0.0, 0.0, 0.0, 0.0],
              'Voltage': [0.0, 0.0, 0.0, 0.0],
              'Frequency': [0.0, 0.0, 0.0, 0.0],
              'Power': [0.0, 0.0, 0.0, 0.0],
              'PowerFactor': [0.0, 0.0, 0.0, 0.0],
              'ActiveEnergy': [0.0, 0.0, 0.0, 0.0],
              'ApparentEnergy': [0.0, 0.0, 0.0, 0.0],
              'ApparentPower': [0.0, 0.0, 0.0, 0.0],
              'Co2': [0.0, 0.0, 0.0, 0.0]}
    
    for rackguid in rackguids:
        rackresult = q.actions.rootobject.rack.getAggregatedData(rackguid, meteringtypes, request = params["request"])['result']
        for meteringtype, value in rackresult['value'].iteritems():
            if meteringtype in ('Voltage', 'Frequency'):
                result[meteringtype] = avg(result[meteringtype], float(value))
            else:
                result[meteringtype] += float(value)
        
        for meteringtype, values in rackresult['average'].iteritems():
            for i, value in enumerate(values):
                if meteringtype in ('Voltage', 'Frequency'):
                    averages[meteringtype][i] = avg(averages[meteringtype][i], float(value))
                else:
                    averages[meteringtype][i] += float(value)
                    
    #recalculation of voltage for more accurate values
    if result['ApparentPower'] and result['Current']:
        result['Voltage'] = result['ApparentPower'] / result['Current']
    
    #calculation of powerfactor.
    if result['Power'] and result['ApparentPower']:
        result['PowerFactor'] = min(1.0, result['Power'] / result['ApparentPower'])
    
    #voltage and power factor averages recalculations
    for i, apower in enumerate(averages['ApparentPower']):
        if apower and averages['Power'][i]:
            averages['PowerFactor'][i] = min(1.0, averages['Power'][i] / apower)
        if apower and averages['Current'][i]:
            averages['Voltage'][i] = apower / averages['Current'][i]
        
    params['result'] = {'returncode': True,
                        'value': result,
                        'string': dict([(k, "%0.2f" % v) for k, v in result.iteritems()]),
                        'average': averages,
                        'averagestring': dict([(k, ["%0.2f" % v for v in vs]) for k, vs in averages.iteritems()])}

def match(q, i, params, tags):
    return True
