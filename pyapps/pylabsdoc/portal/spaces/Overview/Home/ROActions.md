@metadata title=Root Object Actions
@metadata order=60
@metadata tagstring=root object ro action


# Root Object Actions

Root object actions typically implement some kind of control flow. A typical Cloud API call will result in a root object action. This root object action will contain code to change the model, start new sub root object actions or start actor actions.

An example would be starting all machines in a VDC:

1. The main root object action will call the DRP to get all machines in a VDC.
2. This root object action will then start a new root object action, for example a root object action called start machine, for every machine found in the VDC.
3. Start machine will call other root object actions to get new information or to configure firewalls and DHCP servers.
4. At the end the correct actor action is called to start the machine on the correct physical machine.


## Starting a Root Object Action

Use the action manager of the workflow engine to start a root object action. A  dictionary parameter can be defined to parse arguments to the root object action.

    q.actions.rootobject.machine.restore(backupmachineguid, executionparams=executionparams)

[[note]]
**Note**

This call should be executed in an environment where the workflow engine is running and initialized.
[[/note]]


## Example of a Root Object Action

Root object actions are just simple tasklets which use OSIS to change the DRP model. They can start new root object actions or actor actions. Below is an example of a root object action.

[[code]]
__author__ = 'aserver'
__tags__ = 'customer', 'addCapacityAvailable'
__priority__= 3

def main(q, i, params, tags):
     customer = q.drp.customer.get(params['customerguid'])
     capavailable = customer.capacityunitsavailable.new()
     capavailable.amount = params['amount']
     capavailable.capacityunittype = params['capacityunittype']
     for key in params.iterkeys():
        if key == "name":
           capavailable.name = params['name']
        if key == "description":
           capavailable.description = params['description']
     customer.capacityunitsavailable.append(capavailable)
     q.drp.customer.save(customer)
     params['result'] = True

def match(q, i, params, tags):
     return True
[[/code]]


## Root Object Action Programming Rules

Only call new root object actions or actor actions and do DRP changes.

Do not:
* Call RScripts.
* Use a SAL.
* Change the local configuration or files on the file system.