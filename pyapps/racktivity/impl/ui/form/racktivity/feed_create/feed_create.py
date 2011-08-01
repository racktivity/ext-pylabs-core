__tags__ = "wizard", "feed_create"
__author__ = "racktivity"

FEED_CONNECTORS_TAB = 'feedConnectostab'
FEEDS_NUMBER = 'feedsNumber'
CO2EMISSIONS={'COAL':800, 'GAS':430, 'GENERIC': 217, 'GENERIC_GREEN': 22,'NUCLEAR':6, 'SOLAR':60, 'WIND':3, 'GENERIC_FOSSILE': 615}

def callback_numberoffeeds_change(q,i,params,tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    feedstab = form.tabs[FEED_CONNECTORS_TAB]
    buildFeedConnectorsTab(q, feedstab, feedstab.elements[FEEDS_NUMBER].value)
    return form

def callback_feedType_change(q, i, params, tags):
    form = q.gui.form.createForm()
    form.loadForm(params['formData'])
    mainTab = form.tabs['main']
    mainTab.elements['co2emission'].value = CO2EMISSIONS[mainTab.elements['feedProductionType'].value]
    return form

def buildFeedConnectorsTab(q, tab, numberOfFeeds=0):
    #remove old elements
    cache = dict()

    names = [e.name for e in tab.elements]
    
    for name in names:
        if name.startswith("feedconnector-"):
            cache[name] = tab.elements[name].value
        tab.removeElement(name)
            
    tab.addInteger(FEEDS_NUMBER, "Number of feed connectors", minValue=0, value=numberOfFeeds,
                   trigger="change", callback="numberoffeeds_change")
    
    for i in xrange(numberOfFeeds):
        name = "feedconnector-%s-sequence" % i
        tab.addInteger(name, "feed connector %d Sequence" % (i+1), minValue=0)
        if name in cache:
            tab.elements[name].value = cache[name]
        name = "feedconnector-%s-name" % i
        tab.addText(name, "Feed connector %d Label" % (i+1), optional=False)
        if name in cache:
            tab.elements[name].value = cache[name]

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    form = q.gui.form.createForm()
    
    tab = form.addTab("main", "Create Feed")
    tab.addText("feedName", "Name", optional=False)
    feedProductionTypes = dict([(k, k.capitalize()) for k in q.enumerators.feedProductionType._pm_enumeration_items.keys()])
    tab.addChoice("feedProductionType", "Feed Production Type", feedProductionTypes, optional=False, trigger="change", selectedValue='COAL', callback='feedType_change')
    tab.addMultiline("feedDescription", "Feed Description")
    tab.addInteger("co2emission", "CO2 Emission (g/Kwh)", minValue=0, optional=False, value=CO2EMISSIONS['COAL'])
    tab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    feedconnectorstab = form.addTab(FEED_CONNECTORS_TAB, "Feed Connectors")
    buildFeedConnectorsTab(q, feedconnectorstab)
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        #validate data
        tab = form.tabs['main']
        feedName = tab.elements['feedName'].value
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        elif cloudApi.feed.find(name = feedName)['result']['guidlist']:
            tab.elements['feedName'].message = "A feed with the same name already exists"
            tab.elements['feedName'].status = "error"
        else:
            valid = True
    tab = form.tabs['main']
    feedsTab = form.tabs[FEED_CONNECTORS_TAB]
    import re
    import collections
    feeds = collections.defaultdict(dict)
    for element in feedsTab.elements:
        m = re.match("^feedconnector-(\d+)-(.+)$", element.name)
        if m:
            index = int(m.group(1))
            attr = m.group(2)
            if attr == 'sequence':
                feeds[index][attr] = element.value
            else:
                feeds[index][attr] = str(element.value)
            
    for feed in feeds.itervalues():
        feed['status'] = str(q.enumerators.feedConnectorStatusType.NOTCONNECTED)

    labels = None
    labelsvalue = tab.elements['labels'].value
    if labelsvalue:
        labels = set(labelsvalue.split(','))

    tags = collections.defaultdict(dict)
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in tagsvalue.split(','):
            tagslist = tag.split(':')
            tags[tagslist[0]] = tagslist[1]
    tagstring = q.base.tags.getTagString(labels, tags)
    cloudApi.feed.create(name=tab.elements['feedName'].value,
                         feedproductiontype=str(tab.elements['feedProductionType'].value),
                         feedconnectors = feeds.values(),
                         description=tab.elements['feedDescription'].value,
                         co2emission=float(tab.elements['co2emission'].value),
                         tags=tagstring)
    
    q.gui.dialog.showMessageBox("Feed '%s' is being created" % tab.elements['feedName'].value, "Create Feed")
    
def match(q, i, p, params, tags):
    return True
