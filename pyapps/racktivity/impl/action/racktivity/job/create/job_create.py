__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    q.logger.log('Creating the new job in the model', 3)
    job = p.api.model.racktivity.job.new()

    p.api.model.racktivity.job.save(job)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(job.guid, 'job', params['request']['username'])

    params['result'] = {'returncode': True,
                        'jobguid': job.guid}

def match(q, i, params, tags):
    return True
