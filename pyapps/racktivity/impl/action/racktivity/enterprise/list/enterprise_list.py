__author__ = 'racktivity'
__tags__ = 'enterprise', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'enterpriseinfo': rootobjectaction_list.enterprise_list(name = params['name'], campus=params['campus'], tags = params['tags'])}

def match(q, i, params, tags):
    return True
