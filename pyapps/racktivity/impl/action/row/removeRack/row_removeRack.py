__author__ = 'racktivity'
__tags__ = 'row', 'removeRack'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    rowguid = params['rowguid']
    row = q.drp.row.get(rowguid)
    row.racks.remove(params['rackguid'])
    q.drp.row.save(row)
    
    import racktivityui.uigenerator.row
    racktivityui.uigenerator.row.update(rowguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
