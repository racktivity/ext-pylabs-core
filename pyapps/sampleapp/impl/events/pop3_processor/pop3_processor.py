__author__ = 'Incubaid'
__tags__ = 'osis', 'delete'
__priority__= 3

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'pop3'
DOMAIN = "config"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, params, tags):
    p.api.action.crm.lead.create('test', 'test', 'CBAC660B-BFEC-48AE-A619-620ECF27038D', 'COLDCALL', 'NEWBUSINESS', 'PROSPECTING')

def match(q, i, params, tags):
    import base64
    tags = q.base.tags.getObject( params["eventBody"] )
    return '!@***LEAD***@!' in base64.decodestring(tags.getTag("mail"))
