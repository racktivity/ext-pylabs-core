@metadata title=Workflow Engine
@metadata order=40
@metadata tagstring=wfe workflow engine

[architecture]: /#/Overview/Architecture
[stackless]: http://www.stackless.com/
[qpinstall]: /#/Q-Packages/QPInstall
[imgWFE]: images/images50/pylabs/WorkflowEngineHighLevel.png
[imgAC]: images/images50/pylabs/AgentController.png
[imgWfeTasklet]: images/images50/pylabs/WFETasklets.png


# Workflow Engine

The Workflow Engine (WFE) acts like a scheduler for an operating system. It is used to execute different Root Object (RO) Actions and Actor Actions. It also starts the RScripts on the correct Agent. The name scheduler is used because the correct order of executing the different actions is scheduled by the workflow engine.


## High-Level Overview
From a high level perspective, the workflow engine consists of two different components.

![WFE_Overview][imgWFE]


One is a _Tasklet Engine_ which is responsible for the launching and monitoring of tasklets. 
The other component is called the _Agent Controller_. All actor actions that need to interact with a remote agent will do this by contacting the Agent Controller (AC). 
The Agent Controller is a special kind of agent that is running as part of the workflow engine. It is special in the sense that it is the only agent that is allowed to communicate with all other agents.

If you are not familiar with the concepts of Root Object Actions, Actor Actions and RScripts, be sure to take a look a the [PyLabs Architecture][architecture] page.

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
