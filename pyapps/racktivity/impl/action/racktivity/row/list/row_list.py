__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'rowinfo': rootobjectaction_list.row_list(rowguid=params['rowguid'], name = params['name'], alias = params['alias'], roomguid = params['roomguid'], podguid = params['podguid'], tags = params['tags'])}

def match(q, i, params, tags):
    return True
