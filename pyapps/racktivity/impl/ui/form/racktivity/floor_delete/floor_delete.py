__tags__ = "wizard", "floor_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    floorguid = params['extra']['floorguid']
    floor = cloudApi.floor.getObject(floorguid)
    
    rooms = cloudApi.room.find(floor=floorguid)['result']['guidlist']
    if rooms:
        num = len(rooms)
        msg = "The current floor has %s room(s), are you sure you want to delete this floor with all its room(s)?" % num
    else:
        msg = "Are you sure you want to delete '%s' floor?" % floor.name
    
    
    answer = q.gui.dialog.showMessageBox(msg, "Delete floor", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    cloudApi.floor.delete(floorguid)
    q.gui.dialog.showMessageBox("Floor '%s' is being deleted" % floor.name, "Delete floor")
def main(q, i, p, params, tags):
    return True