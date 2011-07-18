__author__ = 'racktivity'
__tags__ = 'lan', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'laninfo': rootobjectaction_list.lan_list(languid=params['languid'], backplaneguid=params['backplaneguid'])}

def match(q, i, params, tags):
    return True
