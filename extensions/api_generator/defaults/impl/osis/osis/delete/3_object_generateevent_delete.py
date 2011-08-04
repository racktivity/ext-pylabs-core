
def main(q, i, p, params, tags):
    guid = params['rootobjectguid']
    type = params['rootobjecttype']
    domain = params['domain'] 
    p.events.publish('pylabs.event.%s.osis.delete.%s.%s' % (p.api.appname, domain, type), guid)
