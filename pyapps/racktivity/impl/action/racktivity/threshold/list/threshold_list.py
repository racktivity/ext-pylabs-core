__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'thresholdinfo': rootobjectaction_list.threshold_list(thresholdguid=params['thresholdguid'], \
                                                                              thresholdtype=params['thresholdtype'], thresholdimpacttype=params['thresholdimpacttype'])}

def match(q, i, params, tags):
    return True
