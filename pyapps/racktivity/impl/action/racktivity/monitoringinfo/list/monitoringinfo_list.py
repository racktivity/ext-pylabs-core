__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'monitoringinfo': rootobjectaction_list.monitoringinfo_list(monitoringinfoguid = params['monitoringinfoguid'])}

def match(q, i, params, tags):
    return True