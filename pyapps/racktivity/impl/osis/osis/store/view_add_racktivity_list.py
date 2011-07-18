__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    fields = {'sw_version': root.sw_version, 'smtp': root.smtp, 'smtplogin': root.smtplogin,
              'smtppassword': root.smtppassword, 'configured': root.configured, \
              'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    osis.viewSave('racktivity', 'view_racktivity_list', root.guid, root.version, fields)
    q.logger.log('Racktivity rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'racktivity'
