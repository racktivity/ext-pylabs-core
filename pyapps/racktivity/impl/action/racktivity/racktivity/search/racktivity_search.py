__author__ = 'racktivity'
__tags__ = 'racktivity', 'search'

from rootobjectaction_lib import rootobjectaction_find

rootobjectmap = {'datacenter': rootobjectaction_find.datacenter_find,
                 'room': rootobjectaction_find.room_find,
                 'rack': rootobjectaction_find.rack_find,
                 'meteringdevice': rootobjectaction_find.meteringdevice_find,
                 'device': rootobjectaction_find.device_find}

def getData(q, rootobjecttype, guids):
    objtype = getattr(q.drp, rootobjecttype)
    
    for guid in guids:
        o = objtype.get(guid)
        data = {'guid': guid,
                'name': o.name,
                'type': rootobjecttype,
                'tags': o.tags}
        yield data

def search(q, rootobjecttype, **searchkeys):
    if rootobjecttype:
        if rootobjecttype in rootobjectmap:
            guids = rootobjectmap[rootobjecttype](**searchkeys)
            for obj in getData(q, rootobjecttype, guids):
                yield obj
        else:
            raise ValueError("Invalid rootobject type on (%s) are supported" % rootobjectmap.keys())
    else:
        #search all
        
        for rootobjecttype, find in rootobjectmap.iteritems():
            guids = find(**searchkeys)
            for obj in getData(q, rootobjecttype, guids):
                yield obj
            

def main(q, i, params, tags):
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
