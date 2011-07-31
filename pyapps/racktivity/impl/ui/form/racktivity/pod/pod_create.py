__author__ = 'racktivity'
__tags__ = 'wizard', 'pod_create'


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

def main(q, i, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Create Pod')
    tab.addText('name', 'Name', message='Please enter the pod name', optional=False)
    tab.addText('alias', 'Alias', message='Please enter the pod alias')
    tab.addMultiline('description', 'Description', message='Please enter the pod description')
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
    tagstring = getTagString(q, tab)

    podguid = cloudapi.pod.create(name=tab.elements['name'].value,
                               description=tab.elements['description'].value,
                               alias=tab.elements['alias'].value,
                               room=room,
                               tags=tagstring)['result']['podguid']
    
    allpods = cloudapi.pod.find(room=room)['result']['guidlist']
    
    if len(allpods) == 1: #only the new pod available.
        for rackguid in cloudapi.rack.find(roomguid=room)['result']['guidlist']:
            cloudapi.pod.addRack(podguid, rackguid)
    
    q.gui.dialog.showMessageBox('Pod "%s" is being created' % tab.elements['name'].value, "Create Pod")

def match(q, i, params, tags):
    return True