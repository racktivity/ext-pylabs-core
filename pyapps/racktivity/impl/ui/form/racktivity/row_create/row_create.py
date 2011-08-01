__author__ = 'racktivity'
__tags__ = 'wizard', 'row_create'


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
    tab = form.addTab('main', 'Create Row')
    tab.addText('name', 'Name', message='Please enter the row name', optional=False)
    tab.addText('alias', 'Alias', message='Please enter the row alias')
    tab.addMultiline('description', 'Description', message='Please enter the row description')
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True

    room = params['extra']['room']
    pod = params['extra']['pod']
    tagstring = getTagString(q, tab)

    rowguid = cloudapi.row.create(name=tab.elements['name'].value,
                               description=tab.elements['description'].value,
                               alias=tab.elements['alias'].value,
                               room=room,
                               pod=pod,
                               tags=tagstring)['result']['rowguid']

    allrows = cloudapi.row.find(pod=pod)['result']['guidlist']
    
    if len(allrows) == 1: #only the new row available.
        podobj = cloudapi.pod.getObject(pod)
        for rackguid in podobj.racks:
            cloudapi.pod.removeRack(pod, rackguid)
            cloudapi.row.addRack(rowguid, rackguid)

    q.gui.dialog.showMessageBox('Row "%s" is being created' % tab.elements['name'].value, "Create Row")

def main(q, i, p, params, tags):
    return True