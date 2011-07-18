__author__ = 'racktivity'
__tags__ = 'row', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'rowinfo': rootobjectaction_list.row_list(rowguid=params['rowguid'], name = params['name'], alias = params['alias'], room = params['room'], pod = params['pod'], tags = params['tags'])}

def match(q, i, params, tags):
    return True
