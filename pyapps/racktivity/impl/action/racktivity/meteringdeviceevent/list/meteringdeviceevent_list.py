__author__ = 'racktivity'
__tags__ = 'meteringdeviceevent', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'meteringdeviceeventinfo': rootobjectaction_list.meteringdeviceevent_list(meteringdeviceguid=params['meteringdeviceguid'], \
                                                                                                           portsequence=params['portsequence'], \
                                                                                                           sensorsequence=params['sensorsequence'], \
                                                                                                           eventtype=params['eventtype'], level=params['level'], \
                                                                                                           thresholdguid=params['thresholdguid'], \
                                                                                                           latest=params['latest'])}

def match(q, i, params, tags):
    return True
