
def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain'] 
    appname = '$appname'
    p.events.publish('pylabs.event.%s.osis.store.%s.%s' % ( appname, domain, root.PYMODEL_MODEL_INFO.name), root.guid)
