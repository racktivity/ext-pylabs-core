import os.path

from pylabs import q, p

from alkira.lfw import *

basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)

def getNodeEnterprise(api, guid):
    action = p.api.action.racktivity
    resutls = []
    for location in action.location.list()['result']['locationinfo']:
        resutls.append({'state':  "closed",
                        'data': location['name'],
                        'attr': {'id': location['guid'],
                                 'rel': 'location'}})
    return resutls

def getNodeLocation(api, guid):
    action = p.api.action.racktivity
    results = []
    for dc in action.datacenter.list(locationguid=guid)['result']['datacenterinfo']:
        results.append({'state':  "closed",
                        'data': dc['name'],
                        'attr': {'id': dc['guid'],
                                 'rel': 'datacenter'}})
    
    return results

def getNodeDatacenter(api, guid):
    action = p.api.action.racktivity
    results = []
    for floor in action.floor.list(datacenterguid=guid)['result']['floorinfo']:
        results.append({'state':  "closed",
                        'data': floor['name'],
                        'attr': {'id': floor['guid'],
                                 'rel': 'floor'}})
    
    return results

def getNodeFloor(api, guid):
    #floor can hold a room or a rack so both are listed.
    #but only racks can exist if floor doesn't have rooms.
    action = p.api.action.racktivity
    results = []
    for roomguid in action.room.find(floorguid=guid)['result']['guidlist']:
        room = action.room.getObject(roomguid)
        results.append({'state':  "closed",
                        'data': room.name,
                        'attr': {'id': roomguid,
                                 'rel': 'room'}})
    if not results:
        for rackguid in action.rack.find(floorguid=guid)['result']['guidlist']:
            rack = action.rack.getObject(rackguid)
            results.append({'state':  "closed",
                            'data': rack.name,
                            'attr': {'id': rackguid,
                                     'rel': 'rack'}})
    
    return results

def getNodeRoom(api, guid):
    #room can hold pod, row or rack 
    #if room has pods, both row and rack wizards are dropped 
    action = p.api.action.racktivity
    results = []
    for pod in action.pod.list(roomguid=guid)['result']['podinfo']:
        results.append({'state':  "closed",
                        'data': pod['name'],
                        'attr': {'id': pod['guid'],
                                 'rel': 'pod'}})
    if not results:
        for row in action.row.list(roomguid=guid)['result']['rowinfo']:
            results.append({'state':  "closed",
                            'data': row['name'],
                            'attr': {'id': row['guid'],
                                     'rel': 'row'}})
    if not results:
        for rackguid in action.rack.find(roomguid=guid)['result']['guidlist']:
            rack = action.rack.getObject(rackguid)
            results.append({'state':  "closed",
                            'data': rack.name,
                            'attr': {'id': rackguid,
                                     'rel': 'rack'}})
    return results

def getNodePod(api, guid):
    #same as room, it can hold row or rack but no more racks after creating the first row
    action = p.api.action.racktivity
    results = []
    for row in action.row.list(podguid=guid)['result']['rowinfo']:
        results.append({'state':  "closed",
                        'data': row['name'],
                        'attr': {'id': row['guid'],
                                 'rel': 'row'}})
    if not results:
        for rackguid in action.rack.find(podguid=guid)['result']['guidlist']:
            rack = action.rack.getObject(rackguid)
            results.append({'state':  "closed",
                            'data': rack.name,
                            'attr': {'id': rackguid,
                                     'rel': 'rack'}})
    return results

def getNodeRow(api, guid):
    #only racks are allowed.
    action = p.api.action.racktivity
    results = []

    for rackguid in action.rack.find(rowguid=guid)['result']['guidlist']:
        rack = action.rack.getObject(rackguid)
        results.append({'state':  "closed",
                        'data': rack.name,
                        'attr': {'id': rackguid,
                                 'rel': 'rack'}})
        
    return results

def getNodeRack(api, guid):
    action = p.api.action.racktivity
    results = []
    
    for mdguid in action.meteringdevice.find(rackguid=guid, id="M1")['result']['guidlist']:
        md = action.meteringdevice.getObject(mdguid)
        results.append({'state':  "leaf",
                        'data': md.name,
                        'attr': {'id': mdguid,
                                 'rel': 'meteringdevice'}})
    return results

NODESMAP = {'enterprise': getNodeEnterprise,
            'location': getNodeLocation,
            'datacenter': getNodeDatacenter,
            'floor': getNodeFloor,
            'room': getNodeRoom,
            'pod': getNodePod,
            'row': getNodeRow,
            'rack': getNodeRack}

class portal(LFWService):

    _authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
    _authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))

    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        q.logger.log("HEADERS from portal.checkAuthentication %s" % str(request._request.requestHeaders))
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        self._authenticate.execute(params, tags=tags)
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True

        # Normally this part isn't needed because we have the Auth service but because we cannot call the service
        # from inside the authorize tasklet (because this is implemented in the main thread of the appserver).
        # So we just do the same as the Auth service is doing and then use the backend directly.
        tags += ('authbackend', )
        params['authbackend'] = self.authBackend


        self._authorize.execute(params, tags=tags)
        return params.get('result', False)
    
    @q.manage.applicationserver.expose
    def getNode(self, id="."):
        action = p.api.action.racktivity
        
        results = []
        if not id:
            raise RuntimeError("Invalid ID")
        
        if id == ".":
            enterprises = action.enterprise.list()['result']['enterpriseinfo']
            for enterprise in enterprises:
                
                results.append({"state": "closed",
                                "data": enterprise['name'],
                                "attr": {"id": enterprise['guid'],
                                         "rel": "enterprise"}})
        else:
            #get id parts.
            type, _, guid = id.partition(":")
            results = NODESMAP[type](p.api, guid)
        
        return results