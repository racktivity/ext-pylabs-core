
def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain'] 
    p.events.publish('pylabs.event.racktivity.osis.store.%s.%s' % (domain, root.PYMODEL_MODEL_INFO.name), root.guid)
