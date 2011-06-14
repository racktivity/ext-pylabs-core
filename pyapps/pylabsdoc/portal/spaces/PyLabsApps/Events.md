[downloadevent]: http://bitbucket.org/despiegk/sso_openerp/
[tour]: http://doc.openerp.com/book/1/1_2_Guided_Tour/1_2_Guided_Tour_install_functionality.html
[SSOEvents]: http://confluence.aserver.com/display/SSODOCINT/SSO+Event+List
[imgExportEventTypes]: images/images50/pyapps/ExportEventTypes.png
[imgExport]: images/images50/pyapps/Export.png
[imgSaveAs: images/images50/pyapps/SaveAs.png


# PyLabs Events

[[warning]]
**Warning**
This page needs complete revision and may be inaccurate at this moment. We try to get it up to date as soon as possible.

Our apologies for any inconvenience.
[[/warning]]

## Introduction

The goal of this document is to describe how the PyLabs event handler works, as well as list the default event processing tasklets.

## Event Types Database

The event types database is implemented as an OpenERP module. The module consists of two object types, Components and Event Types. A description of both is given below.

*Components:*

Components allow you to group a number of events. They have the following properties:

* Name: a free text field describing the component.
* Code: used as the prefix for related events.
* Author: identifies the owner of a component.

*Event Types:*

An event type, is a definition of an event with its properties. It has the following properties:

* Component: a link to the related component.
* Event type id: unique identifier for an event. Consists of a prefix which is related component.code + an auto-incremental number e.g. SSO-MON-PMACHINE-0001
* Tags / Labels: PyLabs tags / labels format.
* Description: a description of the event specified.
* Solution: possible solution when event occurs.
* Severity overrule: with this value you can overrule the severity specified when the event was raised.
* Dedupe period in minutes: a value which specifies how frequent the same event should be processed. Sequential, similar events are dropped.
* Active: a boolean flag identifying if the event is still active.
* Forward to NOC: a boolean flag identifying if events of this types should be forwarded to the NOC.
* Store in DRP: a boolean flag identifying if the event should be stored in the DRP.
* Remove tracing: a boolean flag identifying if the tracing should be removed from the event before further processing.
* Remove logging: a boolean flag identifying if the logging should be removed from the event before further processing.


### Installing the OpenERP Module

[Download the events module][downloadevent] and install it on your OpenERP server.
Kindly check the [guided tour][tour] if you need any assistance with installing an OpenERP module.


### How To Export Event Types

The OpenERP module allows you to export all event types as a ".tar" file containing the definition of all event types. You can do this by following these 3 simple steps:


Step 1: In the menu, in the toolbar section, choose SSO and click on *Export Event Types*.

![ExportEventTypes.png][imgExportEventTypes]

Step 2: Click on *Export*.

![Export][imgExport]

Step 3: Click on *Save As* and save the file to your local file system.

![SaveAs][imgSaveAs]

### Where to Place Exported Event Types in the Sandbox

Untar the exported event types to the following location inside your PyLabs sandbox:

    /opt/qbase5/cfg/evt_type_def/

The tar contains a file for every event type definition. The file name is equal to the ID of that event type.

[[info]]
**Example Event Type Definition**

    {
        "categorization": "machineguid, typeid",
        "forwardtonoc": true,
        "description": "Physical machine is down",
        "storeindrp": true,
        "component_id.id": 8,
        "removetracing": true,
        "solution": "Validate why the physical machine is down / powered off",
        "dedupeperiod": 5,
        "removelogging": true,
        "active": true,
        "priorityoverrule": "3"
    }
[[/info]]


## PyLabs Event Handler


### How to Raise Events

Wherever you want to raise an event in your PyLabs application, you can use one of the following raise methods, according to the desired severity level:

* q.errorconditionhandler.raiseCritical(...)
* q.errorconditionhandler.raiseError(...)
* q.errorconditionhandler.raiseInfo(...)
* q.errorconditionhandler.raiseUrgent(...)
* q.errorconditionhandler.raiseWarning(...)

**Example on raising a critical event**

    q.errorconditionhandler.raiseCritical(message='Physical machine "CPUNODE02" is down\!', typeid='SSO-MON-GENERIC-0001')


### How Events are Processed

The default implementation of the event handler uses the follow logic to process events. Since it's based on the tasklet framework, anyone can modify the event processing sequence by modifying the corresponding tasklets, or by adding custom tasklets.

When the event handler receives a certain event, it first checks if the event is a predefined event, in other words, it checks if there is a file in the directory `/opt/qbase5/cfg/evt_type_def/` with `name = event id`. If that is the case, the event manager parses that content of the event definition, adds the different fields as parameters to the tasklet engine parameters dictionary, and then sets the active property of the error condition object according to the value in the error definition.

### List of Default Event Processing Tasklets

The list is sorted with higher priority tasks first.

#### Remove Tracing/Logging (Priority 10)

*Matches when:*

* errorcondition.active = True
AND

    ** Event definition indicates that tracing should be removed.
       OR
       Event definition indicates that logging should be removed.

*Executes:*

* Removes logging and/or tracing from the error condition object.


####Remove Q-Shell Errors (Priority 10)

*Matches when:*

* errorcondition.active = True
AND
q.qshellconfig.interactive = True


*Executes:*

* errorcondition.active = False


####Severity Overrule (Priority 9)

*Matches when:*

* errorcondition.active = True
AND
Event definition contains an overruling severity.

*Executes:*

* Updates severity on error condition object.


####Dedupe (Priority 8)

*Matches when:*
* errorcondition.active = True
AND
Event definition has a value for dedupeinminutes different from 0.

* No other event from same source and type occurred in the period between now and dedupeinminutes ago.

*Executes:*

* errorcondition.active = False


####Forward to NOC (Priority 1)

*Matches when:*
* errorcondition.active = True
AND
q.qshellconfig.interactive = True

* Event definition indicates that event should be forwarded to NOC.

*Executes:*

* Call CloudAPI sso.sendMessageToNoc(...)


####Store in DRP (Priority 1)

*Matches when:*
* errorcondition.active = True
AND
Event definition indicates that event should be stored in DRP.

*Executes:*

* Call CloudAPI errorcondition.create(...)


####Send SNMPTrap (Priority 1)

*Matches when:*

eventid = 'SSO-MON-PMACHINE-0001'

*Executes:*

* Call CloudAPI sso.sendSNMPTrap(...)

The following are the parameters of sendSNMPTrap:

    sendSNMPTrap(self, message, hostdestination='127.0.0.1', port=162, community='aserver', jobguid='', executionparams={})

This event is raised during the monitoring tasklet, "pmachine_monrule_disk_used.py", when the physical disk is almost full.

**Example on raising an event to send a SNMP Trap from Q-Shell**

Step 1:
Start the snmptrapd (daemon server) from qshell with the following command:

    q.manage.snmptrapd.start()

Step 2:
Once the daemon server is running, type in the following command with a message of your choice:

    q.errorconditionhandler.raiseWarning('Physical disk exceeded size limit', typeid='SSO-MON-PMACHINE-0001', escalate=True)

Step 3:
The SNMP Trap can be found in the directory path below, inside the last created log file:

    /opt/qbase5/var/log/pylabslogs/snmptrapd/


**Example of a sent SNMP Trap**

    1 snmptrapd 13:30:27: Trap Notification, SNMP Engine "O", Context ""
    1 snmptrapd 13:30:27: 1.3.6.1.2.1.1.3 = 1284471027
    1 snmptrapd 13:30:27: 1.3.6.1.6.3.1.1.4.1.0 = 1.3.6.1.6.3.1.1.5.1
    1 snmptrapd 13:30:27: 1.3.6.1.6.3.1.1.4.3.0 = 1.3.6.1.6.3.1.1.5
    1 snmptrapd 13:30:27: 1.3.6.1.6.3.18.1.3.0 = 127.0.0.1
    1 snmptrapd 13:30:27: 1.3.6.1.2.1.1.5 = Physical disk exceeded size limit


####Send E-mails on Failed Jobs (Priority 1)

*Matches when:*

* A job fails
AND
eventid = 'SSO-MON-GENERIC-0004'

*Executes:*

* Call CloudAPI sso.sendMail(subject, body, sender='noreply@aserver.com')


## SSO Event List

For futher information about SSO Events, please check the [SSO Event List][SSOEvents] page.