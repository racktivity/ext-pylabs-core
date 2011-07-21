__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating row properties in the model', 3)
    row = p.api.model.racktivity.row.get(params['rowguid'])
    fields = ('name', 'alias', 'description', 'room', 'pod', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(row, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.row.save(row)
    
    #import racktivityui.uigenerator.row
    #racktivityui.uigenerator.row.update(row.guid)
    #import racktivityui.uigenerator.pod
    #racktivityui.uigenerator.pod.update(row.pod)
    
    params['result'] = {'returncode': True,
                        'rowguid': row.guid}

def match(q, i, params, tags):
    return True
