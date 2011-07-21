__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'laninfo': rootobjectaction_list.lan_list(languid=params['languid'], backplaneguid=params['backplaneguid'])}

def match(q, i, params, tags):
    return True
