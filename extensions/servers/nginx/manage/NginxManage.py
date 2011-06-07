import os
from pylabs import q
from pylabs.baseclasses.ManagementApplication import ManagementApplication, CMDBLockMixin
from pylabs.enumerators import AppStatusType
# Suppress warning by Cheetah about non-C NameMapper
import warnings
import urllib
warnings.simplefilter("ignore")
from NginxServer import NginxServer
warnings.filters.pop(0)

class NginxManage(ManagementApplication, CMDBLockMixin):
    """
    Nginx Server configuration extension entry point
    """

    cmdb = NginxServer()

    def printStatus(self):
        """
        Print the live status of the Nginx Server
        """
        q.console.echo("Nginx is %s" % self.getStatus())
    
    def getStatus(self):
        """
        Get the status of the Nginx Server
        """
        return q.cmdtools.nginx.getStatus()

    def save(self):
        """
        If the configuration is dirty write it to the cmdb
        else return
        """
        q.console.echo("Writing changes to cmdb")
        self.cmdb.save()

    def start(self):
        """
        Starts the Nginx Server based on the applied configuration
        if status is STARTED or STARTING return
        """
        if self.getStatus() == AppStatusType.RUNNING:
            q.console.echo("Nginx is already running")
            return True

        q.cmdtools.nginx.start()
        if self.getStatus() == AppStatusType.RUNNING:
            q.console.echo('Nginx started successfully')
            return True
        else:
            q.console.echo('failed to start Nginx')
            return False

    def stop(self):
        """
        Stops the Nginx Server
        if status is STOPPED or STOPPING return
        """
        if self.getStatus() != AppStatusType.RUNNING:
            q.console.echo("Nginx is not running")
            return True

        q.cmdtools.nginx.stop()

        if self.getStatus() == AppStatusType.HALTED:
            q.console.echo('Nginx stopped successfully')
            return True
        else:
            q.console.echo('failed to stop Nginx')
            return False 

    def restart(self):
        """
        Restart the Nginx Server
        """
        q.cmdtools.nginx.restart()

        if self.getStatus() == AppStatusType.RUNNING:
            q.console.echo('Nginx restarted successfully')
            return True
        else:
            q.console.echo('failed to restart Nginx')
            return False

    def applyConfig(self):
        """
        Generates the site configuration file and reloads the nginx server

        This will clean out some config directories!
        """ 
        self.cmdb.pm_write()

        if self.getStatus() == AppStatusType.RUNNING:
            q.cmdtools.nginx.reload()
