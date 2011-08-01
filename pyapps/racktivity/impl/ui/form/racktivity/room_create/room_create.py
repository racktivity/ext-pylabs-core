__tags__ = "wizard", "room_create"
__author__ = "racktivity"

ROOM_NAME_HELP = "Please enter a valid room name"
ROOM_FLOOR_HELP = "Please enter a valid floor. Valid values are characters from 0 to 9"
ROOM_ALIAS_HELP = "Please enter a room alias name"

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
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()
    
    tab = form.addTab("mainTab", "Create Room")
    tab.addText("ractivity_roomname", "Room Name", optional=False, helpText=ROOM_NAME_HELP)
    tab.addText("ractivity_alias", "Room Alias", optional=True, helpText=ROOM_ALIAS_HELP)
    tab.addMultiline("ractivity_desc", "Room Description", optional=True)
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['mainTab']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True

    datacenterguid = params['extra']['datacenterguid']
    floorguid = params['extra'].get('floorguid', "")
    
    tagstring = getTagString(q, tab)

    roomguid = cloudapi.room.create(name=tab.elements['ractivity_roomname'].value,
                         datacenterguid=datacenterguid,
                         floor=floorguid,
                         alias=tab.elements['ractivity_alias'].value,
                         description=tab.elements['ractivity_desc'].value,
                         tags=tagstring)['result']['roomguid']
    if floorguid:
        for rackguid in cloudapi.rack.find(floor=floorguid)['result']['guidlist']:
            rack = cloudapi.rack.getObject(rackguid)
            if not rack.roomguid: #move all racks that doesn't belong to a room to this room.
                cloudapi.rack.updateModelProperties(rackguid, roomguid=roomguid)
                cloudapi.rack.uiCreatePageUnderParent(rackguid, roomguid)
        cloudapi.room.updateModelProperties(roomguid)
        
    q.gui.dialog.showMessageBox("Room '%s' is being created" % tab.elements['ractivity_roomname'].value, "Create Room")
    
def match(q, i, p, params, tags):
    return True
