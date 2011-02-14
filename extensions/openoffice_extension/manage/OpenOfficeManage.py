from pymonkey import q
from pymonkey.baseclasses.ManagementApplication import ManagementApplication

class OpenOfficeManage(ManagementApplication):

    def start(self):
        """
        Start Open Office
        """
        return q.cmdtools.openoffice.start()

    def stop(self):
        """
        Stop Open Office
        """
        return q.cmdtools.openoffice.stop()

    def getStatus(self):
        """
        Get Status of Open Office
        """
        return q.cmdtools.openoffice.getStatus()

    def restart(self):
        """
        Restart Open Office
        """
        return q.cmdtools.openoffice.restart()

    def printStatus(self):
        """
        Print the status of Open Office
        """
        q.gui.dialog.message("Open Office is %s " % self.getStatus())
