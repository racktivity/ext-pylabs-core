__author__ = 'Incubaid'
__tags__ = 'osis', 'delete'
__priority__= 3

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'lead'
DOMAIN = "crm"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)

    rootobjectguid = params['rootobjectguid']
    rootobjectversionguid = params['rootobjectversionguid']

    osis.viewDelete(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobjectguid, rootobjectversionguid)

    q.logger.log('Deleted rootobject of type %s and guid %s from domain %s' % (ROOTOBJECT_TYPE, rootobjectguid, DOMAIN), 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
