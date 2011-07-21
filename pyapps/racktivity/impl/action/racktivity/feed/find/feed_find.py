__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':True, 'guidlist': rootobjectaction_find.feed_find(name=params['name'], datacenterguid=params['datacenterguid'], 
                                                                             tags=params['tags'], cableguid=params['cableguid'])}

def match(q, i, params, tags):
    return True
