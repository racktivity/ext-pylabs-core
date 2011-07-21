__author__ = 'roomtivity'
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
    
def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    locationguid = params['locationguid']
    if not exists('racktivity_view_location_list', p.api.model.racktivity.location, "guid", locationguid):
        raise ValueError("No location with this guid (%s) exists"%locationguid)
    
    meteringtypes = params['meteringtypes']
    from rootobjectaction_lib import rootobjectaction_find
    datacenterguids = rootobjectaction_find.datacenter_find(locationguid=locationguid)
    
    from rootobjectaction_lib import rootobject_authorization
    datacenterguids = rootobject_authorization.getAuthorizedGuids(params["request"]["username"], datacenterguids, p.api.model.racktivity.datacenter , "getAggregatedData")
    
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
    
    for datacenterguid in datacenterguids:
        datacenterresult = p.api.action.racktivity.datacenter.getAggregatedData(datacenterguid, meteringtypes, request = params["request"])['result']
        for meteringtype, value in datacenterresult['value'].iteritems():
            if meteringtype in ('Voltage', 'Frequency'):
                result[meteringtype] = avg(result[meteringtype], float(value))
            else:
                result[meteringtype] += float(value)
        
        for meteringtype, values in datacenterresult['average'].iteritems():
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
