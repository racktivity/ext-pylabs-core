__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    floorguid = params['floorguid'] or None
    from rootobjectaction_lib import rootobjectaction_list
    
    params['result'] = {'returncode': True,
                        'floorinfo': rootobjectaction_list.floor_list(floorguid=floorguid)}

def match(q, i, params, tags):
    return True
