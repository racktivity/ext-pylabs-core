__tags__ = "wizard", "pod_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    podguid = params['extra']['podguid']
    pod = cloudApi.pod.getObject(podguid)
    
    rows = cloudApi.row.find(pod=podguid)['result']['guidlist']
    if rows:
        num = len(rows)
        msg = "The current pod has %s row(s), are you sure you want to delete this pod with all its row(s)?" % num
    else:
        msg = "Are you sure you want to delete '%s' pod?" % pod.name
    
    
    answer = q.gui.dialog.showMessageBox(msg, "Delete pod", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    cloudApi.pod.delete(podguid)
    q.gui.dialog.showMessageBox("Pod '%s' is being deleted" % pod.name, "Delete pod")
def main(q, i, p, params, tags):
    return True