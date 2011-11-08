@metadata title=Management Application Class
@metadata tagstring=management application class


# Using the Management Application Class

The `ManagementApplication` Class is used for creating the management module of your Application Management extension. This management module contains the methods to manage your application or service, by using the CMDB Objects of the application or service.

The `ManagementApplication` class _always_ inherits from the `ManagementConfiguration` Class. The `ManagementConfiguration` class provides some methods to manage a configuration, such as applyConfig and printConfig. The `ManagementApplication` class provides the basic management functions for the application or service.
Obviously these base classes do not contain any logic nor code, they only provide empty methods for the management module.

## Code Snippet of ManagementApplication.py

[[code]]
def stop(self):
    """
    If status is STOPPING or STOPPED, return.
    Stop the server
    """
    raise NotImplementedError("%s.stop()" % self.cmdb.name)
[[/code]]

## VirtualBoxManager
With this management module you can control and configure your VirtualBox application. 

## Importing the Necessary Modules
In a first phase you need to import all necessary modules. For all management modules you need to import the Pylabs framework central class, of which the `q` object is an instance, and the ManagementApplication base class.
Import other modules if necessary.

[[code]]
from pylabs import q
from pylabs.baseclasses.ManagementApplication import ManagementApplication
from pylabs.enumerators import AppStatusType

from hypervisors.virtualbox_cmdtools import VirtualboxEnums

from VirtualboxHypervisor import VirtualboxHypervisor
[[code]]


## Creating Your Class
Create a class that uses the `ManagementApplication` class and add a Pydoc that briefly explains the purpose of the class. 

[[code]]
class VirtualBoxManager(ManagementApplication):
    """
    Represents a Virtualbox instance Manager to control and configure Virtualbox application
    """

#create an instance of VirtualboxHypervisor
    cmdb = VirtualboxHypervisor()
[[/code]]

## Adding the Methods
Besides the methods that are provided by the base classes (save, applyConfig, start, stop, ...), it is possible that you need to add other methods to fully manage your application or service. In this example we give you some of the methods that are available for this management module.
Make sure that you add proper Pydocs for each method, as done in the example below.

[[code]]
    def save(self):
        """
        Saves the configuration in the cmdb
        If configuration not dirty (i.edirtyProperties. configuration is in sync with cmdb), then
        return. Otherwise save the configuration in the cmdb and clear the dirty flag
        """
        if self.cmdb.isDirty:
            q.logger.log('Saving virtualbox configuration to cmdb', 3)
            self.cmdb.save()
        self.cmdb.dirtyProperties.clear()


    def applyConfig(self):
        """
        Applies the configuration saved in the cmdb to the system
        Call self.init
        Call self.save()
        Apply the configuration to the server
          - The status must be identical before and after the applyConfig command
              (a RUNNING server is again RUNNING, a STOPPED server is again STOPPED)
          - Ideally, a RUNNING server can be runtime reconfigured
          - for some servers a stop - modify config - start must be implemented
        """
        q.logger.log('Applying configurations to VirtualBox server', 3)
        self.init()

        if 'machines' not in self.cmdb.dirtyProperties:
            return

        for machine in self.cmdb.machines.values():
            if machine.removed:
                self._unregisterMachine(machine)
                self.cmdb.machines.pop(machine.name)
            elif machine.isDirty:
                if not machine.created:
                    self._registerMachine(machine)

                self._updateMachine(machine)

        self.save()


    def startMachine(self, name):
        """
        Start the machine

        @type name: string
        @param name: name of the machine to start
        """

        if name in self.cmdb.machines.keys():
            machine = self.cmdb.machines[name]
            try:
                q.hypervisors.cmdtools.virtualbox.machineControl.start(name, machine.kvmport)
                machine.status = q.enumerators.VirtualboxMachineStatusType.RUNNING
            except Exception, ex:
                raise RuntimeError(ex.message)
            q.console.echo('Machine [%s] started successfully'%machine.name)
        else:
             raise ValueError("Machine[%s] is not registered in virtualbox"%name)


    def stopMachine(self, name):
        """
        Stop the machine

        @type name: string
        @param name: name of the machine to stop
        """

        if name in self.cmdb.machines.keys():
            machine = self.cmdb.machines[name]
            try:
                q.hypervisors.cmdtools.virtualbox.machineControl.stop(name)
                machine.status = q.enumerators.VirtualboxMachineStatusType.STOPPED
            except Exception, ex:
                raise RuntimeError(ex.message)
            q.console.echo('Machine [%s] stop successfully'%name)
        else:
             raise ValueError("Machine[%s] is not registered in virtualbox"%name)


    def rebootMachine(self, name):
        """
        Reboot the machine

        @type name: string
        @param machine: machine to be rebooted
        """

        if name in self.cmdb.machines.keys():
            try:
                q.hypervisors.cmdtools.virtualbox.machineControl.reboot(name)
            except Exception, ex:
                raise RuntimeError(ex.message)
            q.console.echo('Machine [%s] rebooted'%name)
        else:
             raise ValueError("Machine[%s] is not registered in virtualbox"%name)


    def __str__(self):
        return str(self.cmdb)


    def __repr__(self):
        return self.__str__()


    def _registerMachine(self, machine):
        """
         Register a new vbox machine

         @type machine: VirtualboxMachine
         @param machine:  Machine object to register with Virtualbox instance
        """

        try:
            q.hypervisors.cmdtools.virtualbox.machineConfig.registerMachine(machine.name, self.cmdb.machinesFolder)
        except Exception, ex:
            raise RuntimeError(ex.message)
        machine.created = True


    def _unregisterMachine(self, machine):
        """
        Unregisters a machine from VirtualBox instance, deattaching any disks attached to a machine

        @type machine: VirtualboxMachine
        @param machine:  Machine object to register with Virtualbox instance
        """

        for disk in machine.disks.values():
            try:
                q.hypervisors.cmdtools.virtualbox.machineConfig.removeDisk(machine.name, disk.order)
            except Exception, ex:
                raise RuntimeError(ex.message)
        try:
            q.hypervisors.cmdtools.virtualbox.machineConfig.unregisterMachine(machine.name)
        except Exception, ex:
                raise RuntimeError(ex.message)
[[/code]]
