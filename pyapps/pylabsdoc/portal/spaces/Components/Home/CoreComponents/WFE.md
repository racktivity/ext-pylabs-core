@metadata title=Workflow Engine
@metadata tagstring=workflow engine tasklet action job

[architecture]: #/Overview/Architecture
[stackless]: http://www.stackless.com/
[qpinstall]: #/Q-Packages/QPInstall
[imgWFE]: images/images51/pylabs/WorkflowEngineHighLevel.png
[imgAC]: images/images51/pylabs/AgentController.png
[imgWfeTasklet]: images/images51/pylabs/WFETasklets.png


# Workflow Engine

The Workflow Engine (WFE) acts like a scheduler for an operating system. It is used to execute different Root Object (RO) Actions and Actor Actions. It also starts the RScripts on the correct Agent. The name scheduler is used because the correct order of executing the different actions is scheduled by the workflow engine.


## High-Level Overview
From a high level perspective, the workflow engine consists of two different components.

![WFE_Overview][imgWFE]


One is a _Tasklet Engine_ which is responsible for the launching and monitoring of tasklets. 
The other component is called the _Agent Controller_. All actor actions that need to interact with a remote agent will do this by contacting the Agent Controller (AC). 
The Agent Controller is a special kind of agent that is running as part of the workflow engine. It is special in the sense that it is the only agent that is allowed to communicate with all other agents.

If you are not familiar with the concepts of Root Object Actions, Actor Actions and RScripts, be sure to take a look a the [Pylabs Architecture][architecture] page.

When the remote execution of an RScript is requested, the Agent Controller sends the RScript to correct agent over the XMPP communication channel. After receiving the script the agent executes it. When the script is executed, the agent reports back the status code and the captured output.

![Agent_Controller][imgAC]


## Workflow Engine Tasklet Execution Model

The workflow engine is a single-threaded Python process that is responsible for the scheduling of the tasklets. Instead of using regular threads to schedule the different tasklets, the workflow engine uses microthreads. 
The workflow engine schedules the execution of all the different tasklets in a single thread using the microthreads and scheduler provided by [Stackless Python][stackless].

![WFE_Tasklets][imgWfeTasklet]

The image above shows an example of a running workflow engine. Each of boxes portrayed in the diagram of the workflow engine represents a tasklet. As mentioned before each of these tasklets runs in a single thread. 
As a result of this approach it is imperative that a tasklet does not perform a blocking system call, except in some well-defined cases that can be detected by the stackless scheduler. If the tasklet would perform a blocking call, this means that the entire workflow engine hangs and brings the entire environment to a halt!

As you can see in the diagram there are some interactions with the network from inside the workflow engine. It is imperative that the network calls never block. To achieve this, the workflow engine uses a modified version of the standard socket module that uses non-blocking calls in combination with interactions with the stackless scheduler primitives to simulate the required blocking behavior.

One thing worth noting is that all write-interactions with the DRP go through a single tasklet that is responsible for all modifications in the DRP triggered by the Root Object actions.


## Installing the Workflow Engine

Install the latest version of the Q-Package named 'workflowengine'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


## Location in the Sandbox

* *XML-RPC interface for debugging the workflow engine:* `/opt/qbase5/apps/applicationserver/services/wfe_debug`
* *The main workflow engine daemon:* `/opt/qbase5/apps/workflowengine`
* *Configuration and management interface:* `/opt/qbase5/lib/pymonkey/extensions/workflowengine/manage`
* *Workflow engine library:* `/opt/qbase5/lib/python/site-packages/workflowengine`


## Managing the Workflow Engine

### Management Extensions

* To start the workflow engine:

    q.manage.workflowmanage.start()

* To stop the workflow engine:

    q.manage.workflowmanage.stop()

* To restart the workflow engine:

    q.manage.workflowmanage.restart()

* To get the status of the workflow engine:

    q.manage.workflowmanage.getStatus()

* To kill the workflow engine:

    q.manage.workflowmanage.kill()


### Q-Packages Start & Stop Tasklets

Get a reference of the 'workflowengine' Q-Package that you previously installed. This can be done the same way we installed the package:

    i.qp.find('workflowengine')

