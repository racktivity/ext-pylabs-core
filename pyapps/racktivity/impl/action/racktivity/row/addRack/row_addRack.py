__author__ = 'racktivity'
__tags__ = 'row', 'addRack'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    rowguid = params['rowguid']
    rackguid = params['rackguid']
    row = q.drp.row.get(rowguid)
    if rackguid in row.racks:
        raise ValueError("The rack already exists in the given row")
    from rootobjectaction_lib import rootobjectaction_list
    if not rootobjectaction_list.rack_list(rackguid=rackguid):
        raise ValueError("Rack with guid %s is not found in the system"%rackguid)
    row.racks.append(rackguid)
    q.drp.row.save(row)
    q.actions.rootobject.rack.uiCreatePageUnderParent(rackguid, rowguid)
    import racktivityui.uigenerator.row
    racktivityui.uigenerator.row.update(rowguid)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
