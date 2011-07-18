__author__ = 'racktivity'
__tags__ = 'row', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.row_find(name=params['name'], alias=params['alias'], room=params['room'], \
                                                                   pod=params['pod'], rack = params['rack'], tags=params['tags'])}

def match(q, i, params, tags):
    return True
