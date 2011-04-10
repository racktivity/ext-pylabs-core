__author__ = 'incubaid'
__tags__ ='osis', 'delete'
__priority__= 3

def main(q, i, p, params, tags):
    rootobjecttype = params['rootobjecttype']
    rootobjectguid = params['rootobjectguid']
    domain = params['domain'] 
    p.events.publish('pylabs.event.sampleapp.osis.delete.%s.%s' % (domain, rootobjecttype), rootobjectguid)
