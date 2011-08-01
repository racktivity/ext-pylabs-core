__tags__ = "wizard", "floor_update"
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
    cloudApi = p.api.action.racktivity
    form = q.gui.form.createForm()
    floorguid = params['extra']['floorguid']
    floor = cloudApi.floor.getObject(floorguid)
    tab = form.addTab("mainTab", "Update Floor")
    tab.addText("name", "Name", optional=False, message="Please enter the floor name", value=floor.name)
    tab.addInteger('floor', 'Floor', message='Please enter the floor number', optional=False, value=floor.floor)
    tab.addText("alias", "Alias", optional=True, message="Please enter the floor alias name", value=floor.alias)
    tab.addMultiline("description", "Description", optional=True, message="Please enter the floor description", value=floor.description)
    tagobj = q.base.tags.getObject(floor.tags or '')
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
    
    cloudApi.floor.updateModelProperties(floorguid, name=tab.elements['name'].value,
                                         floor=tab.elements['floor'].value,
                                         alias=tab.elements['alias'].value,
                                         description=tab.elements['description'].value,
                                         tags=tagstring)

    q.gui.dialog.showMessageBox("Floor '%s' is being updated" % tab.elements['name'].value, "Create Floor")

def main(q, i, p, params, tags):
    return True