__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    feed = p.api.model.racktivity.feed.get(feedguid)
    connector = None
    for c in feed.feedconnectors:
        if c.name == params['name']:
            connector = c
            break
    
    if not connector:
        raise ValueError("Can't find connector with name '%s'" % params['name'])
    
    connector.cableguid = params['cableguid']
    p.api.model.racktivity.feed.save(feed)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True