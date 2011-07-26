__author__ = 'racktivity'
__priority__= 3

import collections

ALL = 'all'
from rootobjectaction_lib import rootobjectaction_find

def avg(v1, v2):
    if v1 == 0:
        return v2
    else:
        return (v1 + v2) / 2
     
def expanddevices(guids):
    """
    One level expand, no recursion for performance
    """
    devices = list()
    for guid in guids:
        devices.append(guid)
        children = rootobjectaction_find.find("meteringdevice", parentmeteringdeviceguid=guid)
        for child in children:
            devices.append(child)
    
    return set(devices)

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    customerguid = params['customerguid']
    meteringtypes = params['meteringtypes']
    
    if meteringtypes != ALL:
        if isinstance(meteringtypes, basestring):
            meteringtypes = meteringtypes.split(';')
        elif not isinstance(meteringtypes, list):
            raise RuntimeError("Wrong meteringtypes, expecting a list of meteringtypes or a semicolon separated list of meteringtypes")
    else:
        meteringtypes = ['Current', 'Power', 'PowerFactor', 'ActiveEnergy', 'ApparentEnergy', 'Temperature', 'Humidity', 'Airflow']
        
    if not meteringtypes:
        raise RuntimeError("Empty list of meteringtypes")


    resourcesguids = rootobjectaction_find.resourcegroup_find(customerguid=customerguid)
    
    result = {'Current':0, 'Power':0, 'PowerFactor':0, 'ActiveEnergy':0, 'ApparentEnergy':0, 'Temperature':0, 'Humidity':0, 'Airflow':0}
    
    databases = {}
    portseq = 0
    sensorseq = 0
    aggregationtype = 'AVERAGE'
    resolution = 300
    
    for resourceguid in resourcesguids:
        resource = p.api.model.racktivity.resourcegroup.get(resourceguid)
        mdguids = expanddevices(resource.deviceguids)
        for deviceguid in mdguids:
            md = p.api.model.racktivity.meteringdevice.get(deviceguid)
            for port in md.poweroutputs:
                if 'Current' in meteringtypes:
                    databases['Current-%s' % portseq] = {'databasename': "%s_%d_current" % (md.guid, port.sequence),
                                                     'aggregationtype': aggregationtype,
                                                     'resolution': resolution}
                if 'Power' in meteringtypes:
                    databases['Power-%s' % portseq] = {'databasename': "%s_%d_power" % (md.guid, port.sequence),
                                                   'aggregationtype': aggregationtype,
                                                   'resolution': resolution}
                if 'PowerFactor' in meteringtypes:
                    databases['PowerFactor-%s' % portseq] = {'databasename': "%s_%d_powerfactor" % (md.guid, port.sequence),
                                                         'aggregationtype': aggregationtype,
                                                         'resolution': resolution}
                if 'ActiveEnergy' in meteringtypes:
                    databases['ActiveEnergy-%s' % portseq] = {'databasename': "%s_%d_activeenergy" % (md.guid, port.sequence),
                                                          'aggregationtype': aggregationtype,
                                                          'resolution': resolution}
                if 'ApparentEnergy' in meteringtypes:
                    databases['ApparentEnergy-%s' % portseq] = {'databasename': "%s_%d_apparentenergy" % (md.guid, port.sequence),
                                                            'aggregationtype': aggregationtype,
                                                            'resolution': resolution}
                portseq += 1
            
            for sensor in md.sensors:
                if sensor.sensortype == "TEMPERATURESENSOR":
                    if 'Temperature' in meteringtypes:
                        databases['Temperature-%s' % sensorseq] =  {'databasename': "%s_%d_temperature" % (md.guid, sensor.sequence),
                                                                'aggregationtype': aggregationtype,
                                                                'resolution': resolution}
                    
                if sensor.sensortype == "HUMIDITYSENSOR":
                    if 'Humidity' in meteringtypes:
                        databases['Humidity-%s' % sensorseq] =  {'databasename': "%s_%d_humidity" % (md.guid, sensor.sequence),
                                                             'aggregationtype': aggregationtype,
                                                             'resolution': resolution}
                    
                if sensor.sensortype == "AIRFLOWSENSOR":
                    if 'AirFlow' in meteringtypes:
                        databases['Airflow-%s' % sensorseq] =  {'databasename': "%s_%d_airflow" % (md.guid, sensor.sequence),
                                                            'aggregationtype': aggregationtype,
                                                            'resolution': resolution}
                sensorseq += 1
        
    res = p.api.actor.graphdatabase.getLatestValues(databases)['result']['values']
    
    for valuekey, value in res.iteritems():
        kt = valuekey.split("-")[0]
        if kt in ('Temperature', 'Humidity', 'Airflow', 'PowerFactor'):
            result[kt] = avg(result[kt], value or 0)
        else:
            result[kt] += value or 0
    
    #convert defaultdict to dict since workflow engine can't pass dicts around.
    params['result'] = {'returncode': True, 'value': result, 'string': dict([(k, "%0.2f" % v) for k, v in result.iteritems()])}

def match(q, i, params, tags):
    return True
