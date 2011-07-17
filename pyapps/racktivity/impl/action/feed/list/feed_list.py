__author__ = 'racktivity'
__tags__ = 'feed', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'feedinfo': rootobjectaction_list.feed_list(feedguid=params['feedguid'],
                                                                                       datacenterguid=params['datacenterguid'],
                                                                                       feedproductiontype=params['feedproductiontype'],
                                                                                       tags=params['tags'])}

def match(q, i, params, tags):
    return True

