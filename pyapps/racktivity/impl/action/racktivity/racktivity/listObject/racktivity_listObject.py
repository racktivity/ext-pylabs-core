__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    filterobj = p.api.model.racktivity.racktivity.getFilterObject()
    
    objects = p.api.model.racktivity.racktivity.findAsView(filterobj, "racktivity_view_racktivity_list")
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
