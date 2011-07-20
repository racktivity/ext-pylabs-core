__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name':root.name, 
                   'description': root.description, 
                   'address': root.address, 
                   'netmask':root.netmask, 
                   'block':root.block, 
                   'iptype':root.iptype, 
                   'ipversion':root.ipversion, 
                   'languid':root.languid,
                   'status':root.status,
                   'virtual':root.virtual,
                   'tags':root.tags}

    osis.viewSave(params['domain'], 'ipaddress', viewname, root.guid, root.version, fields)
    q.logger.log('ipaddress saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'ipaddress'
