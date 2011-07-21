__author__ = 'racktivity'

def main(q, i, p, params, tags):
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
