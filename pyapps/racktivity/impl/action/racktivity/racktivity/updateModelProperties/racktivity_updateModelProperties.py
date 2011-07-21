__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    q.logger.log('Updating racktivity properties in the model', 3)
    fields = ('sw_version', 'smtp', 'smtplogin', 'smtppassword', 'configured', 'tags')
    racktivity = p.api.model.racktivity.racktivity.get(params['racktivityguid'])
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(racktivity, key, value)
            changed = True
    if changed:
        q.logger.log_tasklet(__tags__, params, fields, nameKey = "sw_version")
        p.api.model.racktivity.racktivity.save(racktivity)

    params['result'] = {'returncode': True, 'racktivityguid': racktivity.guid}

def match(q, i, params, tags):
    return True
