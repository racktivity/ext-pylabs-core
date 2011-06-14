# Actor Actions

After updating the model in a root object action, typically an actor action is called. An example of an actor action is changing the status of a machine or updating the IP address.
A change to the model will probably require a change in reality. Such an action will then use RScripts to change the reality on the machines. Typically actor actions should not contain any access to the DRP or start new root object actions.
Several actor actions can implement the same type of action, but for different technologies. An example would be configuring a hypervisor. The action actor to configure the hypervisor will be implemented for different hypervisors, such as the XEN and VirtualBox.
The action actor that configures a hypervisor for a VirtualBox should actually check the hypervisor is indeed a VirtualBox machine.
Actor actions are normal tasklets, they contain a 'match' and a 'main' function. The 'match' function is used to define the usage and the technology used in the RScripts which are started by the tasklet.


## How to Start an Actor Action

The code below initializes a hypervisor:

    q.actions.actor.hypervisor.initialize(pmachineguid, jobguid='', executionparams={})

[[note]]
**Note** 
This call should be executed in an environment where the workflow engine is running and initialized.
[[/note]]


## Example of an Actor Action

Below is an example of an actor action which configures a VIRTUALBOX30 hypervisor:

[[code]]
__author__ = 'aserver'
__tags__ = 'hypervisor', 'initialize'
__priority__= 3

def main(q, i, params, tags):
    agentguid = q.actions.rootobject.machine.getMachineAgent(params['pmachineguid'])['result']
    params['result'] = q.workflowengine.agentcontroller.executeActorActionScript(agentguid, 'hypervisor_initialize', {'machineguid': params['pmachineguid']})

def match(q, i, params, tags):
    hypervisortype = params['hypervisortype']
    return hypervisortype == q.enumerators.hypervisortype.VIRTUALBOX30
[[/code]]


## Actor Actions Programming Rules

The main goal is to start the correct RScripts.

It should **not**:

* Have access to the DRP.
* Start other actor actions or root object actions.
* Start external applications.