__author__ = 'racktivity'
__tags__ = 'pod', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'podinfo': rootobjectaction_list.pod_list(podguid = params['podguid'], name = params['name'], alias = params['alias'], room = params['room'], tags = params['tags'])}

def match(q, i, params, tags):
    return True
