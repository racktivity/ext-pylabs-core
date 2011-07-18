__author__ = 'racktivity'
__tags__ = 'racktivity', 'listObject'

def main(q, i, params, tags):
    params['result'] = {'returncode': False}
    filterobj = q.drp.racktivity.getFilterObject()
    
    objects = q.drp.racktivity.findAsView(filterobj, "view_racktivity_list")
    for obj in objects:
        for k in ('viewguid', 'version'):
            del obj[k]
    
    if objects:
        params['result'] = {'returncode': True,
                            'racktivityinfo': objects[0]}
    else:
        params['result'] = {'returncode': False,
                            'racktivityinfo': None}

def match(q, i, params, tags):
    return True
