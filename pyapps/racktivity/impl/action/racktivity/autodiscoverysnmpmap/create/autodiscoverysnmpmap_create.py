__author__ = 'aserver'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "manufacturer")
    from rootobjectaction_lib import rootobjectaction_find
    if rootobjectaction_find.exists('racktivity_view_autodiscoverysnmpmap_list', p.api.model.racktivity.autodiscoverysnmpmap, "manufacturer", params['manufacturer']):
        raise ValueError("manufacturer %s already exists"%params['manufacturer'])
    if rootobjectaction_find.exists('racktivity_view_autodiscoverysnmpmap_list', p.api.model.racktivity.autodiscoverysnmpmap, "sysobjectid", params['sysobjectid']):
        raise ValueError("the sysobjectid %s already exists"%params['sysobjectid'])
    
    fields = ('manufacturer', 'sysobjectid', 'oidmapping', 'tags')
    autodiscoverysnmpmap = p.api.model.racktivity.autodiscoverysnmpmap.new()
    for key, value in params.iteritems():
        if key in fields and value is not None:
            setattr(autodiscoverysnmpmap, key, value)
    p.api.model.racktivity.autodiscoverysnmpmap.save(autodiscoverysnmpmap)
    params['result'] = {'returncode': True,'autodiscoverysnmpmapguid': autodiscoverysnmpmap.guid}

def match(q, i, params, tags):
    return True
