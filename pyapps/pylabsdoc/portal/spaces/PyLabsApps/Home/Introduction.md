@metadata title=Introducing PyApps
@metadata order=10
@metadata tagstring=intro pyapp architecture drp create

[imgPyAppArch]: images/images50/pyapps/PyApp_Architecture.png
[imgDrp]: images/images50/pyapps/PyLabs_DRP.png
[imgPyApp]: images/images50/pyapps/PyApp.png
[imgPyAppCreate]: images/images50/pyapps/PyApp_Create.png
[drp]: /#/PyLabs50/Architecture
[epydoc]: http://epydoc.sourceforge.net/


#PyLabs Applications

##Introducing PyApps
A PyApp is an application which is created on top of the PyLabs framework.
Each PyApp consists of the same components, such as Root Objects, actions, wizards, forms, tasklets, ...

In this section we introduce you to the different components of PyApps and how they interact.


###Architecture
Below you can find the architecture of how the PyLabs framework is built.

![PyApps_Architecture][imgPyAppArch]

![PyLabs_DRP][imgDrp]

Arakoon: key/value store of objects, non-queryable, no relational DB. This database is used to store the actual objects of your application.

PostgreSQL: open source relational db, used for views, fast, queryable. This database is used to store views on objects. For example, you can create a view on a customer which save its name and address. This view and its data will be stored in this PostgreSQL database. Via OSIS, these views are populated and updated.

OSIS: Object Store and Indexing System, this is a layer on top of Arakoon and PostgreSQL. OSIS has two functions:

* store and retrieve Thrift Serialized Objects in and from Arakoon
* store and update views in PostgreSQL


###PyModel
PyModel is a PyLabs extension to define, create, and update complex objects. PyModel is capable of serializing Thrift objects to store them in Arakoon, as well as deserializing these objects for further usage in your application.
The PyModel extension is represented by `p.api.model in PyLabs`.


###Root Objects
A Root Object of a PyApp is a logical unit in the [DRP][drp] (Datacenter Resource Planning). The Root Object is a composite entity of properties, components and references to other Root Objects.

For example:
The Root Object "Customer" can have the properties Name, Description, Address,... It can have contact person as component and can be in relation with another customer via a reference.


###Actions
An Action is a definition of possible operations on root objects. The definition determines which arguments the operation expects and what the result must be of the operation. 

Per action, there exists one tasklet which contains the business logic and the actual code for the operation.


###From Modeling to Reality
Below you find a graphical overview of the creation of a PyApp. 

![PyApp][imgPyApp]


