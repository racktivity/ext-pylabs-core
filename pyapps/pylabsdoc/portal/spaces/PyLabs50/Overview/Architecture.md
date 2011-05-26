[imgpyappArch]: images/pyapps/PyLabs_Architecture.png
[imgDRP]: images/images50/pylabs/PyLabs_DRP.png


## PyLabs Architecture
The PyLabs framework is a Python framework, specifically aimed at cloud application development. It provides all required components needed to build a typical cloud application. 
PyLabs covers a very wide range of functionality, from the basics such as logging services to an advanced workflow engine to oversee distributed program execution.

The framework itself is made up out of different logical layers. This page explains the different layers making up the full PyLabs stack and define the responsibilities of each layer. 

![PyApps_Architecture][imgpyappArch]

![PyLabs_DRP][imgDRP]

Arakoon: key/value store of objects, non-queryable, no relational DB. This database is used to store the actual objects of your application.

PostgreSQL: open source relational database, fast, and queryable. This database is used to store views on objects in the DRP. For example, you can create a view on a customer which save its name and address. This view and its data will be stored in this PostgreSQL database. Via OSIS, these views are populated and updated.

OSIS: Object Store and Indexing System, this is a layer on top of Arakoon and PostgreSQL. OSIS has two functions:

* store and retrieve Thrift Serialized Objects in and from Arakoon
* store and update views in PostgreSQL


### PyLabs Layers

* **Cloud API** and **Wizards**: This layer is the interface to the end-user. It provides the functionality to manage for example a virtualized datacenter.

* **DRP**: An object store built on top of the Object Storage and Indexing System (OSIS).

* **Root Object Actions**: These type of actions are designed to be abstract. Root object actions typically implement some kind of control flow. A Root Object Action can invoke other Root Object Actions or Actor Actions. These actions are also the only ones allowed to interact with the DRP. 
Each time a Root Object Action is invoked a job is created. Following this logic, each job can have multiple child jobs.

* **Actor Actions**: These kind of actions are more concrete than Root Object Actions. In this layer, interactions with DRP are strictly prohibited. Each time an Actor action is invoked a job is created, but these jobs cannot have child jobs.

* **RScripts**: These are small Python scripts that are executed remotely by the workflow engine. To find out more see the section on the workflow engine.

* **System Abstraction Layer**: This is the layer closest to the actual system. It is a facade that encapsulates the actual system commands.