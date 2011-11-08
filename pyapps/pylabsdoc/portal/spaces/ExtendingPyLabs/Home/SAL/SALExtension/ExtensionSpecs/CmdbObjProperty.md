@metadata title=CMDB Object
@metadata order=30
@metadata tagstring=cmdb object property

[baseclass]: #/ExtendingPylabs/BaseClasses
[createenum]: #/ExtendingPylabs/CreateEnumerators


# Properties of Pylabs CMDB Objects

Each Pylabs extension that manages an existing application or service will have objects to be managed, such as a machine, a Port Forwarding server, a disk partition, etc. These objects are stored in the CMDB (Configuration Management DataBase) and are *CMDB Objects*. The CMDB only contains the configuration of these objects, it does not contain any logic.

There are three types of CMDB Objects:

* *CMDB Object*:
This is a configuration of a simple object that does not belong to an application, such as a disk partition. A CMDB Object will always inherit from the base class CMDB Object. The CMDB Object class inherits on its turn from the base class Base CMDB Object.
* *CMDB Application Object*:
This is a configuration of an application object that is not a server application, such as a machine. A CMDB Application Object always inherits from the base class CMDB Application Object. The CMDB Application Object class inherits on its turn from the base class CMDB Object.
* *CMDB Server Object*:
This is a configuration of a server object, such as a Port Forwarding rule. A CMDB Server Object always inherits from the base class CMDB Server Object. The CMDB Server Object class inherits on its turn from the base class CMDB Application Object.

[[info]]
**Information**
For more information on CMDB Objects, Base CMDB Objects, CMDB Application Objects and CMDB Server Objects, please check the Pylabs [Base Classes][baseclass].
[[/info]]

Each of the CMDB objects have in common that their properties mainly consist of:

* Simple properties; such as base type properties.
* Complex properties; such as a CMDB Sub-object.


## Simple Properties

Simple properties are properties that rely on the defined Pylabs types. For example, the name of a Port Forwarding rule, which is a string. Most of the Pylabs types are common for all developing languages, such as 'string', 'integer', 'dictionary', 'boolean', etc. The Pylabs framework however, provides you some more base types, such as 'ipaddress', 'filepath' and 'unixdirpath'.
If you have a type that you would use in multiple applications, you can [extend the Pylabs base types][createenum] yourself, instead of creating the type for each application.
A simple property can also be set via an enumerator. Pylabs contains predefined enumerators, such as the status of an application, but you can also [create your own enumerators][createenum].

## Complex Properties

A CMDB object can have a property that is too complex to define as a simple property. This type of property will then be created as a CMDB Sub Object. The CMDB Sub Object always inherits from the base class CMDB Sub Object. The CMDB Sub Object class inherits on its turn also from the base class Base CMDB Object.
For example, the configuration of a PortForwarding server contains PortForwarding rules. Such a PortForwarding rule has too many properties to define it as a base type, so the rule becomes a CMDB Subobject. 