##PyApps Directory Structure
Below you can find the directory structure of a PyApp.

    pyapps/
    `-- myappname
        |-- interface
        |   |-- action
        |   |   `-- domainname
        |   |       |-- rootobject1.py (interface on root object)
        |   |       `-- rootobject2.py
        |   |-- actor
        |   |   `-- domainname
        |   |       |-- actor1.py (model of an actor object)
        |   |       `-- actor2.py
        |   |-- config
        |   |   `-- rootobjectname
        |   |       `-- configuration1.py (model of a pyapp configuration)
        |   |-- model
        |   |   `-- domainname
        |   |       |-- object1.py (model of root object)
        |   |       `-- object2.py
        |   `-- monitoring
        |       `-- monitoringobject1.py (model of a monitoring object)
        |
        |-- impl (actual implementation of the pyapp)
        |   |-- action (contains the different actions of the pyapp)
        |   |   `-- domainname (domain in the pyapp)
        |   |       `-- rootobjectname (a root object of the pyapp)
        |   |           `-- methodname (action on a root object)
        |   |               `-- tasklet1.py (actual implementation)
        |   |-- actor (to create something in reality) 
        |   |   `-- domainname (domain in the pyapp)
        |   |       `-- actorname
        |   |           `-- methodname (name of the action)
        |   |               |-- scripts (directory for rscripts)
        |   |               |   `-- rscript1.rscript (script to be executed by agent)
        |   |               `-- tasklet1.py (tasklet to make rscript by an agent)
        |   |-- authenticate
        |   |   `-- authenticate.py
        |   |-- authorize
        |   |   `-- authorize.py
        |   |-- events (define actions triggered by a pyapp event)
        |   |   |-- event_action1
        |   |   |   |-- consumer.cfg (configuration when action must be triggered)
        |   |   |   |-- event_action1.py (action to be executed upon event)
        |   |   |   `-- event_action2.py
        |   |   `-- event_action2
        |   |       |-- consumer.cfg
        |   |       |-- event_action1.py
        |   |       `-- event_action2.py
        |   |-- init
        |   |   `-- portal 
        |   |       `-- portalaction.py (populate PyApps portal with pages)
        |   |-- osis (methods to delete/store objects from/in views in postgres db) 
        |   |   |-- config (config objects of pyapp)
        |   |   |   |-- config1_delete.py
        |   |   |   `-- config1_store.py
        |   |   |-- domainname
        |   |   |   `-- rootobjectname
        |   |   |       |-- objectname_delete.py
        |   |   |       `-- objectname_store.py 
        |   |   |-- generic (generic osis methods)
        |   |   |   `-- tasklet.py
        |   |   |-- monitoring 
        |   |   |   |-- monitoring_delete.py
        |   |   |   `-- monitoring_store.py
        |   |   `-- ui (related to UI objects)
        |   |       |-- ui_object_delete.py
        |   |       `-- ui_object_store.py
        |   |-- schedule
        |   |   `-- domainname
        |   |       `-- rootobjectname
        |   |           |-- schedule1.py
        |   |           `-- schedule2.py
        |   |-- setup
        |   |   `-- osis (define view to be stored in postgres db)
        |   |       |-- tasklet1.py
        |   |       `-- tasklet2.py
        |   `-- ui (pyapp UI definitions)
        |        |-- form (form definitions)
        |        |   `-- domainname
        |        |       `-- rootobject_action
        |        |           `-- tasklet1.py
        |        `-- wizard (wizard definitions)
        |            `-- domainname
        |                `-- rootobject_action
        |                    `-- tasklet1.py
        |
        `-- portal (documentation of pyapp)
            |-- spaces
            |   |-- api (api doc of pyapp)
            |   |-- doc (manual of pyapp)
            |   |   |-- doc1.md
            |   |   `-- doc2.md
            |   `-- domainname
            |       `-- Home.md
            `-- static (static data to be included in pyapp doc)
                `-- images
                    |-- image1.jpg
                    `-- image2.jpg
            

###interface
The `interface`-directory contains the files that model your complete PyApp.


####interface/action/*domainname*
* action: this is the directory that contains the modeling of the actions on the different objects of your PyApp.
* *domainname*: name of the domain to which the action belongs, this avoids the usage of actions in other parts of your PyApp.
    - config: this domain refers to the configuration of PyApp module.
    - core: default directory, this is for core functionalities which are common for each PyApp that you create.
    - ui: actions on UI objects, such as finding or creating pages.
    - *pyappname*: contains the modeling of actions per root object, specific for your own PyApp.


####interface/actor/domainname
* actor: this directory contains the model of actors in your PyApp. An actor is your interface to the reality. Tasklets in this section will interact with the reality, for example send an e-mail.
* domainname: this will mainly be the name of your PyApp, `crm` in case of this sample PyApp.


####interface/config
* config: contains the model of a PyApp specific module, for example a `pop3` object.


####interface/model/domainname
* model: contains the model of root objects in your PyApp
* domainname: name of the domain to which the root object belongs, this avoids the usage of root objects in possible other installed PyApps. This directory contains one file per root object. Each file is the complete definition of an object.


####interface/monitoring
* monitoring: model of a monitoring object


###impl
The `impl`-directory contains all the code that perform an action in your PyApp, for example create an object. 


####impl/action/*domainname*/rootobjectname/methodname
* action: this is the directory that contains the actions as defined in the interface on a Root Object.
* *domainname*: name of the domain to which the action belongs, this avoids the usage of actions in other parts of your PyApp. The domain names can be:
    - config: this domain refers to the configuration of the PyApp itself.
    - core: default directory, this is for core functionalities which are common for each PyApp that you create.
    - ui: actions on UI objects, such as finding or creating pages.
    - *pyappname*: actions, specific for your own PyApp.
