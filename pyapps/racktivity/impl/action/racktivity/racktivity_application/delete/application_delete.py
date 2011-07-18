__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    app = q.drp.racktivity_application.get(params['applicationguid'])
    app.status = str(q.enumerators.applicationstatustype.ABANDONED) #TODELETE
    q.drp.racktivity_application.save(app)
    deleted = q.drp.racktivity_application.delete(params['applicationguid'])
    params['result'] = {'returncode': deleted}

def match(q, i, params, tags):
    return True