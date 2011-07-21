__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    rowguid = params['rowguid']
    row = p.api.model.racktivity.row.get(rowguid)
    row.racks.remove(params['rackguid'])
    p.api.model.racktivity.row.save(row)
    
    #import racktivityui.uigenerator.row
    #racktivityui.uigenerator.row.update(rowguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
