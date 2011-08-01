__tags__ = "wizard", "datacenter_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    datacenterguid = params['extra']['datacenterguid']
    datacenter = cloudApi.datacenter.getObject(datacenterguid)
    
    rooms = cloudApi.room.find(datacenterguid=datacenterguid)['result']['guidlist']
    if rooms:
        num = len(rooms)
        msg = "The current datacenter has %s room(s), are you sure you want to delete this datacenter with all its room(s)?" % num
    else:
        msg = "Are you sure you want to delete '%s' datacenter?" % datacenter.name
    
    
    answer = q.gui.dialog.showMessageBox(msg, "Delete datacenter", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    cloudApi.datacenter.delete(datacenterguid)
    q.gui.dialog.showMessageBox("datacenter '%s' is being deleted" % datacenter.name, "Delete datacenter")
def main(q, i, p, params, tags):
    return True