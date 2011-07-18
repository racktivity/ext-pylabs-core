__author__ = 'racktivity'
__tags__ = 'rack', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'rackinfo': rootobjectaction_list.rack_list(rackguid=params['rackguid'])}

def match(q, i, params, tags):
    return True
