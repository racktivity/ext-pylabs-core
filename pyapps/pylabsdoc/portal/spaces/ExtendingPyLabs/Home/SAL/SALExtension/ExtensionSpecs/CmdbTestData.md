@metadata title=CMDB Test Data
@metadata order=50
@metadata tagstring=cmdb test data

[extspec]: #/ExtendingPylabs/ExtensionSpecs
[qshelloption]: #/Q-Shell/QShellOptions


# CMDB Test Data

Test data, or in other words, fake data, is data that you add in the [specifications of a CMDB object][extspec]. This is mainly random data or data that you invent yourself. When you activate the fake data, it is as if the fake data is stored in the CMDB. It allows the developers to use the defined methods of an application without having written any code, but they get to know how to use the methods and what they should return.


## Activating the Fake Data

Start the Q-Shell and use the command below:

    q.vars.setVar('fakeData', True)

You can also activate the fake data per application or service. To do this, start the Q-Shell in [debug mode][qshelloption] and run the command below:

    q.manage.<name of application>.cmdb.__fake_data__()

Let's try it with the 'portforwarder' application:

    q.manage.portforwarder.cmdb.__fake_data__()

Using the fake data:

* Get the list of portforwarding rules:

    In [1]: q.manage.portforwarder.cmdb.forwards
    Out[1]: 
    {'Forward-13': <PortForward.PortForward object at 0x89b6b2c>,
     'Forward-16': <PortForward.PortForward object at 0x89b602c>,
     'Forward-59': <PortForward.PortForward object at 0x89b40cc>,
     'Forward-60': <PortForward.PortForward object at 0x89b62cc>,
     'Forward-70': <PortForward.PortForward object at 0x89b6c0c>,
     'Forward-75': <PortForward.PortForward object at 0x89b614c>,
     'Forward-79': <PortForward.PortForward object at 0x89b616c>,
     'Forward-92': <PortForward.PortForward object at 0x89b6bcc>,
     'Forward-96': <PortForward.PortForward object at 0x89b61ec>,
     'Forward-97': <PortForward.PortForward object at 0x89b4a8c>,
     'Rule 1': <PortForward.PortForward object at 0x87f2d4c>,
     'newRule': <PortForward.PortForward object at 0x89c656c>}

* Select forward rule 97 (Forward-97):

    forward = q.manage.portforwarder.cmdb.forwards['Forward-97']

* View details for the selected rule:

    In [1]: forward.remoteHost
    Out[1]: '10.100.0.48'

    In [1]: forward.remotePort 
    Out[1]: 57240

    In [1]: forward.localPort
    Out[1]: 470
