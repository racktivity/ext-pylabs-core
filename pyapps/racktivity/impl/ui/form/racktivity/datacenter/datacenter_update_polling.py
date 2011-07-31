__author__ = 'racktivity'
__tags__ = 'wizard', 'datacenter_update_polling'
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    
    datacenters = cloudapi.datacenter.list()['result']['datacenterinfo']
    datacenterDict = dict([(datacenter['guid'], datacenter['name']) for datacenter in datacenters])
    
    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Update Datacenter Polling')
    tab.addChoice('datacenter', 'Data Center', datacenterDict, selectedValue='', message='Please select datacenter', optional=False)
    tab.addInteger("polling", "Polling Interval", message="Energy switch polling interval in minutes", value=5)
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']
    
    dcguid = tab.elements['datacenter'].value
    interval = tab.elements['polling'].value
    
    sql = """
    select meteringdevice."guid" from meteringdevice.view_meteringdevice_list as meteringdevice
       join rack.view_rack_list as rack on meteringdevice.rackguid = rack.guid
       join room.view_room_list as room on rack.roomguid = room.guid
       join datacenter.view_datacenter_list as datacenter on room.datacenterguid = datacenter.guid
       where datacenter.guid = '%(guid)s' and meteringdevice.parentmeteringdeviceguid is Null;
    """ % {'guid': dcguid}
    
    results = q.drp.meteringdevice.query(sql)
    
    for result in results:
        guid = result['guid']
        policiesguids = rootobjectaction_find.policy_find(rootobjectguid=guid)
        if policiesguids:
            policy = q.drp.policy.get(policiesguids[0])
            policy.interval = float(interval)
            q.drp.policy.save(policy)
            
    q.gui.dialog.showMessageBox('Polling has been updating', "Update Datacenter polling")

def match(q, i, params, tags):
    return True