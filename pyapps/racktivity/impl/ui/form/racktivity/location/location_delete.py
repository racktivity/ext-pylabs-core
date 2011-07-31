__tags__ = "wizard", "location_delete"
__author__ = "racktivity"

def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    
    locationguid = params['extra']['locationguid']
    
    datacenters = cloudApi.datacenter.find(locationguid=locationguid)['result']
    if datacenters:
        num = len(datacenters)
        answer = q.gui.dialog.showMessageBox('''The current location has %s datacenter(s),
are you sure you want to delete this location with all its datacenter(s)?''' % num,
                                                 "Delete location", msgboxButtons="YesNo",
                                                 msgboxIcon="Question", defaultButton="No")
        if answer == "No":
            return
    location = cloudApi.location.getObject(locationguid)
    cloudApi.location.delete(locationguid=locationguid)
    q.gui.dialog.showMessageBox("location '%s' is being deleted" % location.name, "Delete location")
    
def match(q,i,params,tags):
    return True