#Action Tasklets
For each Root Object you have created an [interface] (action.md). The interface file contains the different actions that you can perform on the Root Object.
The examples of the tasklets so far did not create objects in Arakoon. 

In this section we will take the step to the actual management of Root Objects: create, delete, update Root Objects, create lists, find objects, ...

Besides the most common actions, you can of course create your own specific action, but remember that, for each defined action in the interface, you have to create one action tasklet.


##Before Creating Tasklets
What do you need to know before you start implementing the Root Object Interface?

The tasklets have the same structure as any other [tasklet] (http://confluence.incubaid.com/display/PYLABS/Tasklets).

    __author__='incubaid'
    
    def main(q, i, p, params, tags):
        <code to implement action>

        params['result']=<something>
   
    def match(q, i, params, tags):
        return True


###File Name and Location
The file name of an action tasklet has always the following structure:

<priority>_<rootobject>_<action>.py

* priority: the priority of the tasklet, 1 is lowest priority 
* rootobject: name of the Root Object, all lowercase
* action: name of the action, as defined in the interface file of the proper Root Object

The <priority> replaces the `__priority__` inside the tasklet.
The <rootobject>_<action> combination replaces the `__tags__` inside the tasklet.

The tasklet is located in `<pyapp name>/impl/action/<domain>/<rootobject>/<action>`. See the [PyApps Directory Structure] (sampleapp.md) for more information about the location of the files.


###Provided Data
The execution of the action tasklet mostly requires a lot of data about an object. This data is not to be retrieved in this action tasklet itself, but is gathered in the `params` dictionary. As seen in the [Creating Forms and Wizards] (formwizardparctical.md) section, the wizards and forms gather the data. This data is passed on to the cloud API call, which on its turn calls this tasklet. 

All of this is part of the PyLabs framework.

The next sections will cover the basic principles of implementing the actions.

##Creating Objects

