__tags__ = "wizard", "rack_create"
__author__ = "racktivity"

def getTagString(q, tab):
    labels = None
    labelsvalue = tab.elements['labels'].value
    trim = lambda s: s.strip()
    if labelsvalue:
        labels = set(map(trim, labelsvalue.split(',')))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in map(trim, tagsvalue.split(',')):
            tagslist = tag.split(':')
            tags[tagslist[0].strip()] = tagslist[1].strip()
    return q.base.tags.getTagString(labels, tags)

def main(q, i, p, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    
    floorguid = params['extra'].get('floorguid', "")
    roomguid = params['extra'].get('roomguid', "")
    podguid = params['extra'].get('podguid', "")
    rowguid = params['extra'].get('rowguid', "")
    
    if rowguid:
        row = cloudapi.row.getObject(rowguid)
        podguid = row.pod
    
    if podguid:
        pod = cloudapi.pod.getObject(podguid)
        roomguid = pod.room
        
    if roomguid:
        room = cloudapi.room.getObject(roomguid)
        floorguid = room.floor
    
    if not floorguid:
        raise RuntimeError("No floor guid is provided")
    
    form = q.gui.form.createForm()
    
    tab = form.addTab("main", "Create Rack")
    tab.addText("rackName", "Name", optional=False)
    
    rackTypes = dict([(k, k.capitalize()) for k in q.enumerators.racktype._pm_enumeration_items.keys()])
    tab.addChoice("rackType", "Type", rackTypes, optional=False)
    tab.addMultiline("rackDescription", "Description")
    tab.addInteger("rackHeight", "Rack Height (U)", minValue=1, value=42)
    tab.addText("rackCorridor", "Corridor", optional=False)
    tab.addText("rackCorridorPosition", "Corridor Position", optional=False)
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        #validate data
        tab = form.tabs['main']
        rackname = tab.elements['rackName'].value
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        elif cloudapi.rack.find(name = rackname, height=None)['result']['guidlist']:
            tab.elements['rackName'].message = "A rack with the same name already exists"
            tab.elements['rackName'].status = "error"
        else:
            valid = True
    tab = form.tabs['main']
    
    tagstring = getTagString(q, tab)
    
    rackguid = cloudapi.rack.create(roomguid=roomguid,
                         floor=floorguid,
                         name=tab.elements['rackName'].value,
                         racktype=tab.elements['rackType'].value,
                         description=tab.elements['rackDescription'].value,
                         corridor=tab.elements['rackCorridor'].value,
                         position=tab.elements['rackCorridorPosition'].value,
                         height=tab.elements['rackHeight'].value,
                         tags=tagstring)['result']['rackguid']
    
    if rowguid:
        #add rack to row.
        cloudapi.row.addRack(rowguid, rackguid)
    elif podguid:
        cloudapi.pod.addRack(podguid, rackguid)
        
    q.gui.dialog.showMessageBox("Rack '%s' has been created" % tab.elements['rackName'].value, "Create Rack")
    
def main(q, i, p, params, tags):
    return True