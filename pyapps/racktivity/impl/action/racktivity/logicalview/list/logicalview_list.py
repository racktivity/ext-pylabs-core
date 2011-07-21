__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True,
                        'logicalviewinfo': rootobjectaction_list.logicalview_list(name=params['name'], 
                                                                                  clouduserguid=params['clouduserguid'],
                                                                                  share=params['share'],
                                                                                  tags=params['tags'],
                                                                                   )}

def match(q, i, params, tags):
    return True
