__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    
    from rootobjectaction_lib import rootobjectaction_find
    if rootobjectaction_find.enterprise_find():
        raise RuntimeError("Can't create more than one enterprise object")

    fields = ('name', 'description', 'tags')
    enterprise = p.api.model.racktivity.enterprise.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(enterprise, key, value)
    
    from rootobjectaction_lib import rootobjectaction_list
    for campus in params['campuses']:
        if not rootobjectaction_list.location_list(campus):
            raise ValueError("Campus with guid %s is not found in the system" % campus)
        enterprise.campuses.append(campus)
    acl = enterprise.acl.new()
    enterprise.acl = acl
    p.api.model.racktivity.enterprise.save(enterprise)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(enterprise.guid, 'enterprise', params['request']['username'])

    params['result'] = {'returncode': True,
                        'enterpriseguid': enterprise.guid}

    #import racktivityui.uigenerator.enterprise
    #racktivityui.uigenerator.enterprise.update()

def match(q, i, params, tags):
    return True
