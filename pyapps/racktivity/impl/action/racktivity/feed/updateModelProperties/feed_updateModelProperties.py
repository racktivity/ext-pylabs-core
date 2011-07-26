__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find
import time

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating feed properties in the model', 3)
    feed = p.api.model.racktivity.feed.get(params['feedguid'])
    
    fields = ('name', 'datacenterguid', 'description', 'productiontype', 'co2emission', 'tags')
    #changes to co2emission is not logged
    logged_fields = ('name', 'datacenterguid', 'description', 'productiontype', 'tags')

    changed = False
    for key, value in params.iteritems():
        if key in fields and value:
            if key == 'co2emission':
                co2factor = feed.co2emission
                import datetime
                co2factor[str(datetime.datetime.now())] = value
            else:
                setattr(feed, key, value)
            changed = True
    
    co2factor = params['co2emission']
    if co2factor != None:
        changed = True
        feed.co2emission["%d" % time.time()] = float(co2factor)
        
    if changed:
        #log this event
        parms = dict(params)
        parms["productiontype"] = parms["feedproductiontype"]
        #logger.log_tasklet(__tags__, parms, logged_fields)
        #save the object
        p.api.model.racktivity.feed.save(feed)
        
    if params['datacenterguid']:
        dcguid = params['datacenterguid']
        for guid in rootobjectaction_find.feed_find(datacenterguid=dcguid):
            if guid != feed.guid:
                wrongfeed = p.api.model.racktivity.feed.get(guid)
                wrongfeed.datacenterguid = ''
                p.api.model.racktivity.feed.save(wrongfeed)


    params['result'] = {'returncode':True, 'feedguid': feed.guid}

def match(q, i, params, tags):
    return True

