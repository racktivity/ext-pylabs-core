__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    ipaddress = p.api.model.racktivity.ipaddress.new()
    ipaddress.iptype = q.enumerators.iptype.STATIC
    ipaddress.ipversion = q.enumerators.ipversion.IPV4
    ipaddress.block = False
    fields = ('name', 'description', 'address', 'netmask', 'block', 'iptype', 
              'ipversion', 'languid', 'virtual', 'tags')

    from rootobjectaction_lib import rootobjectaction_find
    if rootobjectaction_find.ipaddress_find(name=params['name']):
        raise ValueError('An IP address with the name %s already exists'%params['name'])
    
    for key, value in params.iteritems():
        if key in fields and value:
            if key == 'address':
                if not q.system.net.validateIpAddress(value):
                    raise ValueError('Invalid IP address')
            setattr(ipaddress, key, value)

    p.api.model.racktivity.ipaddress.save(ipaddress)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(ipaddress.guid, 'ipaddress', params['request']['username'])

    params['result'] = {'returncode': True,
                        'ipaddressguid': ipaddress.guid}

def match(q, i, params, tags):
    return True