* rootobjectname: name of the Root Object.
* methodname: name of the method, as defined in the interface file of the proper Root Object. This directory contains the actual files (tasklets) that execute something in the PyApp. 


####impl/actor/domainname/actorname/methodname/scripts
* actor: this directory contains the definitions of actors in your PyApp. An actor is your interface to the reality. Tasklets in this section will interact with the reality, for example send out an e-mail.
* domainname: this will mainly be the name of your PyApp, `crm` in case of this sample PyApp.
* actorname: meaningful name for the actor of your PyApp.
* methodname: name of the action that the actor will execute. This directory contains tasklets that provide the data of which scripts must be executed by whom. The scripts-directory is a subdirectory of the action-directory.
* scripts: this directory contains the scripts that are executed by the PyLabs agents. They execute something in reality, for example send out a mail.


####impl/authenticate
This directory contains tasklets that authenticates users in the PyApp.


####impl/authorize
This directory contains tasklets that authorizes users for sections in the PyApp. For example, user A is an administrator who is allowed to do everything in the PyApp, but user B has only rights to view data in the PyApp.


####impl/events/actionname
* events: this is the directory to define actions which are triggered by an event.
* actionname: this directory contains a configuration file and tasklets, which are executed upon a configured event.


####impl/init/portal
* init: this directory contains the actions that must be run at the start of your PyApp
* portal: this directory contains the tasklets that populate your PyApps' portal with content


####impl/osis/domainname/rootobjectname
* osis: this directory contains the actions that will populate the created views in your PyApp.
* domainname: name of the domain to which the action belongs, this avoids the usage of actions in other parts of your PyApp.
* rootobjectname: name of the Root Object, only in case of a specific PyApp domain name.


####impl/schedule/domainname/rootobjectname
* schedule: in this directory we place tasklets which can be scheduled, for example, check for mail every 300 seconds. The tasklets themselves are stored per domain name.
* domainname: name of the domain to which the scheduled action belongs.
* rootobjectname: name of the Root Object.


####impl/setup/osis
* setup: this directory is used to set up your OSIS views.
* osis: contains the actual tasklets that create the OSIS views that you want. For example a list of all customers with their name or a list of all customers with all details results in two different tasklets.


####impl/ui/*UI type*/domainname
* ui: the directory for all UI related actions, such as wizards and forms that need to be displayed in your PyApp.
* *UI type*: the type of UI element that needs to be displayed. This is either `form` or `wizard`.
* domainname: name of the domain to which the UI element belongs.


###portal
The `portal`-directory contains all the documentation files of your PyApp.


####portal/spaces/api
* api: contains the API documentation of your PyApp in [epydoc][] format. The API documentation is generated when installing your PyApp.
__Note__: Epydoc is a tool for generating API documentation for Python modules, based on their docstrings.


####portal/spaces/doc
* doc: contains the actual documentation of your PyApp


####portal/spaces/domainname
* domainname: name of the domain of your PyApp, this directory must contain the landing page of your PyApp


####portal/static
* static: contains static files, that can be referenced to from your documentation, mainly images.


##Process of Creating a PyApp


###General Steps

Below you can find a general overview of the creation process of a PyApp.

![PyApp\_Create][imgPyAppCreate]

1. Create the Specifications of the PyApp
2. Model the different Root Objects
3. Model the Root Object interface (actions)
4. Create OSIS views
5. Implement the OSIS population actions
6. Implement the defined interfaces
7. Implement wizards and forms

From a practical point of view, you have to:

1. Install PyLabs
2. Create the PyApp Directory structure
3. Create at least one model file
4. Install the PyApp via the Q-Shell: `p.application.install('yourPyApp')`

After this installation command you see the API that you have created.

[[information]]
**Information**

After _each change_ in your PyApp, for example you have added a new Root Object model, you have to reinstall your PyApp:

`p.application.reinstall('yourPyApp')`
[[/information]]


###Advanced
1. Define actions triggered by Events
2. Scheduled Actions
3. Debugging a PyApp

##Conclusion
This concludes the introduction to PyApps. In this chapter you have seen the structure of PyApps and the steps to create PyApps. In the next chapters, we go into detail of the creation of a PyApp, taking the *sampleapp* as example.
