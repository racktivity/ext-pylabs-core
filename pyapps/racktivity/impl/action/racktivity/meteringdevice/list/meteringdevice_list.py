__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True, 'meteringdeviceinfo': rootobjectaction_list.meteringdevice_list(meteringdevicetype=params['meteringdevicetype'], \
                                                                                                            rackguid=params['rackguid'], \
                                                                                                            parentmeteringdeviceguid=params['parentmeteringdeviceguid'])}

def match(q, i, params, tags):
    return True