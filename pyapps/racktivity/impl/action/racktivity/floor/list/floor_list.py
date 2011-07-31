__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    
    params['result'] = {'returncode': True,
                        'floorinfo': rootobjectaction_list.floor_list(floorguid=params['floorguid'],
                                                                      datacenterguid=params['datacenterguid'])}

def match(q, i, params, tags):
    return True
