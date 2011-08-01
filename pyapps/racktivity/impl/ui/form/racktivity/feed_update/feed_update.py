__tags__ = "wizard", "feed_update"
__author__ = "racktivity"

CO2EMISSIONS={'COAL':800, 'GAS':430, 'GENERIC': 217, 'GENERIC_GREEN': 22,'NUCLEAR':6, 'SOLAR':60, 'WIND':3, 'GENERIC_FOSSILE': 615}

def callback_feedType_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    mainTab = form.tabs['main']
    mainTab.elements['co2emission'].value = CO2EMISSIONS[mainTab.elements['feedProductionType'].value]
    return form

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()

    feedguid = params['extra']['rootobjectguid']
    feed = cloudapi.feed.getObject(feedguid)
    tab = form.addTab("main", "Update Feed")
    
    currentCo2emission = max([(k,v) for k, v in feed.co2emission.iteritems()])[1]
    
    tab.addText("feedName", "Name", value=feed.name, optional=False)
    
    feedProductionTypes = dict([(k, k.capitalize()) for k in q.enumerators.feedProductionType._pm_enumeration_items.keys()])
    tab.addChoice("feedProductionType", "Type", feedProductionTypes, selectedValue=str(feed.productiontype), optional=False, trigger="change", callback='feedType_change')
    tab.addMultiline("feedDescription", "Description", value=feed.description)
    tab.addInteger("co2emission", "CO2 Emission (g/Kwh)", minValue=0, optional=False , value=currentCo2emission)
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        #validate data
        tab = form.tabs['main']
        feedname = tab.elements['feedName'].value
        conflictFeeds = cloudapi.feed.find(name = feedname)['result']['guidlist']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        elif conflictFeeds and conflictFeeds[0] != feed.guid:
            tab.elements['feedName'].message = "A feed with the name already exists"
            tab.elements['feedName'].status = "error"
        else:
            valid = True
    tab = form.tabs['main']

    labels = None
    labelsvalue = tab.elements['labels'].value
    if labelsvalue:
        labels = set(labelsvalue.split(','))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in tagsvalue.split(','):
            tagslist = tag.split(':')
            tags[tagslist[0]] = tagslist[1]
    tagstring = q.base.tags.getTagString(labels, tags)

    cloudapi.feed.updateModelProperties(feedguid=feed.guid,
                         name=tab.elements['feedName'].value,
                         datacenterguid=feed.datacenterguid,
                         feedproductiontype=tab.elements['feedProductionType'].value,
                         description=tab.elements['feedDescription'].value,
                         co2emission = float(tab.elements['co2emission'].value),
                         tags=tagstring)
    
    q.gui.dialog.showMessageBox("Feed '%s' is being updated" % tab.elements['feedName'].value, "Update Feed")
    
def main(q, i, p, params, tags):
    return True