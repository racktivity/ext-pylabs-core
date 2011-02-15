from pylabs.InitBase import *

q.application.appname="setup wizardrunner"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True

if q.gui.dialog.askYesNo("Are you sure your qbase sandbox is configured to use mercurial as basis for qpackage metadata?")==False:
    q.gui.dialog.message("Follow the procedure on http://confluence.aserver.com/display/PM/Downloads") 
    q.application.stop()



i.qp.updateAll()
i.qp.findByName("pyamf").install()
q.gui.dialog.message("We are now going to install the control wizard, take most recent version, last version tested = 1.4")
i.qp.findByName("portal_control_wizard").install()
q.gui.dialog.message("We are now going to install the applicationserver, take most recent version, last version tested = 1.3")
i.qp.findByName("applicationserver").install()
q.system.fs.changeDir("/opt/qbase3/apps/pywizardsdk")
q.system.fs.symlink("/opt/qbase3/apps/applicationserver/services/wizard_engine/wizard.py","/opt/qbase3/apps/pywizardsdk/wizard.py",True)


#file:///opt/qbase3/apps/pywizardsdk/vpdcwizard.swf?allowScriptAccess=always&wizardName=test&wizardTitle=titleexample&wizardSdkAddress=localhost

q.gui.dialog.message("START server:")
q.gui.dialog.message("q.gui.dialog.message(\"START:\"")

q.gui.dialog.message("START client:")
q.gui.dialog.message("firefox \"file:///opt/qbase3/apps/pywizardsdk/vpdcwizard.swf?allowScriptAccess=always&wizardName=test&wizardTitle=titleexample&wizardSdkAddress=localhost\"")

q.gui.dialog.message("If it doesn't work check you flash install go to http://www.adobe.com/software/flash/about")
