@metadata title=Base Classes
@metadata order=50
@metadata tagstring=base class overview

[twisted]: http://twistedmatrix.com/trac/


# PyLabs Base Classes

The PyLabs base classes module contains different classes which are required for the full functionality of PyLabs. The purpose of the `baseclasses` module is twofold:

* Obtain functionalities and properties for later usage when developing applications, based on the PyLabs framework.
* Create categories in the different PyLabs functionalities for clarity and easy retrieval of the functions.

----
## In this Chapter...

Overview of the PyLabs BaseClasses

[[children/]]


## BaseCMDBObject
The BaseCMDBObject class is the base for _all_ CMDB object types, e.g. CMDBServerObject or CMDBApplicationObject. All types of CMDB objects must inherit from this class. This class adds the attributes _timestampcreated_ and _timestampmodified_ to a new type of CMDB Object. Both attributes are integers and represent epoch time.

This class must be used when you create new types of CMDB objects and should not be modified. The CMDBObject class inherits from this class.


    timestampcreated = Integer(doc = 'Epoch time when this object was created')
    timestampmodified = Integer(doc = 'Epoch time when this object was last modified')

    #these properties will be added to ALL CMDB Objects


## BaseEnumeration
The BaseEnumeration class is the base for all enumeration classes (e.g. PlatformType). 
The BaseEnumeration class provides a check method which checks whether a given variable is a valid enumeration item and a generic getByName method which retrieves an enumeration item based on its name.

When you use the BaseEnumeration class, you can create your own enumeration class with a few lines of code:

[[code]]
from pylabs.baseclasses import BaseEnumeration

class SeverityType(BaseEnumeration):
    """Utility class which gives string representation of severity level"""

    def __repr__(self):
        return str(self)


SeverityType.registerItem('info')      #registerItem is a method inherited from BaseEnumeration. This method registers the item in the enumeration and will become uppercased
SeverityType.registerItem('warning')
SeverityType.registerItem('error')
SeverityType.registerItem('critical')
SeverityType.finishItemRegistration()  #finishItemRegistration is used when no more items should be created.
[[/code]]


## BaseType
If you create a class that needs `q.base.*` as attributes in that class, you have to import class: `from pylabs.baseclasses import BaseType`. If you do not do this, you will get weird errors and your application will fail when using this class. 
This is _by design_.


## CMDBApplicationObject
The CMDBApplicationObject class always inherits everything from the CMDBObject class and adds the attributes `initDone` and `pid`. This class contains the configuration application object for daemons or normal applications but does _not_ contain any management logic. 
Use the CMDBApplicationObject class for creating objects with application data.


## CMDBObject
The CMDBObject class _always_ inherits from the BaseCMDBObject class and adds CMDB configuration attributes to a CMDB object, i.e. a configuration for a daemon or application. It is the base class for all CMDB classes which are registered directly in the CMDB and is used for the initialization of a CMDB object.
The initialization consists of the initialization of the _base properties_, i.e. creating a CMDB ID and a CMDB guid.

Use this class for CMDB objects which are not CMDBApplication or CMDBServer objects and which is not a property of a complex CMDB Object.

It is possible to use the CMDBObject class to directly manipulate in the CMDB via a self-developed application. However, in the PyLabs framework, this class is mainly used by the [#CMDBApplicationObject] class and indirectly by the CMDBServerObject class. 


## CMDBServerObject
The CMDBServerObject class _always_ inherits everything from CMDBApplicationObject and adds the attributes `autoRestart` and `startAtReboot`.  This class contains the configuration application object for server applications but does _not_ contain any management logic.
Use the CMDBServerObject class for configuring a server application, e.g. configuring a portforwarder server. The portforwarding class of PyLabs inherits from the CMDBServerObject Class and adds the attributes `forwards` (i.e. a dictionary of portforwarding rules), `managementPort` and, `cmdbtypename` (i.e. location in the CMDB).


## CMDBSubObject
The CMDBSubObject class _always_ inherits everything from BaseCMDBObject and adds the attribute `rootcmdbtypename`, i.e. indicate to which CMDB object it belongs. CMDBSubObjects should not be registered directly to the CMDB.
Use the CMDBSubObject class to define a more complex property of a CMDB object, e.g. one portforwarding rule on a portforwarding server. Validations on the properties of the subobject can also be put in here.


## CommandWrapper
The CommandWrapper class is a class that does nothing more than wrapping functions, mainly system utilities such as mkfs, registry manipulations, ... and application commands. All system utilities and application commands must inherit from the CommandWrapper class.
At this moment the purpose of this class is only to categorize subclasses, it does not provide any functionality, nor it adds properties.

Use the CommandWrapper class when you develop a command module of an application. This module contains the methods for the actions on your application, such as starting and stopping the application. Make sure that all logic is defined here, for example, starting an application is not possible when the status of the application is starting.
The methods of this module can then be used in the management module (ManagementApplication) of your application. The methods of the command module _must_ appear in the name space `q.cmdtools.<application>` but they are preferred to be used through a management class of the application or by experienced users.


## ManagementApplication
The ManagementApplication class is the management base class for one server or one application. This class is one of the core PyLabs classes since it is the bridge between the application's configuration stored in the CMDB and the management and configuration of the application on the system.    
The management class applies the configuration stored in the CMDB to the system and controls the application on the system using the command module (CommandWrapper) of the application.


## ManagementApplicationXMLRPC
This base class has the same function as the `ManagementApplication` class, but now exposed over XMLRPC. An XMLRPC Server is required.
XMLRPC is a spec and a set of implementations that allow software running on disparate operating systems, running in different environments to make procedure calls over the Internet.
It's remote procedure calling using HTTP as the transport and XML as the encoding. XML-RPC is designed to be as simple as possible, while allowing complex data structures to be transmitted, processed and returned.


## ManagementConfiguration
This class is a base class for managing configurations stored in the CMDB. It is a bridge between configuration (= CMDB) and the system that uses the configuration.


## XMLRPCServer
This is a generic implementation of an XMLRPC Server based on [twisted][]. When creating a server class, inherit from this class.

[[code]]
from pylabs.InitBase import q
from pylabs.baseclasses.xmlrpc.server import ManagementClassXMLRPCServer
[[/code]]


## SystemWrapper
The SystemWrapper class is a class that does nothing more than wrapping functions, mainly operating system commands, e.g. copyFile. It has a similar function as the CommandWrapper class. 


## Dirty Flagging
The PyLabs framework has a mechanism that allows you to verify if the real configuration of a CMDB Object is synchronized with the CMDB. A CMDB object is a configuration that has specific properties. It might be possible that a user changes a value of a CMDB object without saving it in the CMDB. As a consequence the CMDB object becomes dirty (i.e. not synchronized with the CMDB) as long as it is not saved.  
Dirty flagging will be mainly used in the code that defines a CMDB Object. See CMDBSubObject paragraph for the usage of the dirty flag.
