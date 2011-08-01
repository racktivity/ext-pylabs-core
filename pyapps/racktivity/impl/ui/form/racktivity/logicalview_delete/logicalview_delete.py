__tags__ = "wizard", "logicalview_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    logicalviewguid = params['extra']['logicalviewguid']
    logicalview = cloudApi.logicalview.getObject(logicalviewguid)
    
    msg = "Are you sure you want to delete '%s' logicalview?" % logicalview.name
 
    answer = q.gui.dialog.showMessageBox(msg, "Delete logical view", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    cloudApi.logicalview.delete(logicalviewguid)
    q.gui.dialog.showMessageBox("Logical view '%s' is being deleted" % logicalview.name, "Delete logical view")
def main(q, i, p, params, tags):
    return True