__author__ = 'racktivity'
__tags__ = 'racktivity', 'updateModelProperties'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    q.logger.log('Updating racktivity properties in the model', 3)
    fields = ('sw_version', 'smtp', 'smtplogin', 'smtppassword', 'configured', 'tags')
    racktivity = q.drp.racktivity.get(params['racktivityguid'])
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(racktivity, key, value)
            changed = True
    if changed:
        q.logger.log_tasklet(__tags__, params, fields, nameKey = "sw_version")
        q.drp.racktivity.save(racktivity)

    params['result'] = {'returncode': True, 'racktivityguid': racktivity.guid}

def match(q, i, params, tags):
    return True
