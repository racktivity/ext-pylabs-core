__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_update'

from pymonkey.pmtypes import IPv4Range, IPv4Address

REGEX_IP4ADDRESS_VALIDATOR = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def callback_updateAccount(q, i, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    meteringdeviceguid = params['SESSIONSTATE']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    formData = params['formData']
    form.loadForm(formData)
    tab = form.tabs['main']
    oldlogin = None
    oldpassword = None
    for account in meteringdevice.accounts:
        if account.guid == tab.elements['account'].value:
            oldlogin = account.login
            oldpassword = account.password
            break

    tab.addText('login', 'Login', value=oldlogin)
    tab.addPassword('password', 'Password', value=oldpassword)
    tab.addPassword('password-validation', 'Confirm Password', value=oldpassword)
    return form

def connectFeed(q, cloudapi, feedguid, mdguid):
    md = cloudapi.meteringdevice.getObject(mdguid)
    for powerinput in md.powerinputs:
        cableguid = powerinput.cableguid
        if cableguid:
            connectorname = 'connector_%s_%s' % (md.guid, powerinput.label)
            feedguids = cloudapi.feed.find(cableguid=cableguid)['result']['guidlist']
            if feedguids:
                oldfeedguid = feedguids[0]
                oldfeed = cloudapi.feed.getObject(oldfeedguid)
                for fc in oldfeed.feedconnectors:
                    if fc.name == connectorname:
                        cloudapi.feed.deleteConnector(oldfeedguid, connectorname)
                        break
                cloudapi.feed.addConnector(feedguid, connectorname, 0, str(q.enumerators.feedConnectorStatusType.NOTCONNECTED))
                cloudapi.feed.connectConnector(feedguid, connectorname, cableguid)

def getFeed(cloudapi, module):
    for powerinput in module.powerinputs:
        if powerinput.cableguid:
            feedguids = cloudapi.feed.find(cableguid=powerinput.cableguid)['result']['guidlist']
            if feedguids:
                return feedguids[0]

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
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)
    policyguids = cloudapi.policy.find(rootobjectguid=meteringdeviceguid, rootobjectaction="monitor")['result']['guidlist']
    if policyguids:
        policy = cloudapi.policy.getObject(policyguids[0])
    else:
        policy = None
    
    params['SESSIONSTATE']['meteringdeviceguid'] = meteringdeviceguid
    rackguid = meteringdevice.rackguid
    rack = cloudapi.rack.getObject(rackguid)
    if rack.floor:
        floor = cloudapi.floor.getObject(rack.floor)
        datacenterguid = floor.datacenterguid
    elif rack.roomguid:
        room = cloudapi.room.getObject(rack.roomguid)
        datacenterguid = room.datacenterguid
    params['SESSIONSTATE']['datacenterguid'] = datacenterguid
    nic = None
    ipaddress = None
    if meteringdevice.nics:
        nic = meteringdevice.nics[0]
        if nic.ipaddressguids:
            ipaddress = cloudapi.ipaddress.getObject(nic.ipaddressguids[0])
            lan = cloudapi.lan.getObject(ipaddress.languid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Update Energy Switch')
    tab.addText('name', 'Name', value=meteringdevice.name)
    types = dict([(k, k.capitalize()) for k in q.enumerators.meteringdevicetype._pm_enumeration_items.keys()])
    tab.addChoice('type', 'Energy Switch Type', values=types, selectedValue=str(meteringdevice.meteringdevicetype))
    tab.addInteger('positionx', 'Units in Rack', message='Units in the rack occupied by the Energy Switch', value=meteringdevice.positionx, minValue=0)
    tab.addInteger('positiony', 'Vertical Position', message='Vertical position of the Energy Switch in the rack', value=meteringdevice.positiony, minValue=0)
    tab.addInteger('positionz', 'Horizontal Position', message='Horizontal position of the Energy Switch in the rack', value=meteringdevice.positionz, minValue=0)
    tab.addInteger('height', 'Height', message='Height of the Energy Switch in U.', value=meteringdevice.height)
    if policy:
        tab.addInteger("polling", "Polling Interval", message="Energy switch polling interval in minutes", value=policy.interval)
    if nic and ipaddress:
        tab.addText('ipaddress', 'Ipaddress', message='Update ipaddress', value=ipaddress.address, validator=REGEX_IP4ADDRESS_VALIDATOR)
    
    tagobj = q.base.tags.getObject(meteringdevice.tags or '')
    tab.addText('tags', 'Tags', value=",".join(["%s:%s" % (k, v) for k, v in tagobj.tags.iteritems()]),
                helpText='Enter tags in the form of tag1:value1,tag2:value2')
    tab.addText('labels', 'Labels', value=",".join(tagobj.labels),
                helpText='Enter labels as comma separated values e.g. label1,label2')

    moduleguids = cloudapi.meteringdevice.find(parentmeteringdeviceguid=meteringdeviceguid)['result']['guidlist']
    modules = [cloudapi.meteringdevice.getObject(moduleguid) for moduleguid in moduleguids]
    feedguids = cloudapi.feed.find(datacenterguid=datacenterguid)['result']['guidlist']
    feeds = [cloudapi.feed.getObject(feedguid) for feedguid in feedguids]
    feedsdict = dict([(feed.guid, feed.name) for feed in feeds])
    for module in modules:
        feedguid = getFeed(cloudapi, module)
        if feedguid:
            tab.addDropDown('feedguid_module_%s' % module.name, 'Module %s' % module.name, feedsdict, selectedValue=feedguid)

    accounts = dict([(acc.guid, acc.login) for acc in meteringdevice.accounts])
    if accounts:
        tab.addChoice('account', 'Update an Account', values=accounts, message='Select 1 account to update', trigger='change', callback='updateAccount')

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        tags = tab.elements['tags'].value
        if tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        elif 'password' in tab.elements:
            if tab.elements['password'].value != tab.elements['password-validation'].value:
                tab.elements['password'].status = "error"
                tab.elements['password'].message = "Passwords do not match"
                tab.elements['password-validation'].status = "error"
                tab.elements['password-validation'].message = "Passwords do not match"
        elif 'ipaddress' in tab.elements:
            if not IPv4Address(tab.elements['ipaddress'].value) in IPv4Range(netIp=lan.network, netMask=lan.netmask):
                tab.elements['ipaddress'].status = 'error'
                tab.elements['ipaddress'].message = 'Ipaddress provided is not in the same network, provide a correct one'
            else:
                valid = True
        else:
            valid = True

    tab = form.tabs['main']
    elements = [element.name for element in tab.elements]
    labels = None
    labelsvalue = tab.elements['labels'].value
    
    if policy:
        cloudapi.policy.updateModelProperties(policy.guid, str(tab.elements['polling'].value))
    
    tagstring = getTagString(q, tab)

    #Update the account credentials
    account = list()
    if accounts and 'login' in elements:
        account = [{'login':tab.elements['login'].value, 'password':tab.elements['password'].value, 'guid':tab.elements['account'].value}]

    #Update the ipaddress of the nic
    if nic and ipaddress:
        cloudapi.ipaddress.updateModelProperties(ipaddressguid=ipaddress.guid,
                                                 address=tab.elements['ipaddress'].value)

    for module in modules:
        if 'feedguid_module_%s' % module.name in tab.elements and tab.elements['feedguid_module_%s' % module.name].value:
            feedguid = tab.elements['feedguid_module_%s' % module.name].value
            connectFeed(q, cloudapi, feedguid, moduleguid)

    if account:
        cloudapi.meteringdevice.updateModelProperties(meteringdeviceguid, name=tab.elements['name'].value,
                                                      meteringdevicetype=str(q.enumerators.meteringdevicetype.getByName(tab.elements['type'].value)),
                                                      height=tab.elements['height'].value,
                                                      positionx=tab.elements['positionx'].value,
                                                      positiony=tab.elements['positiony'].value,
                                                      positionz=tab.elements['positionz'].value,
                                                      accounts=account,
                                                      tags=tagstring)
    else:
        cloudapi.meteringdevice.updateModelProperties(meteringdeviceguid, name=tab.elements['name'].value,
                                                      meteringdevicetype=str(q.enumerators.meteringdevicetype.getByName(tab.elements['type'].value)),
                                                      height=tab.elements['height'].value,
                                                      positionx=tab.elements['positionx'].value,
                                                      positiony=tab.elements['positiony'].value,
                                                      positionz=tab.elements['positionz'].value,
                                                      tags=tagstring)

    q.gui.dialog.showMessageBox('Energy Switch "%s" is being updated' % tab.elements['name'].value, "Update Energy Switch")

def match(q, i, params, tags):
    return True
