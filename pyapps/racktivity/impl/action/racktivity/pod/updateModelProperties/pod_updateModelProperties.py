__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating pod properties in the model', 3)
    pod = p.api.model.racktivity.pod.get(params['podguid'])
    fields = ('name', 'alias', 'description', 'roomguid', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(pod, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.pod.save(pod)
    
    #import racktivityui.uigenerator.pod
    #racktivityui.uigenerator.pod.update(pod.guid)
    #import racktivityui.uigenerator.room
    #racktivityui.uigenerator.room.update(pod.room)
    
    params['result'] = {'returncode': True,
                        'podguid': pod.guid}

def match(q, i, params, tags):
    return True
