[importpylabs]: /pylabsdoc/#/HowTo/ImportPyLabs
[importextension]: /pylabsdoc/#/HowTo/ImportExtensionClass
[baseclass]: /pylabsdoc/#/ExtendingPyLabs/BaseClasses
[contribute]: /pylabsdoc/#/PyLabs50/Contributing
[namespace]: /pylabsdoc/#/PyLabs50/NameSpaces


# CMD Tools Extension Specifications

The CMD Tools extension must contain one or multiple command files which contain the methods that wraps the command line tools of the application. 
The methods should also include the logic and possible tests that precede the actual command. For example, check that the status of an application is not already 'STARTING' when trying to start the application.

By wrapping the command tools, you gain more control over the commands, for example you can add logging when a command is executed. 

Use the 'cmdtools' namespace as location for these methods. Check the [Q-Namespace][namespace] page for more details on the cmdtools namespace.


## Content of the Specification File

* Import the required modules. Check How to Import PyLabs][importpylabs] and [How to Import Classes from Extensions][importextension].
* Add a Class that inherits from the base class [CMDBApplicationObject][baseclass].
* Add all methods of the class.
* Add PyDocs for *each* method that gives its full explanation, see the *DocString* section in the [Contributing in Style][contribute] page.


## Advantages

* The developer has immediately all modules that he has to use.
* The developer no longer has to take care of the documentation of the methods
* The developer can immediately use the extension in the Q-Shell


## Example

[[code]]
#import the necessary modules
from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.enumerators import AppStatusType
from TomcatSetEnvVars import TomcatSetEnvVars
import time

#create a class that inherits from the CommandWrapper class:
class PortForwarderCmd(CommandWrapper):

    def start(self, foreground = False, managementPort = 8000):
        """Start the portforwarding daemon

        @param foreground:     boolean indicating if portforwarder should not daemonize and run in foreground
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        """
        pass

    def stop(self, managementPort = 8000):
        """
        Stops the portforwarding daemon
        
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        """
        pass

    def list(self, managementPort = 8000):
        """
        Lists all active port forwarding rules
        
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        @return: dictionary with all active rules. Key is local port, value is tuple of (remoteHost, remotePort)
        """
        pass

    def addRule(self, localPort, remoteHost, remotePort,  managementPort = 8000):
        """
        Add a new port forwarding rule to the server.
        Server should be running.
        
        @param localPort: Port number on the local host
        @param remoteHost: Hostname or ip to forward to
        @param remotePort: Port number on the remote host
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        """
        pass

    def removeRule(self, localPort,  managementPort = 8000):
        """
        Remove the active port forwarding rule for a given local port
        
        @param localPort: Port number on the local host
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        """
        pass

    def getStatus(self, managementPort = 8000):
        """
        Check if the portForwarder service is running on the given local port
        
        @param managementPort: port on which the management xmlrpcserver listens (default 8000)
        @return: boolean, True if running else False
        """
        pass
[[/code]]