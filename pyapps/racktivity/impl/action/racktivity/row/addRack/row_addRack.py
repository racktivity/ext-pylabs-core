__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    rowguid = params['rowguid']
    rackguid = params['rackguid']
    row = p.api.model.racktivity.row.get(rowguid)
    if rackguid in row.racks:
        raise ValueError("The rack already exists in the given row")
    from rootobjectaction_lib import rootobjectaction_list
    if not rootobjectaction_list.rack_list(rackguid=rackguid):
        raise ValueError("Rack with guid %s is not found in the system"%rackguid)
    row.racks.append(rackguid)
    p.api.model.racktivity.row.save(row)
    p.api.action.racktivity.rack.uiCreatePageUnderParent(rackguid, rowguid)

    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
