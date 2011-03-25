__author__ = 'Incubaid'
__tags__ = 'osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'customer'
DOMAIN = "crm"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)

    rootobject = params['rootobject']

    values = {'name': rootobject.name}

    osis.viewSave(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobject.guid, rootobject.version, values)

    q.logger.log('Saved rootobject %s' % rootobject, 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
