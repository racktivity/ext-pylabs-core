#Creating a PyLabs Application

##Introducing PyApps
Explain PyLabs/PyApps: drp/model/actions/actors/osis/app domain/...
A PyLabs Application (PyApp) is an application designed to run on the PyLabs 5 
framework. Each PyApp consists of the same components, such as Root Objects 
(RO), Actions, Wizards, Forms, ...

###Architecture
*insert architecture scheme here*

Arakoon: key/value store of objects, non-queryable, no relational DB
PostgreSQL: open source relational db, used for views, fast, queryable 

OSIS: on top of Arakoon and PostgreSQL, sort of interface to postgresql/
arakoon, crud on objects in arakoon/postgresql, create views for fast indexing

###PyModel
PyModel is p.api.model.domain.RO, get/store objects from/in Arakoon and/or 
PostgreSQL. The get-function is a deserialization process of an object, the 
store-function is a serialization process of an object

####Root Objects
A Root Object of a PyApp is a logical unit in the DRP (Datacenter Resource 
Planning). The Root Object is a composite entity of properties, components and
references to other Root Objects.

For example:
The Root Object "Customer" can have the properties Name, Description, Address,
... It can have contact person as component and can be in relation with another
 customer via a reference.

###Actions
Define possible actions on a root object, define args per function, define 
result of action

Per action, there exists 1 tasklet which contains the biz logic and the actual 
code

###From Modelling to Reality
graphical overview with steps from specs over model to reality

###PyApps Directory Structure
Below you can find the directory structure of a PyApp.

    pyapps/
    `-- myappname
        |-- cfg
        |-- portal
        |   |-- static
        |   |-- doc
        |   `-- api
        |-- impl
        |    |-- action
        |    |   `-- domainname
        |    |       `-- rootobjectname
        |    |           `-- methodname
        |    |               `-- tasklet1.py
        |    |-- actor
        |    |   `-- domainname
        |    |       `-- actorname
        |    |           `-- methodname
        |    |               `-- tasklet1.py
        |    |-- osis
        |    |   `-- domainname
        |    |       `-- tasklet1.py
        |    |-- service
        |    |   `-- domain
        |    |       |-- service1.py
        |    |       `-- service2.py
        |    |-- setup
        |    |   |-- tasklet1.py
        |    |   `-- tasklet2.py
        |    |-- config
        |    |   |-- tasklet1.py
        |    |   `-- tasklet2.py
        |    |-- ui
        |    |   |-- form
        |    |   |   `-- tasklet1.py
        |    |   |-- portal
        |    |   |   `-- tasklet1.py
        |    |   `-- wizard
        |    |       `-- tasklet1.py
        |    |-- portal
        |    `-- worker
        |-- client (*)
        |    `-- action
        `-- interface
             |-- action
             |   `-- domainname
             |       |-- rootobject1.py
             |       `-- rootobject2.py
             |-- actor
             |   `-- domainname
             |       |-- actor1.py
             |       `-- actor2.py
             `-- pymodel
                 `-- domainname
                     |-- object1.py
                     `-- object2.py




##Root Objects
Define Root Objects (specs)
Model Root Objects (pyapps>app>interface>pymodel>domain>RO.py)

##Actions
Define interface/actions per root object (pyapps>app>interface>action>domain>RO.py)

##OSIS actions
what is, purpose, ...

###Views
Create views on RO in osis

###Wizards and Forms
Create wizards/forms per defined action (pyapps>app>impl>ui>form/wizard>RO_action.py)

Implement wizards on osis level

##Turning Model into Reality
Implement the real action
