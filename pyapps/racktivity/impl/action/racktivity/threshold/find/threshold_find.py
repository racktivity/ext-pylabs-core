__author__ = 'racktivity'
__tags__ = 'threshold', 'find'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'retruncode': True,
                        'guidlist': rootobjectaction_find.threshold_find(thresholdtype=params['thresholdtype'],
                                                                         thresholdimpacttype=params['thresholdimpacttype'],
                                                                         tags=params['tags'])}

def match(q, i, params, tags):
    return True