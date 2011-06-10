[imgPylabsSystemWrapper]: images/images50/extendingpylabs/PylabsSystemWrapper.png
[cmdbobjproperty]: /pylabsdoc/#/ExtendingPyLabs/CmdbObjProperty

# ﻿System Abstraction Layer

[[warning]]
**Warning**
This PyLabs System Abstraction Layer section needs complete review and may be inaccurate at this moment. We try to get it up to date as soon as possible.

Our apologies for any inconvenience.
[[/warning]]

The System Abstraction Layer, or in other words, System Wrappers, wrap the management (installation, management, upgrades, automation etc.) of an existing application or service.

Some examples of services and applications for which a System Wrapper can be created:

* An Apache web server.
* A MySQL database.
* A ZFS file system.
* A firewall.
* An IDE application for installation on desktops.

By creating a System Wrapper, the service or application becomes manageable from within the Pylabs framework. This means that the service or application can be installed, managed and automated in a uniform manner, whether it is through a command line interface or in automation scripts.

For example, the Apache web server system wrapper, allows easy and uniform management and automation of the Apache web server across different platforms.

System Wrappers are created as a set of Pylabs Extensions.
This section describes how to create a Pylabs System Wrapper, as a set of Pylabs Extensions.


## Architecture of a Pylabs System Wrapper

The schema below shows the structure of a System Wrapper.

![PylabsSystemWrapper][imgPylabsSystemWrapper]

[[note]]
**Note** 
Starting from PyLabs 5.0 it is recommended not to use the CMDB (Configuration Management Data Base) approach anymore, but just wrap system calls and implement the logic from a CMDB in your Q-Shell script calling the SAL.
[[/note]]


## Main Components

The System Wrapper consists of two extensions that work together:

* An application management extension.
* A command tool extension.


### Application Management Extension

The application management extension contains the modules to manage the application or service, such as starting or stopping it.

The extension can contain other modules, for example for the configuration of your application/service or a custom enumerator. You need to find a good balance in the granularity of your modules. Do not write too many modules, but neither too little. Both ways make it very hard to maintain and use the extension; too little modules makes it difficult to extend the management extension.

The management extension of the application or service consists of at least two modules:

* At least one configuration module: *CMDB Management*
* A management module: *Application Management*


#### Application Management Module:

The Application Management module is the module that contains the methods to manage the application, such as starting and stopping the application/service, or retrieving the configuration(s) of the application/service. The methods in the manage module make use of the CMDB object of the application/service.


#### CMDB Management Module:

The CMDB Management module stores the actual configuration of the application or service.
The configuration of the application or service is stored as a CMDB Object in the CMDB. The CMDB Object is a set of [Properties of Pylabs CMDB Objects][cmdbobjproperty], which can consist of a CMDB Sub Object(s) and Pylabs Types (`q.basetype + CMDB Name`).


### Command Tools Extension

This extension contains the methods that wrap the execution of the application or service such as starting and stopping. These methods should be called by the Application Management Module. 
It is not always necessary to have a command tools extension, such as when an API of a third party software package is used. For example, a Xen API is used instead of a self written Xen API.
