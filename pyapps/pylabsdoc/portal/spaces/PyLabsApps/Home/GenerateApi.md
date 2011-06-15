[appserver]: /pylabsdoc/#/Components/AppServer
[wfe]: /pylabsdoc/#/Components/WFE

# Generating an API

[[warning]]
**Warning**
This page needs complete review and may be inaccurate at this moment. We try to get it up to date as soon as possible.

Our apologies for any inconvenience.
[[/warning]]

When the API is defined we use a generator to generate the cloud API service.
The generator generates client and server files.

* *Client:* Extension and Pylabs API client.
* *Server:* Application server services, library to glue the service with the workflow engine, default workflow engine tasklets and management extensions.

Typically it calls the workflow engine to get the requested changes or to apply the changes.


##Generating

Define where your cloud API root object definitions can be found:

    q.generator.cloudapi.specDir = $api_dir

Generate the root object action:

    q.generator.cloudapi.generatePythonRoot()

This generates a directory structure in:

* `/opt/qbase5/cloud_api_generator/`

The directory contains two main subdirectories:

* *generatedServer*: Files to create the cloud API server, it contains the classes to create the service and the supported library which uses the workflow engine.
* *generatedClient:* PyLabs client to call the generated cloud API server.


##Creating the Cloud API service Package

The generated API should be located as a service in the application server.
So the main files will be located in `/opt/qbase5/apps/applicationserver/services`
Also a library is created during the generator step, this should be located in `/opt/qbase5/lib/python/site-packages/`

Typically those are the actions which should be performed on the node which will host the API:

* Install [Application Server][appserver]
* Install [Workflow Engine][wfe]


### Copying the Files in the Correct Directories

* The application service:

    mkdir /opt/qbase5/apps/applicationserver/services/cloud_api
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/*.py /opt/qbase5/apps/applicationserver/services/cloud_api/.
    touch /opt/qbase5/apps/applicationserver/services/cloud_api/__init__.py
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/applicationserverservice.cfg /opt/qbase5/cfg/qconfig/. #Do this step only when you have no other services!

* Some extra helper libraries:

    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/cloud_api_rootobjects /opt/qbase5/lib/python/site-packages/.
    touch /opt/qbase5/lib/python/site-packages/cloud_api_rootobjects/__init__.py
    mkdir /opt/qbase5/lib/pymonkey/extensions/$api_name_api
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/extensions/* /opt/qbase5/lib/pymonkey/extensions/$api_name_api/.

* Some default generated tasklets for the workflow engine:

    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/tasklets/example /opt/qbase5/apps/workflowengine/tasklets/rootobject/.
    touch /opt/qbase5/apps/workflowengine/tasklets/rootobject/tasklets_updated

* Installing the client:

    mkdir /opt/qbase5/lib/pymonkey/extensions/cloud_api_client
    cp /opt/qbase5/apps/cloud_api_generator/generatedClient/* /opt/qbase5/lib/pymonkey/extensions/cloud_api_client/.
    touch /opt/qbase5/lib/pymonkey/extensions/cloud_api_client/__init__.py

* Configuring the client:

[[note]]
**Note** 
Choose 'admin' as your login and password.
[[/note]]

    In [1]: i.config.cloudApiConnection.add('main')
     Enter (IP) address of the Application Server [127.0.0.1]: 
    Enter port of the Application Server [80]: 8888
    Enter URL path of the XML-RPC transport of the Application Server [/appserver/xmlrpc/]: /RPC2
    Enter customer login (optional): admin
    Enter customer password (optional): 
    Enter customer password (optional) (confirm): 
    