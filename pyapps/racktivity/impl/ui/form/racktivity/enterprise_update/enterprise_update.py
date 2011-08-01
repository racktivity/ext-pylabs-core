__author__ = 'racktivity'

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
    enterpriseguid = params['extra']['enterpriseguid']
    enterprise = cloudapi.enterprise.getObject(enterpriseguid)
    
    form = q.gui.form.createForm()
    
    enterprisetab = form.addTab('enterprise', 'Enterprise')
    enterprisetab.addText('name', 'Name', value=enterprise.name, message='Please enter the enterprise name', optional=False)
    enterprisetab.addMultiline('description', 'Description', value=enterprise.description, message='Please enter the enterprise description')
    tagobj = q.base.tags.getObject(enterprise.tags or '')
    enterprisetab.addText('tags', 'Tags',  value=",".join(["%s:%s" % (k, v) for k, v in tagobj.tags.iteritems()]),
                helpText='Enter tags in the form of tag1:value1,tag2:value2')
    enterprisetab.addText('labels', 'Labels', value=",".join(tagobj.labels),
                helpText='Enter labels as comma separated values e.g. label1,label2')
    
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        enterprisetab = form.tabs['enterprise']
        enterprisetags = enterprisetab.elements['tags'].value
        if enterprisetags and ':' not in enterprisetags:
            enterprisetab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            enterprisetab.elements['tags'].status = 'error'
        else:
            valid = True
    
    enterprisetab = form.tabs['enterprise']
    tagstring = getTagString(q, enterprisetab)

    cloudapi.enterprise.create(name=enterprisetab.elements['name'].value,
                               description=enterprisetab.elements['description'].value,
                               campuses=enterprise.campuses,
                               tags=tagstring)

    q.gui.dialog.showMessageBox('enterprise "%s" is being updated' % enterprisetab.elements['name'].value, "Update enterprise")

def main(q, i, p, params, tags):
    return True