Followed by choosing the version of the package you installed if more than one is present.

Now you can use the start and stop tasklets as follows:

* Start:

    i.qp.lastPackage.qpackage.start()

* Stop:

    i.qp.lastPackage.qpackage.stop()


## Configuring the Workflow Engine

The Workflow Engine is using the configuration framework and is accessible on:

    i.config.workflowengine

Parameters which should be configured:

* *osis_address:* Address of the OSIS server.
* *osis_service:* Name of the OSIS service.
* *xmppserver:* DNS address of the XMPP server.
* *agentcontrollerguid:* The agent GUID of the agent controller.
* *password:* Password of the agent controller on the XMPP server.


## Workflow Engine API

Every component can be used via the Workflow Engine API.
Several functions are available in the 'q' tree/namespace.

[[note]]
**Note**

The methods in the hooks below are carried out when a workflow engine process starts, yet you do not have direct access to them.
[[/note]]


### Agent Controller

Functions to start a remote script on a agent or to kill it.

Accessible on:

    q.workflowengine.agentcontroller.

* *executeScript(agentguid, actionname, scriptpath, params, executionparams={}, jobguid=None):* Execute a script on an agent. The action will be executed in a new job that is the newest child of the current job.
* *executeActorActionScript(agentguid, scriptname, params, executionparams={}, jobguid=None):* Execute an actor action script on an agent. The action will be executed in a new job that is the newest child of the current job.
* *killScript(self, agentguid, jobguid, timeout):* Kill a script.

For more parameters check the Q-Shell and use q.workflowengine.agentcontroller. to get more information about the paramters and calls.


### Job Manager

Normally you shouldn't use those functions they are mainly used internally in the Workflow Engine.

Accessible on:

    q.workflowengine.jobcontroller.

More information can be gathered by using the help functionallity in Pylabs.

* *createJob(parentjobguid, actionName, executionparams, agentguid=None, params=""):* Create a job.
* *startJob(jobguid):* Start a job.
* *setJobDone(jobguid, result):* Set the job status to done.
* *setJobDied(jobguid, exception):* Set the job status to died'.
* *appendJobLog(jobguid, logmessage, level=5, source=""):* Append a log message to the a job log.
* *shouldWait(jobguid):* Pause a job.
* *getMaxduration(jobguid):* Get the maximum duration of a job.
* *registerJobFinishedCallback(jobguid):*
* *killJob(jobguid):* Kill a job.
* *isKilled(jobguid):* Check if a job is killed.

CreateJob will return a WFLJob object which has the following functions

* *isRootJob():* Check if the job has children.
* *start():* Start a job.
* *log(logmessage, level, source):* Add a log message to a job.
* *done(result):* Set the job status to 'done'.
* *died(exception):* Set the job status to 'died'.
* *create_drp_object():* Create a job DRP object.
* *commit_drp_object():* Commit a job object.


### Action Manager

Used to start Actor or RootObject Actions.

Accessible on:

    q.workflowengine.

More information can be gathered by using the help functionallity in pylabs.

* *startActorAction(self, actorname, actionname, params, executionparams={}, jobguid=None):* Starts a given Actor Action. Uses the tasklet engine to run the matching tasklets.
* *startRootobjectAction(self, rootobjectname, actionname, params, executionparams={}, jobguid=None):* Starts a given Root Object Action. Uses the tasklet engine to run the matching tasklets.
* *waitForActions(self, jobguids):* Wait for some background jobs to finish.


### Examples

* Start a machine:

    params =dict()
    params['machineguid'] = machineguid
    executionparams['rootobjectguid'] = machineguid
    executionparams['rootobjecttype'] = 'machine'
    q.workflowengine.actionmanager.startRootobjectAction('machine', 'start', params, jobguid=jobguid, executionparams=executionparams)

* Start an actor action which uses a hypervisor actor to start a machine:

    params =dict()
    params['machineguid'] = machineguid
    q.workflowengine.actionmanager.startActorAction('hypervisor', 'startVMachine', params, jobguid=jobguid, executionparams=executionparams)
