#Implementing Action Tasklets
For each Root Object you have created an [interface](/sampleapp/#/doc/action). The interface file contains the different actions that you can perform on the Root Object.
The examples of the tasklets so far did not create objects in Arakoon. 

In this section we will take the step to the actual management of Root Objects: create, delete, update Root Objects, create lists, find objects, ...

Besides the most common actions, you can of course create your own specific action, but remember that, for each defined action in the interface, you have to create one action tasklet.


##Before Creating Tasklets
What do you need to know before you start implementing the Root Object Interface?

The tasklets have the same structure as any other [tasklet](http://confluence.incubaid.com/display/PYLABS/Tasklets).

[[code]]
__author__='incubaid'
    
def main(q, i, p, params, tags):
    code to implement action

    params['result']=something

def match(q, i, params, tags):
    return True
[[/code]]


###File Name and Location
In PyLabs 5, it is recommended that the file name of an action tasklet has the following structure:

`<priority>_<rootobject>_<action>.py`

* priority: integer value, indicating the priority of the tasklet, 1 is lowest priority 
* rootobject: name of the Root Object, all lower-case
* action: name of the action, as defined in the interface file of the proper Root Object

When you use the new file names for the action tasklets, do not use the `__priority__` and `__tags__` parameters inside the tasklet.
The `__priority__` is replaced by the priority indication in the file name of the tasklet.
The `__tags__`  parameter is replaced by the folder names in which the tasklet resides. Take a look at the action tasklet `1_customer_create.py` of the 'sampleapp'. 
This file is located in `/opt/qbase5/pyapps/sampleapp/impl/action/crm/customer/create`, where `crm` is a domain inside the 'sampleapp' application. All folder names, including the domain name, are used as tags of the tasklet.

See the [PyApps Directory Structure](/sampleapp/#/doc/sampleapp) for more information about the location of the files.

__Note:__ It is possible to still use the old tasklet file names and use the `__priority__` and `__tags__` parameters inside the tasklet, but it is recommended not to mix them.


###Provided Data
The execution of the action tasklet mostly requires a lot of data about an object. This data is not to be retrieved in this action tasklet itself, but is gathered in the `params` dictionary. 
The `params` dictionary lives throughout the whole PyLabs framework. You will see in the [Creating Forms and Wizards](/sampleapp/#/doc/formwizardparctical) section, that the wizards and forms gather the data. This data is passed on to the cloud API call, which on its turn calls this tasklet. 

All of this is part of the PyLabs framework.

The next sections will cover the basic principles of implementing the actions.

##Creating Objects
Creating objects to store in the DRP always takes three phases:

1. Create a new object
2. Set the properties
3. Save the object in the DRP


###Creating an Empty Object
To create an empty root object:

    object = p.api.model.<domain>.<rootobject>.new()

For example:

    lead = p.api.model.crm.lead.new()

This creates an empty object. If you would save this empty object, it will be saved with some basic properties, such as a guid and a creation date. 
All other properties, which are defined in the [modeling](/sampleapp/#/doc/modeling) phase are empty.


###Setting Properties
With the created object, it becomes very easy to set its properties.

[[code]]
lead.name = params['name']
lead.code = params['code']
lead.customerguid = params['customerguid']
lead.source = params['source']
lead.type = params.get('type')
lead.status = params.get('status')
lead.amount = params.get('amount')
lead.probability = params.get('probability')
[[/code]]

You notice that we use two different ways to set a property.
The first way, `params['keyword']`, returns the value of the keyword in the `params` dictionary, but in case the given keyword does not exist in the dictionary, the complete creation of the object will fail. For example, if the `params` dict does not contain the keyword `code`, the lead object will not be created. This way of setting properties is mainly used for key properties of the object.
The second option, `params.get('keyword')`, also returns the value of the keyword, but in case the given keyword does not exist in the dictionary, `None` is returned as value. This means that the object can still be created even though the property is not available in the `params` dictionary.


###Saving the Object
Saving the object is similar to creating the object:

[[code]]
object = p.api.model.domain.RO.save(created object)
[[/code]]

In the given example:
    
[[code]]    
lead = p.api.model.crm.lead.save(lead)
[[/code]]

It is also required to add the guid of the object to the keyword 'result' in the `params` dictionary. See the [Defining Actions Interface on Root Objects](/sampleapp/#/doc/action) chapter for more information.

[[code]]
params['result'] = lead.guid
[[/code]]


##Getting Full Objects
Sometimes it will be required that you retrieve a full object from the database, for example to update properties. The best way to get an object is to create a `getObject`-function on a Root Object. This way you can grab an object any time you want, since it is available in an application client. This client communicates with the application server, which on its turn can access the DRP.
The alternative is to grab the object via the model, but this is only possible if you are working in the application server environment itself, which is not likely.

To get the object:

[[code
object = p.api.model.domain.rootobject.get('rootobjectguid')
params['result'] = object
[[/code]]

It is recommended to add some error handling for example to throw an error in case the guid key is not available in the `params` dictionary.

[[code]]
TYPE = "lead"
GUID_FIELD = "%sguid" % TYPE

def main(q, i, p, params, tags):
    if GUID_FIELD not in params:
        raise ValueError("Cannot retrieve %s, there is no %s key in the params" % (TYPE, GUID_FIELD))
    guid = params[GUID_FIELD]

    object = p.api.model.crm.lead.get(guid)
    params['result'] = object
[[/code]]    

With this tasklet you have retrieved a complete object and added it to the `params` dictionary.


##Updating Objects
No Root Object is a static piece of data, you will need to update it over time. The update of an object overwrites old values with new values. These new values are passed to the tasklet via the `params` dictionary. The least effective and therefore not recommended way is to retrieve the object and then set the properties one by one, even if the value remains the same.

[[code]]
lead = p.api.model.crm.lead.get(params['leadguid'])
lead.name = params['name']
lead.code = params['code']
lead.customerguid = params['customerguid']
lead.source = params['source']
lead.type = params.get('type')
lead.status = params.get('status')
lead.amount = params.get('amount')
lead.probability = params.get('probability')
p.api.model.crm.lead.save(lead)
[[/code]]

Better is to store the properties of the Root Object in a list and check if the property is actually present in the `params` dictionary. On the retrieved object, you can execute a `setattr` function to set the new value.

[[code]]
FIELDS = (
        'name',
        'code',
        'customerguid',
        'source',
        'type',
        'status',
        'amount',
        'probability'
        )

def main(q, i, p, params, tags):
    object = p.api.model.crm.lead.get(params['leadguid'])

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not updating field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None:
            q.logger.log("Field %s is None: not updating field %s" % (field, field), 7)
            continue

        q.logger.log("Updating field %s to value %s" % (field, value), 7)
        setattr(object , field, value)
[[/code]]        


##Deleting Objects
Deleting an object is a very simple tasklet:

1. Get the object guid out of the `params` dictionary
2. Delete the object by using the retrieved guid

For example:

[[code]]
TYPE = "lead"
GUID_FIELD = "%sguid" % TYPE

def main(q, i, p, params, tags):
    if GUID_FIELD not in params:
        raise ValueError("Cannot delete %s, there is no %s key in the params" % (TYPE, GUID_FIELD))
    guid = params[GUID_FIELD]

    p.api.model.crm.lead.delete(guid)
    params['result'] = True
[[/code]]    


##Creating Lists
In the [OSIS Views](/sampleapp/#/doc/osisviews) chapter, you have learned how you can create different views on a Root Object. These views can now be used to create a list.

A first step in this action is to get the model of a Root Object. On the model object, you create a filter object, which allows you to create your own filters. In this case the filter will be based on an OSIS view that you have created.

[[code]]
TYPE = "lead"
DOMAIN = "crm"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def main(q, i, p, params, tags):
   filter = p.api.model.crm.lead.getFilterObject()
[[/code]]   

To add rows to the list:

[[code]]
FIELDS = (
        'name',
        'code',
        'customerguid',
        'source',
        'type',
        'status',
        'amount',
        'probability'
        )

for field in FIELDS:
    if field not in params:
        q.logger.log("Field %s not in params dict: not searching for field %s" % (field, field), 7)
        continue

    value = params[field]
    if value is None:
        q.logger.log("Field %s is None: not searching for field %s" % (field, field), 7)
        continue

    q.logger.log("Adding filter on field %s with value value %s" % (field, value), 7)
    f.add(VIEW, field, value)
[[/code]]    

A last step is to store the actual list.

[[code]]
result = p.api.model.crm.lead.findAsView(filter, VIEW)
params['result'] = result
[[/code]]

All together this leads to the following tasklet which creates a list:

[[code]]
__author__ = "Incubaid"

FIELDS = (
        'name',
        'code',
        'customerguid',
        'source',
        'type',
        'status',
        'amount',
        'probability'
        )

TYPE = "lead"
DOMAIN = "crm"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def get_model_handle(p):
    return p.api.model.crm.lead

def main(q, i, p, params, tags):
    handle = get_model_handle(p)

    f = handle.getFilterObject()

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not searching for field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None:
            q.logger.log("Field %s is None: not searching for field %s" % (field, field), 7)
            continue

        q.logger.log("Adding filter on field %s with value value %s" % (field, value), 7)
        f.add(VIEW, field, value)

    result = handle.findAsView(f, VIEW)
    params['result'] = result
[[/code]]    


##What's Next
In this section you have learned to create the basic operations on a Root Object. This section does not cover all possible actions, but it should give you a good idea about the principles of creating actions.

In a next step we will discuss how you can create your own forms and wizards of your PyApp. A form and a wizard are both UI elements of your PyApp. 
These elements allows you to interact with the user, for example ask for a confirmation or request input.

