__author__ = 'racktivity'
__tags__ = 'ipaddress', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'ipaddressinfo': rootobjectaction_list.ipaddress_list(ipaddressguid=params['ipaddressguid'])}

def match(q, i, params, tags):
    return True
