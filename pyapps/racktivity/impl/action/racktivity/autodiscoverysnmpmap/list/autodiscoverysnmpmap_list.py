__author__ = 'aserver'
__tags__ = 'autodiscoverysnmpmap', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'autodiscoverysnmpmapinfo': rootobjectaction_list.autodiscoverysnmpmap_list(
                                                                                         autodiscoverysnmpmapguid=params['autodiscoverysnmpmapguid'],
                                                                                         manufacturer = params['manufacturer'])}

def match(q, i, params, tags):
    return True
