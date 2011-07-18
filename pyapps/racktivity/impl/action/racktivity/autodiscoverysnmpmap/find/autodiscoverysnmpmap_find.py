__author__ = 'aserver'
__tags__ = 'autodiscoverysnmpmap', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {
                        'returncode':True,
                        'guidlist': rootobjectaction_find.autodiscoverysnmpmap_find(
                                                                                    sysobjectid =  params['sysobjectid'],
                                                                                    manufacturer=params['manufacturer'],
                                                                                    tags=params['tags'])
                        }


def match(q, i, params, tags):
    return True
