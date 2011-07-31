__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    feed = p.api.model.racktivity.feed.get(feedguid)
    connector = None
    for fc in feed.feedconnectors:
        if fc.name == params['name']:
            connector = fc
            break
    if not connector:
        raise ValueError("No connector found with name '%s'" % params['name'])
    
    #Delete the connector from the feed and save to drp
    feed.feedconnectors.remove(connector)
    p.api.model.racktivity.feed.save(feed)

    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True