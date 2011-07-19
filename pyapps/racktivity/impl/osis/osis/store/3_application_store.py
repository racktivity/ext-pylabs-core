__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    parentapps = root.parentapplicationguids
    parentstr = ""
    if parentapps:
        parentstr = ",".join(parentapps)
    osis.viewSave(params['domain'], 'application', viewname, root.guid, root.version, {'name'                  :root.name, \
                                                                                    'description'           :root.description, \
                                                                                    'status'                :str(root.status), \
                                                                                    'template'              :root.template, \
                                                                                    'applicationtemplateguid':root.applicationtemplateguid, \
                                                                                    'machineguid'           :root.machineguid, \
                                                                                    'meteringdeviceguid'    :root.meteringdeviceguid, \
                                                                                    'customsettings'        :root.customsettings, \
                                                                                    'meteringdeviceguid'    :root.meteringdeviceguid, \
                                                                                    'parentapplicationguids':parentstr,
                                                                                    'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()),
                                                                                    'tags'                   :root.tags})
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'application'
