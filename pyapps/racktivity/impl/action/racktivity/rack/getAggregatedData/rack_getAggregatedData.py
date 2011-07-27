__author__ = 'racktivity'
__priority__= 3

import collections
from rootobjectaction_lib import rootobjectaction_find

def avg(v1, v2):
    if v1 == 0:
        return v2
    else:
        return (v1 + v2) / 2

CO2EMISSIONS = {'COAL':800.0,
                'GAS':430.0,
                'GENERIC':4.0,
                'GENERIC_GREEN':4.0,
                'NUCLEAR':6.0,
                'SOLAR':60.0,
                'WIND':3.0}

def getEmissionFactor(q, mdguid):
    feeds = set()
    device = p.api.model.racktivity.meteringdevice.get(mdguid)
    for input in device.powerinputs:
        if input.cableguid:
            guids = rootobjectaction_find.feed_find(cableguid=input.cableguid)
            feeds = feeds.union(guids)
    
    if not feeds:
        q.logger.log("Metering deivce '%s' is not connected to any feeds, Can't calculate CO2 emission")
        return 0
    
    if len(feeds) > 1:
        q.logger.log("Metering deivce '%s' is connected to multiple feeds, Can't calculate CO2 emission")
        return 0
    
    feed = p.api.model.racktivity.feed.get(feeds.pop())
    timestamps = feed.co2emission.keys()
    
    if timestamps:
        #get last time stamp.
        timestamps.sort()
        return feed.co2emission[timestamps.pop()]
    else:
        #get default.
        return CO2EMISSIONS.get(str(feed.productiontype), 0)

class KeyGen(object):
    def __init__(self, guid):
        self.guid = guid
    
    def __call__(self, metering):
        return "%s-%s" % (metering, self.guid)
    
    @property
    def current(self):
        return self("Current")
    
    @property
    def voltage(self):
        return self("Voltage")
    
    @property
    def frequency(self):
        return self("Frequency")
    
    @property
    def power(self):
        return self("Frequency")
    
    @property
    def powerfactor(self):
        return self("PowerFactor")
    
    @property
    def activeenergy(self):
        return self("ActiveEnergy")
    
    @property
    def apparentenergy(self):
        return self("ApparentEnergy")
    
    @property
    def apparentpower(self):
        return self("ApparentPower")
    
def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    rackguid = params['rackguid']
    if not rootobjectaction_find.find('rack', guid = rackguid):
        raise ValueError("No rack with this guid (%s) exists"%rackguid)
    
    meteringtypes = params['meteringtypes']
    
    #get all metering types.
    meteringtypes = ['Current', 'Voltage', 'Frequency', 'Power', 'PowerFactor',
                     'ActiveEnergy', 'ApparentEnergy', 'ApparentPower',
                     'Co2']

    mdguids = rootobjectaction_find.find("meteringdevice", rackguid=rackguid)
    
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
    
    databases = {}
    portseq = 0
    sensorseq = 0
    aggregationtype = 'AVERAGE'
    resolution = 300
    
    
    for mdguid in mdguids:
        md = p.api.model.racktivity.meteringdevice.get(mdguid)
        key = KeyGen(mdguid)
        
        databases[key.current] = "%s_current" % md.guid
        databases[key.voltage] = "%s_voltage" % md.guid
        databases[key.frequency] = "%s_frequency" % md.guid
        databases[key.powerfactor] = "%s_powerfactor" % md.guid
        databases[key.activeenergy] = "%s_activeenergy" % md.guid
        databases[key.apparentenergy] = "%s_apparentenergy" % md.guid
    
    res = p.api.actor.racktivity.graphdatabase.getLatests(databases)['result']['values']
    averagesres = p.api.actor.racktivity.graphdatabase.getAverageValues(databases)['result']['values']
    
    for mdguid in mdguids:
        key = KeyGen(mdguid)
        current = res[key.current]
        voltage = res[key.voltage]
        #empty values, no power readings.
        if current == None or voltage == None:
            #it's not a power module, skip it
            continue
        
        data = {'Current': current,
                'Voltage': voltage,
                'Frequency': res[key.frequency],
                'ActiveEnergy': res[key.activeenergy],
                'ApparentEnergy': res[key.apparentenergy]}
        
        powerfactor = res[key.powerfactor]
        apparentpower = current * voltage
        power = apparentpower * powerfactor
        
        emissionFactor = getEmissionFactor(q, mdguid)
        co2 = data['ActiveEnergy'] * emissionFactor
        
        data['ApparentPower'] = apparentpower
        data['Power'] = power
        data['Co2'] = co2
        
        #add to aggregated results
        for mt, value in data.iteritems():
            if mt in ('Voltage', 'Frequency'):
                result[mt] = avg(result[mt], value)
            else:
                result[mt] += value
        
        #averages.
        avgdata = {'Current': averagesres[key.current],
                   'Voltage': averagesres[key.voltage],
                   'Frequency': averagesres[key.frequency],
                   'ActiveEnergy': averagesres[key.activeenergy],
                   'ApparentEnergy': averagesres[key.apparentenergy]}
        
        avgpowerfactor = averagesres[key.powerfactor]
        avgapparentpower = [x * y for x, y in zip(avgdata['Current'], avgdata['Voltage'])]
        avgpower = [x * y for x, y in zip(avgapparentpower, avgpowerfactor)]
        avgco2 = [emissionFactor * x for x in avgdata['ActiveEnergy']]
        
        avgdata['ApparentPower'] = avgapparentpower
        avgdata['Power'] = avgpower
        avgdata['Co2'] = avgco2
        
        for mt, values in avgdata.iteritems():
            for i, value in enumerate(values):
                if mt in ('Voltage', 'Frequency'):
                    averages[mt][i] = avg(averages[mt][i], value or 0)
                else:
                    averages[mt][i] += value or 0
    
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
    
    #convert defaultdict to dict since workflow engine can't pass dicts around.
    params['result'] = {'returncode': True, 'value': result,
                        'string': dict([(k, "%0.2f" % v) for k, v in result.iteritems()]),
                        'average': averages,
                        'averagestring': dict([(k, ["%0.2f" % v for v in vs]) for k, vs in averages.iteritems()])}

def match(q, i, params, tags):
    return True
