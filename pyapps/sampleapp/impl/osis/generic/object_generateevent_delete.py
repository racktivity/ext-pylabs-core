__author__ = 'incubaid'
__tags__ ='osis', 'delete'
__priority__= 3

def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain'] 
    p.events.publish('pylabs.event.sampleapp.osis.delete.%s.%s' % (domain, root.PYMODEL_MODEL_INFO.name), root.guid)
    