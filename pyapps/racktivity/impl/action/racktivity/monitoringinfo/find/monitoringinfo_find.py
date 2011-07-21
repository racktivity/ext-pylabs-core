__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True, 'guidlist': rootobjectaction_find.monitoringinfo_find(monitoringdeviceguid=params['monitoringdeviceguid'], \
                                                                                                starttimestamp=params['starttimestamp'], \
                                                                                                endtimestamp=params['endtimestamp'], \
                                                                                                last=params['last'], jobguid=params['jobguid'],
                                                                                                tags=params['tags'])}

def match(q, i, params, tags):
    return True
