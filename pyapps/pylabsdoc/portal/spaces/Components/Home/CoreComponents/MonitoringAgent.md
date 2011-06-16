@metadata title=Monitoring Agent
@metadata tagstring=monitor agent cloud

[qpinstall]: /#/Q-Packages/QPInstall


# Monitoring Agent

The monitoring agent is a python application that contains a scheduler. This scheduler is responsible for starting tasklets which gather monitor information at fixed moments. The monitor information is saved in the DRP model.

##Installing the Monitoring Agent

Install the latest version of the Q-Package named 'cloud_monitoring_agent'.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.

[[note]]
**Note** 
When you restart your Q-Shell, you will be asked to configure the Clould API Connection, followed by the Monitoring Agent.
[[/note]]


## Location in the Sandbox

* *Monitoring agent service:* `/opt/qbase5/apps/monitor_agent/`
* *Monitoring management extension:* `/opt/qbase5/lib/pymonkey/extensions/monitor_agent`
* *Monitoring model:* `/opt/qbase5/lib/python/site-packages`


## Managing the Monitoring Agent

* To start the monitoring agent:

    q.manage.monitoringagent.start()

* To stop the monitoring agent:

    q.manage.monitoringagent.stop()

* To restart the monitoring agent:

    q.manage.monitoringagent.restart()

* To get the status of the monitoring agent:

    q.manage.monitoringagent.getStatus()

* To kill the monitoring agent:

    q.manage.monitoringagent.kill()


## Configuring the Monitoring Agent

The monitoring agent needs a monitor server to change the internal monitor object model.

Initially, you configure this once you restart your Q-Shell, but if you need to re-configure it later on, or if you have not restarted your Q-Shell, use the following command:

    i.config.monAgentOSIS.review()                                         


## Creating Monitoring Agent Tasklets

The tasklets have a basic structure and contain a match and a main function.

The match function is mainly used to check if the time between two executions is big enough, and the main function contains code to raise warnings or to populate the monitor mode.


## Examples

@todo: add examples


## Code Repositories

The source code can be found on the following BitBucket code repository:
    
    http://bitbucket.org/despiegk/monitoring_agent
    