__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    app = p.api.model.racktivity.application.get(params['applicationguid'])
    app.status = str(q.enumerators.applicationstatustype.ABANDONED) #TODELETE
    p.api.model.racktivity.application.save(app)
    deleted = p.api.model.racktivity.application.delete(params['applicationguid'])
    params['result'] = {'returncode': deleted}

def match(q, i, params, tags):
    return True