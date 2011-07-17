__author__ = 'racktivity'
__tags__ = 'location', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    locationguid = params['locationguid']
    params['result'] = {'returncode': True,
                        'locationinfo': rootobjectaction_list.location_list(locationguid=locationguid)}

def match(q, i, params, tags):
    return True
