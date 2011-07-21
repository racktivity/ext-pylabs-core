__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    
    feed = p.api.model.racktivity.feed.get(feedguid)
    for feedconnector in feed.feedconnectors:
        if feedconnector.name == params['name']:
            raise ValueError('Connector name must be unique within the module')

    connectorfields = ('name', 'sequence', 'status')
    feedconnector = feed.feedconnectors.new()
    for key, value in params.iteritems():
        if key in connectorfields and value:
            setattr(feedconnector, key, value)
    
    if not feedconnector.sequence:
        maxsequence = 0
        for p in feed.feedconnectors:
            maxsequence = max(p.sequence, maxsequence)
        feedconnector.sequence = maxsequence + 1
    
    if feedconnector.sequence <= 0:
        raise RuntimeError("Sequence must be 1 or more")
    
    #validate the sequence and the label
    for p in feed.feedconnectors:
        if feedconnector.sequence == p.sequence:
            raise RuntimeError("Sequence '%s' is already taken by another feedconnector" % feedconnector.sequence)
        
    feed.feedconnectors.append(feedconnector)
    p.api.model.racktivity.feed.save(feed)

    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True