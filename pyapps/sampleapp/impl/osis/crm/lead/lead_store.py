__author__ = 'Incubaid'
__tags__ = 'osis', 'store'
__priority__= 3

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'lead'
DOMAIN = "crm"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, params, tags):
    osis = OsisDB().getConnection('main')

    rootobject = params['rootobject']

    values = {'name': rootobject.name}
    values = {'code': rootobject.code}
    values = {'customerguid': rootobject.customerguid}
    values = {'source': rootobject.source}
    values = {'type': rootobject.type}
    values = {'status': rootobject.status}
    values = {'amount': rootobject.amount}
    values = {'probability': rootobject.probability}

    osis.viewSave(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobject.guid, rootobject.version, values)

    q.logger.log('Saved rootobject %s' % rootobject, 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
