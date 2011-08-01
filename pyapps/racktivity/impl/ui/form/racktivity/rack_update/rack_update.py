__tags__ = "wizard", "rack_update"
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
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()
    
    rackguid = params['extra']['rootobjectguid']
    rack = cloudapi.rack.getObject(rackguid)
    tab = form.addTab("main", "Create Rack")
    
    tab.addText("rackName", "Name", value=rack.name, optional=False)
    
    rackTypes = dict([(k, k.capitalize()) for k in q.enumerators.racktype._pm_enumeration_items.keys()])
    tab.addChoice("rackType", "Type", rackTypes, selectedValue=str(rack.racktype), optional=False)
    tab.addMultiline("rackDescription", "Description", value=rack.description)
    tab.addInteger("rackHeight", "Rack Height (U)", minValue=1, value=rack.height)
    tab.addText("rackCorridor", "Corridor", optional=False, value=rack.corridor)
    tab.addText("rackCorridorPosition", "Corridor Position", optional=False, value=rack.position)
    
    tagobj = q.base.tags.getObject(rack.tags or '')
    tab.addText('tags', 'Tags', value=",".join(["%s:%s" % (k, v) for k, v in tagobj.tags.iteritems()]),
                helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', value=",".join(tagobj.labels),
                helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        #validate data
        tab = form.tabs['main']
        rackname = tab.elements['rackName'].value
        conflictRacks = cloudapi.rack.find(name = rackname, height=None)['result']['guidlist']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        elif conflictRacks and conflictRacks[0] != rack.guid:
            tab.elements['rackName'].message = "A rack with the same name already exists"
            tab.elements['rackName'].status = "error"
        else:
            valid = True
    tab = form.tabs['main']
    
    tagstring = getTagString(q, tab)
    
    cloudapi.rack.updateModelProperties(rackguid=rack.guid,
                         name=tab.elements['rackName'].value,
                         racktype=tab.elements['rackType'].value,
                         description=tab.elements['rackDescription'].value,
                         corridor=tab.elements['rackCorridor'].value,
                         position=tab.elements['rackCorridorPosition'].value,
                         height=tab.elements['rackHeight'].value,
                         tags=tagstring)
    
    q.gui.dialog.showMessageBox("Rack '%s' is being updated" % tab.elements['rackName'].value, "Update Rack")
    
def main(q, i, p, params, tags):
    return True