__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'sw_version': root.sw_version, 'smtp': root.smtp, 'smtplogin': root.smtplogin,
              'smtppassword': root.smtppassword, 'configured': root.configured, \
              'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()), 'tags': root.tags}
    osis.viewSave(params['domain'], 'racktivity', viewname, root.guid, root.version, fields)
    q.logger.log('Racktivity rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'racktivity'
