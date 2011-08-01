__tags__ = "wizard", "room_update"
__author__ = "racktivity"

ROOM_NAME_HELP = "Please enter a valid room name"
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
    cloudApi = i.config.cloudApiConnection.find('main')
    form = q.gui.form.createForm()
    roomguid = params['extra']['roomguid']
    room = cloudApi.room.getObject(roomguid)
    tab = form.addTab("mainTab", "Update Room")
    tab.addText("ractivity_roomname", "Room Name", optional=False, helpText=ROOM_NAME_HELP, value=room.name)
    tab.addText("ractivity_alias", "Room Alias", optional=True, helpText=ROOM_ALIAS_HELP, value=room.alias)
    tab.addMultiline("ractivity_desc", "Room Description", optional=True, value=room.description)
    
    tagobj = q.base.tags.getObject(room.tags or '')
    tab.addText('tags', 'Tags', value=",".join(["%s:%s" % (k, v) for k, v in tagobj.tags.iteritems()]),
                helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', value=",".join(tagobj.labels),
                helpText='Enter labels as comma separated values e.g. label1,label2')

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
            
    tagstring = getTagString(q, tab)
    
    cloudApi.room.updateModelProperties(roomguid, name=tab.elements['ractivity_roomname'].value,
                                         alias=tab.elements['ractivity_alias'].value,
                                         description=tab.elements['ractivity_desc'].value,
                                         tags=tagstring)

    q.gui.dialog.showMessageBox("Room '%s' is being updated" % tab.elements['ractivity_roomname'].value, "Create Room")

def main(q, i, p, params, tags):
    return True