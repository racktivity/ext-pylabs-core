__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    locationguid = params['locationguid']
    params['result'] = {'returncode': True,
                        'locationinfo': rootobjectaction_list.location_list(locationguid=locationguid)}

def match(q, i, params, tags):
    return True
