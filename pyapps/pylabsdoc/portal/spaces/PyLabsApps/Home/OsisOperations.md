@metadata title=OSIS Operations
@metadata order=45
@metadata tagstring=osis operation delete get store

[tasklet]: /#/Overview/Tasklets
[pyappdir]: /#/PyLabsApps/Introduction
[model]: /#/PyLabsApps/Modeling


#OSIS Operations
In the previous section you have learned how you can create OSIS views and that the views, with their objects, are stored in a PostgreSQL database.
In this section we will cover how you can store, update, and delete objects from these views.


##Creating an OSIS Operation
An OSIS operation is a [tasklet][] which is stored in the directory `<pyapp name>/impl/osis/<domain>/<root object>`. See the [PyApps Directory Structure][pyappdir] for more information about the location of the files.

Each file has the following identification:

* __author__ : name of the author of the tasklet
* __tags__ : set of tasklet identifications, used by the tasklet engine to retrieve the proper tasklet
* __priority__ : priority of the tasklet, the lower the value, the lower the priority


##Creating an OSIS Store and Update Operation
The store and update operation in an OSIS view are identical. The main flow is:

1. Create an OSIS connection
2. Get the Root Object from the params, offered to the tasklet
3. Set the values of the Root Object properties
4. Save the OSIS view


###Import Libraries
A first thing to add to the OSIS view is the import of the `OsisDB` library:

[[code]]
from osis.store.OsisDB import OsisDB
[[/code]]

Import other libraries if necessary but that is not likely.

Typically we also define some global variable, such as the domain, the Root Object, and the corresponding OSIS view.

[[code]]
ROOTOBJECT_TYPE = 'sampleapprootobject'
DOMAIN = "sampleappdomain"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)
[[/code]]


###Connecting to OSIS
In the `main` function of the tasklet you have to create a connection to OSIS. The function uses five arguments: `q`, `i`, `p`, `params`, and `tags`. `p` represents the PyApp name space and `params` is a dictionary filled by the PyLabs framework. 

[[code]]
def main(q, i, p, params, tags):
    osis = OsisDB.getConnection(p.api.appname)
[[/code]]    


###Storing or Updating the Root Object in an OSIS View
A first step to store or update a Root Object is to get the Root Object from the `params` dictionary:

[[code]]
rootobject = params['rootobject']
[[/code]]

When you have the Root Object, you can set the different values of the Root Object properties.

[[code]]
values = {
    'property1': rootobject.property1
    'property2': rootobject.property2,
    'property3': rootobject.property3,
    'property4': rootobject.property4
    }
[[/code]]    

The properties of the Root Object are all defined in the [Root Object Model][model].

When you have set the values of the Root Object, you only have to save the view with the new or updated Root Object. This action is a method on the osis connection and expects the following arguments in the given order:

* domain to which the view belongs
* the name of Root Object
* name of the osis view
* guid of the Root Object
* version of the Root Object
* a dictionary with values

Use the `viewSave` method as follows:

[[code]]
osis.viewSave(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobject.guid, rootobject.version, values)
[[/code]]


###Tasklet Execution
The store and update tasklet can only be executed when the `rootobjecttype` in the `params` dictionary matches the given Root Object type. This must be defined in the `match` function of the tasklet:

[[code]]
def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
[[/code]]    


##Example of an OSIS Store

[[code]]    
__author__ = 'Incubaid'
__tags__ = 'osis', 'store'
__priority__= 1

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'sampleapprootobject'
DOMAIN = "sampleappdomain"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, p, params, tags):
    osis = OsisDB.getConnection(p.api.appname)

    rootobject = params['rootobject']

    values = {
        'property1': rootobject.property1
        'property2': rootobject.property2,
        'property3': rootobject.property3,
        'property4': rootobject.property4
        }

    osis.viewSave(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
[[/code]]    


##Creating an OSIS Delete Operation
The flow of a delete operation in an OSIS view is similar to the create/update operation flow. First create a connection to OSIS, get Root Object data, and finally update the OSIS view by deleting the Root Object.


###Retrieving the Root Object Data
To delete a Root Object from an OSIS view, you only need its guid. The guid is stored in the `params` dictionary and can be retrieved as follows:

[[code]]
rootobjectguid = params['rootobjectguid']
[[/code]]

To delete the object, you must use the `viewDelete` method on the the OSIS connection object. This method expects the following arguments in the given order:

* domain to which the view belongs
* the name of Root Object
* name of the osis view
* guid of the Root Object

Use the `viewSave` method as follows:

[[code]]
osis.viewSave(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobjectguid)
[[/code]]


###Tasklet Execution
The store and update tasklet can only be executed when the `rootobjecttype` in the `params` dictionary matches the given Root Object type. This must be defined in the `match` function of the tasklet:

[[code]]
def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
[[/code]]    


##Example of an OSIS Delete

[[code]]
__author__ = 'Incubaid'
__tags__ = 'osis', 'delete'
__priority__= 3

from osis.store.OsisDB import OsisDB

ROOTOBJECT_TYPE = 'lead'
DOMAIN = "crm"
VIEW_NAME = '%s_view_%s_list' % (DOMAIN, ROOTOBJECT_TYPE)

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)

    rootobjectguid = params['rootobjectguid']
    rootobjectversionguid = params['rootobjectversionguid']

    osis.viewDelete(DOMAIN, ROOTOBJECT_TYPE, VIEW_NAME, rootobjectguid, rootobjectversionguid)

def match(q, i, params, tags):
    return params['rootobjecttype'] == ROOTOBJECT_TYPE
[[/code]]    


##What's Next?
So far you have learned about: 

* modeling Root Objects and its interfaces
* the creation of OSIS views and their purposes
* the creation of OSIS operations

In a next step we will discuss how you can implement the actions of a Root Object. 
