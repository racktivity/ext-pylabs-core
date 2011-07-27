__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating enterprise properties in the model', 3)
    enterprise = p.api.model.racktivity.enterprise.get(params['enterpriseguid'])
    fields = ('name', 'description', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(enterprise, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.enterprise.save(enterprise)


    params['result'] = {'returncode': True,
                        'enterpriseguid': enterprise.guid}

def match(q, i, params, tags):
    return True
