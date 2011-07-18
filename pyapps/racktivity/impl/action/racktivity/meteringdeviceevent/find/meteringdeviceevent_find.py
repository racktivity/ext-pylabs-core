__author__ = 'racktivity'
__tags__ = 'meteringdeviceevent', 'find'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    result = rootobjectaction_find.meteringdeviceevent_find(meteringdeviceguid=params['meteringdeviceguid'], portsequence=params['portsequence'], \
                                                            sensorsequence=params['sensorsequence'], eventtype=params['eventtype'], level=params['level'], \
                                                            thresholdguid=params['thresholdguid'], latest=params['latest'])
    params['result'] = {'returncode': True,
                        'guidlist': result}

def match(q, i, params, tags):
    return True