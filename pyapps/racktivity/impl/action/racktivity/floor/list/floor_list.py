__author__ = 'racktivity'
__tags__ = 'floor', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    floorguid = params['floorguid'] or None
    from rootobjectaction_lib import rootobjectaction_list
    
    params['result'] = {'returncode': True,
                        'floorinfo': rootobjectaction_list.floor_list(floorguid=floorguid)}

def match(q, i, params, tags):
    return True
