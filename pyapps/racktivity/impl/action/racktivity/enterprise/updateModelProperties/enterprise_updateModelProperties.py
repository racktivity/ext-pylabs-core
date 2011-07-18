__author__ = 'racktivity'
__tags__ = 'enterprise', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating enterprise properties in the model', 3)
    enterprise = q.drp.enterprise.get(params['enterpriseguid'])
    fields = ('name', 'description', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(enterprise, key, value)
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.enterprise.save(enterprise)
    
    import racktivityui.uigenerator.enterprise
    racktivityui.uigenerator.enterprise.update()
    
    
    params['result'] = {'returncode': True,
                        'enterpriseguid': enterprise.guid}

def match(q, i, params, tags):
    return True
