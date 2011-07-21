__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    # rootobjecttype: application, datacenter, device
    # fromTime/endTime: YYYY-MM-DD hh:mm:ss
    from rootobjectaction_lib import rootobjectaction_find
    
    params['result'] = {'returncode': True,
                        'jobinfo': rootobjectaction_find.job_find(actionname=params['actionname'], deviceguid =params['deviceguid'], \
                                                                  agentguid=params['agentguid'], applicationguid=params['applicationguid'], \
                                                                  datacenterguid=params['datacenterguid'], fromTime=params['fromTime'], \
                                                                  toTime=params['toTime'],clouduserguid=params['clouduserguid'])}

def match(q, i, params, tags):
    return True

