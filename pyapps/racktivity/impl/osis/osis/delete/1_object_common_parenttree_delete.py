__author__ = 'racktivity'
__tags__ ='osis', 'delete'

def main(q, i, params, tags):
    """
    Delete tree entry in parenttree table
    """
    osis = p.application.getOsisConnection(p.api.appname)
    osis.viewDelete(params['domain'], 'public', 'parenttree', params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] in ("rack", "pod", "row", "room", "floor", "datacenter", "location", "meteringdevice", "device", "enterprise")
