
def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain'] 
    p.events.publish('pylabs.event.%s.osis.store.%s.%s' % ( p.api.appname, domain, root.PYMODEL_MODEL_INFO.name), root.guid)
