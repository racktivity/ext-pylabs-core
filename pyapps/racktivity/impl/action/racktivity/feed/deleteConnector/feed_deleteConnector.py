__author__ = 'racktivity'
__tags__ = 'feed', 'deleteConnector'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    feed = q.drp.feed.get(feedguid)
    connector = None
    for p in feed.feedconnectors:
        if p.name == params['name']:
            connector = p
            break
    if not connector:
        raise ValueError("No connector found with name '%s'" % params['name'])
    
    #Delete the connector from the feed and save to drp
    feed.feedconnectors.remove(connector)
    q.drp.feed.save(feed)

    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True