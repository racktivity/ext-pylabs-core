## Using the Command Wrapper Class

In a system wrapper, you have seen that there is a management extension and a command tools extension. This command tools extension contains the modules with the command line commands of an application or service. 
These commands are mainly used by the management module where the commands get the necessary parameters of a CMDB Object. The commands can also be used directly, but then all parameters have to be filled in manually.

The command tools module always inherits from the base class `CommandWrapper`. 


### VirtualBoxMachineControl
This module contains the commands to manage a VirtualBox machine, e.g. start, stop, pause, resume, reboot, ...


### Importing the Necessary Modules
In a first phase you need to import all necessary modules. For all command tools modules you need to import the PyLabs framework central class, of which the `q` object is an instance, and the `CommandWrapper` base class.
Import other modules if necessary.

[[code]]
from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper

from VirtualBoxMachineConfiguration import executeVBoxCommand
from VirtualboxEnums import VirtualboxMachineStatusType
import init
[[/code]]


### Creating Your Class
Create a class that uses the CommandWrapper class and add a Pydoc that briefly explains the purpose of the class.
[[code]]
class VirtualBoxMachineControl(CommandWrapper):
    """VirtualBox Machine management commands, start, stop, reboot, pause, resume ... etc
    """
[[/code]] 


### Adding the Methods
In the example below you find some sample methods of the VirtualBoxMachineControl module. The methods in the command tools contain some logic to avoid conflicts, for example if a VirtualBox machine has the status RUNNING, it can not be started a second time.
Make sure that you add proper Pydocs to the methods.

[[code]]
    def start(self, name, kvmport = None):
        """
        Start the machine

        @param name: unique name for the machine
        @param kvmport: port to use by the VBox process for listening to enable remote access to the virtual machine
        """

        status = self.getStatus(name)
        if status == VirtualboxMachineStatusType.RUNNING:
            q.console.echo('Machine is already running')
            return
        elif status == VirtualboxMachineStatusType.STOPPED:
            if not kvmport :
                q.logger.log("No kvmport supplied. Trying to start the machine in GUI mode", 3)
                command = 'VBoxManage startvm %(machine)s ' %{'machine':name}
            else:
                q.logger.log("Starting the machine in vrdp mode on port %s" %kvmport, 3)
                command = 'VBoxManage startvm %(machine)s -type vrdp' %{'machine':name}

            exitCode, output = executeVBoxCommand(command)
            if not exitCode:
                q.logger.log("Machine %s Started"%name, 3)
            else:
                q.logger.log("Failed to start machine %s. Reason: %s"%(name, output), 3)
                raise RuntimeError("Failed to start machine")
        elif status == VirtualboxMachineStatusType.PAUSED:
            q.console.echo('Machine is paused. Please call resume() instead')
        else:
            raise ValueError("Invalid status %s" %status)


    def stop(self, name):
        """
        Stop the machine

        @param name: unique name for the machine
        """

        status = self.getStatus(name)
        if status == VirtualboxMachineStatusType.STOPPED:
            q.console.echo('Machine is not running')
            return
        if status == VirtualboxMachineStatusType.RUNNING or self.getStatus(name) == VirtualboxMachineStatusType.PAUSED:
            command = 'VBoxManage controlvm %(machine)s poweroff'%{'machine':name}
            exitCode, output = executeVBoxCommand(command)
            if not exitCode:
                q.logger.log("Machine %s Stopped"%name, 5)
            else:
                q.logger.log("Failed to stop machine %s. Reason: %s"%(name, output), 5)
                raise RuntimeError('Failed to stop machine')
        else:
            raise ValueError("Invalid status %s" %status)


    def reboot(self, name):
        """
        Reboot the machine

        @param name: unique name for the machine
        """

        status = self.getStatus(name)
        if status == VirtualboxMachineStatusType.RUNNING:
            command = 'VBoxManage controlvm %(machine)s reset'%{'machine':name}
            exitCode, output = executeVBoxCommand(command)
            if not exitCode:
                q.logger.log("Machine %s Rebooted"%name, 5)
            else:
                q.logger.log("Failed to reboot machine %s. Reason: %s"%(name, output), 5)
                raise RuntimeError('Failed to reboot machine')
        else:
            raise ValueError("Invalid status %s" %status)


    def pause(self, name):
        """
        Pause the machine

        @param name: unique name for the machine
        """

        status = self.getStatus(name)
        if status == VirtualboxMachineStatusType.RUNNING:
            command = 'VBoxManage controlvm %(machine)s pause'%{'machine':name}
            exitCode, output = executeVBoxCommand(command)
            if not exitCode:
                q.logger.log("Machine %s paused"%name, 5)
            else:
                q.logger.log("Failed to pause machine %s. Reason: %s"%(name, output), 5)
                raise RuntimeError('Failed to pause machine')
        else:
            raise ValueError("Invalid status %s" %status)


    def resume(self, name):
        """
        Resume the machine if it's paused

        @param name: unique name for the machine
        """

        status = self.getStatus(name)
        if status == VirtualboxMachineStatusType.PAUSED:
            command = 'VBoxManage controlvm %(machine)s resume'%{'machine':name}
            exitCode, output = executeVBoxCommand(command)
            if not exitCode:
                q.logger.log("Machine %s resumed"%name, 3)
            else:
                q.logger.log("Failed to resume machine %s. Reason: %s"%(name, output), 3)
                raise RuntimeError('Failed to resume machine')
        else:
            raise ValueError("Invalid status %s" %status)
[[/code]]
