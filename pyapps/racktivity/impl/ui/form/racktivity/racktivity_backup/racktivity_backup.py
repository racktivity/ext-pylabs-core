__tags__ = "wizard", "racktivity_backup"
__author__ = "racktivity"

BACKUP_POLICY = 'racktivity_backup'

def main(q, i, p, params, tags):
    import json
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()
    #Set default values
    dest = "/opt/racktivity_backups/"
    interval = 24
    enabled = True
    runbetween = '[("00:00", "24:00")]'
    runnotbetween = '[]'
    #Get the backup policy
    backuppolicyguids = cloudapi.policy.find(BACKUP_POLICY)['result']['guidlist']
    if backuppolicyguids:
       backuppolicyguid = backuppolicyguids[0]
       backuppolicy = q.drp.policy.get(backuppolicyguid)
       if backuppolicy.policyparams:
           dest = eval(backuppolicy.policyparams)["path"]
	   interval = int(backuppolicy.interval / 60)
	   enabled = (backuppolicy.runnotbetween != '[("00:00", "24:00")]')
	       
    backuptab = form.addTab('main', 'Backup Configuration')
    
    backuptab.addText('location', 'Backup location', value=dest, message='Please enter the backup location')
    backuptab.addInteger('interval', 'Time between backups in hours', value=interval, helpText='Enter the time in hours between backups', minValue=1)
    backuptab.addYesNo('enabled', 'AutoBackup is enabled ?', selectedValue=int(enabled), helpText='Set this to No to disable the automatic backup functionality')
    
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        #validate data
	if q.system.fs.exists(tab.elements['location'].value):
            valid = True
	else:
	    q.gui.dialog.showMessageBox("Directory %s doesn't exist"%tab.elements['location'].value, "Information")
	    valid = False
	tab = form.tabs['main']

    enabled = bool(tab.elements['enabled'].value)
    if enabled:
        runnotbetween = '[]'
    else:
        #To disable to policy, set the runnot to be the whole day
        runnotbetween = '[("00:00", "24:00")]'

    if backuppolicyguids:
        #The backup policy already exists

        result = cloudapi.policy.updateModelProperties(backuppolicyguid, policyparams = json.dumps({'path':tab.elements['location'].value}),
                                                       runnotbetween = runnotbetween, interval=float(tab.elements['interval'].value)*60)
    else:
        #Create the backup policy
        cloudapi.policy.create(name = BACKUP_POLICY, description = 'Racktivity Backup policy', 
                                                                 interval = float(tab.elements['interval'].value)*60, 
                                                                 rootobjecttype = 'racktivity', rootobjectaction = 'backup', 
								 rootobjectguid = None, 
                                                                 runbetween = '[("00:00", "24:00")]', runnotbetween = runnotbetween, 
                                                                 policyparams = json.dumps({'path':tab.elements['location'].value}))

    q.gui.dialog.showMessageBox("Backup policy has been updated", "Information")

def main(q, i, p, params, tags):
    return True
