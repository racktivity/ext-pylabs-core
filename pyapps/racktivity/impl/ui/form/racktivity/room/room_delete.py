__tags__ = "wizard", "room_delete"
__author__ = "racktivity"

def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    roomguid = params['extra']['roomguid']
    racks = cloudApi.rack.find(roomguid=roomguid)['result']['guidlist']
    if racks:
        num = len(racks)
        answer = q.gui.dialog.showMessageBox('''The current room has %s rack(s),
are you sure you want to delete this room with all its rack(s)?''' % num,
                                             "Delete room", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
        if answer.lower() == "no":
            return
    room = cloudApi.room.getObject(roomguid)
    cloudApi.room.delete(roomguid=roomguid)
    q.gui.dialog.showMessageBox("room '%s' is being deleted" % room.name, "Delete room")

def match(q,i,params,tags):
    return True
