__author__ = 'racktivity'
__tags__ = 'feed', 'connectConnector'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    feed = q.drp.feed.get(feedguid)
    connector = None
    for c in feed.feedconnectors:
        if c.name == params['name']:
            connector = c
            break
    
    if not connector:
        raise ValueError("Can't find connector with name '%s'" % params['name'])
    
    connector.cableguid = params['cableguid']
    q.drp.feed.save(feed)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True