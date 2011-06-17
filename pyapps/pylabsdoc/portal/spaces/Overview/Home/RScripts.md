@metadata title=RScripts
@metadata order=80
@metadata tagstring=rscript reality agent


# RScripts

RScripts are simple scripts which are executed remotely by an agent. They are linked to and started by an actor action. Typically SAL Pylabs extensions are used in the RScript.

Below are a few examples of what RScripts are used for:

* Starting and stopping services.
* Installing Q-Packages.
* Network setup.

As well as many more.

## Starting an RScript

    params['result'] = q.workflowengine.agentcontroller.executeActorActionScript(agentguid, 'hypervisor_initialize', {'machineguid': params['pmachineguid']})

The table below shows what each variable represents:

<table width="600">
<tr>
<th align="left" width="300" bgcolor="#D8D8D8">Parameter</th><th width="300" bgcolor="#D8D8D8">Represents</th>
</tr>
<tr>
<td>agentguid</td><td>The GUID of the agent which should execute the RScript.</td>
</tr>
<tr>
<td>'hypervisor_initialize'</td><td>The RScript which should be executed.</td>
</tr>
<tr>
<td>{'machineguid': params['pmachineguid']}</td><td>Parameters needed by the RScript.</td>
</tr>
</table>

[[note]]
**Note** 
This call should be executed in an environment where the workflow engine is running and initialized.
[[/note]]


## Example of an RScript

[[code]]
q.logger.log('Executing command: q.hypervisors.manage.virtualbox.pauseMachine(%s)'%params['machineguid'])
q.hypervisors.manage.virtualbox.pauseMachine(params['machineguid'])
q.logger.log('machine %s paused successfully'%params['machineguid'])
params['result'] = True
[[/code]]


## RScript Programming Rules

RScripts should only be used for local changes. They should use the SAL.
There should be:
* No DRP calls
* No starting of other actions.