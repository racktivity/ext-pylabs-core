__author__ = 'racktivity'
__tags__ = 'cable', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':True, 'guidlist': rootobjectaction_find.cable_find(name=params['name'], cabletype=params['cabletype'], 
                                                                             description=params['description'], label=params['label'],
                                                                             tags=params['tags'])}

def match(q, i, params, tags):
    return True
