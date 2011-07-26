__author__ = 'racktivity'

from rootobjectaction_lib import rootobjectaction_find

def getData(q, rootobjecttype, guids):
    objtype = getattr(p.api.model.racktivity, rootobjecttype)
    
    for guid in guids:
        o = objtype.get(guid)
        data = {'guid': guid,
                'name': o.name,
                'type': rootobjecttype,
                'tags': o.tags}
        yield data

def search(q, rootobjecttype, **searchkeys):
    if rootobjecttype:
        guids = rootobjectaction_find.find(rootobjecttype, **searchkeys)
        for obj in getData(q, rootobjecttype, guids):
            yield obj
    else:
        #search all
        for rootobjecttype in ('datacenter', 'room', 'rack', 'meteringdevice', 'device'):
            guids = rootobjectaction_find.find(rootobjecttype, **searchkeys)
            for obj in getData(q, rootobjecttype, guids):
                yield obj
            

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    
    rootobjecttype = params.get('rootobjecttype')
    
    tagsstring = params['tag']
    
    tags = q.base.tags.getObject(tagsstring)
    
    #find at least one keyword to search
    searchkey = ''
    if tags.labels:
        searchkey = list(tags.labels)[0]
    elif tags.tags:
        searchkey = tags.tags.values()[0]
    
    results = list()
    
    if searchkey:
        for match in search(q, rootobjecttype, tags=searchkey):
            tagobj = q.base.tags.getObject(match['tags'])
            skip = False
            for l in tags.labels:
                if l not in tagobj.labels:
                    skip = True
                    break
            for keyvalue in tags.tags.iteritems():
                if keyvalue not in tagobj.tags.items():
                    skip = True
                    break
            if not skip:
                results.append(match)
            
    params['result'] = {'returncode': True,
                        'objects': results}

def match(q, i, params, tags):
    return True
