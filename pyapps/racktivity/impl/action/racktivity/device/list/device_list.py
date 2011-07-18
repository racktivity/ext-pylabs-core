__author__ = 'racktivity'
__tags__ = 'device', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'deviceinfo': rootobjectaction_list.device_list(deviceguid=params['deviceguid'])}

def match(q, i, params, tags):
    return True
