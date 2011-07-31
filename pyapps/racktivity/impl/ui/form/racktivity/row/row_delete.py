__tags__ = "wizard", "row_delete"
__author__ = "racktivity"

def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')
    rowguid = params['extra']['rowguid']
    row = cloudApi.row.getObject(rowguid)
    
    racks = row.racks
    if racks:
        num = len(racks)
        msg = "The current row has %s rack(s), are you sure you want to delete this row with all its rack(s)?" % num
    else:
        msg = "Are you sure you want to delete '%s' row?" % row.name
    
    
    answer = q.gui.dialog.showMessageBox(msg, "Delete row", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    cloudApi.row.delete(rowguid)
    q.gui.dialog.showMessageBox("Row '%s' is being deleted" % row.name, "Delete row")
def match(q,i,params,tags):
    return True