@metadata title=Testing API
@metadata order=130
@metadata tagstring=test api pyapp

[actions]: #/PylabsApps/Action
[qpinstall]: #/Q-Packages/QPInstall
[appserver]: #/Components/AppServer


# Testing your API

[[warning]]
**Warning**

This page needs complete review and may be inaccurate at this moment. We try to get it up to date as soon as possible.

Our apologies for any inconvenience.
[[/warning]]

This is a small tutorial on how you can start to test your API.

We will use the API created in [Defining Actions Interface on Root Objects][actions] and suppose that they are saved in `/opt/demo_dir/src/api/rootobject`


## Installing the Cloud API Generator

Find and install the latest version of the 'cloud_api_generator' Q-Package.
If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


## Generating the API

If you didn't restart your Q-Shell after installing the Could API Generator, then please do so.

Prior to generating the API, we need to set the directory from which the generator will get the API definitions and disable the generation of actor action libraries. This can be achieved with the command below:

    q.generator.cloudapi.specDir = /opt/demo_dir/src/api/rootobject/e

[[note]]
**Note** 

You need to reconfigure this everytime you restart your Q-Shell.
[[/note]]

Now we can start generating the API:

    q.generator.cloudapi.generatePythonRoot()

Exit the Q-Shell and a lot new directories will appear in `/opt/qbase5/apps/cloud_api_generator`
The most important are generatedClient and generatedServer.


## Installing the Application Server and Workflow Engine

Find and install the latest versions of the Q-Packages named 'applicationserver' and 'workflowengine'.

[[note]]
**Note** 

When you restart the Q-Shell after installing the application server, you will be asked to configure it. Details of this configuration can be found on the [Application Server][[appserver] page. Also if you would like more details on the workflow engine, you can check the [Workflow Engine] page.
[[/note]]

Restart the shell after the configuration.

[[warning]]
**Warning**

Because we have no agent configured and we are not going to use the storage backend we will get some errors during reconfiguration.
Just answer with 1 (Skip this one) on the first question (no agent config) then enter the default values for the configuration questions that you will be asked.

    What do you want to do?
        1: Skip this one
        2: Go to shell
        Select Nr (1-2):

    Please enter the address of the applicationserver running the OSIS service [http://127.0.0.1:8888]: 
    Please enter the name of the osis service [osis_service]: 
    Please enter the FQDN of the XMPP server [dmachine.sso.daas.com]: 
    Please enter the agentcontrollerguid [agentcontroller]: 
    Please enter the workflowengine port [9876]: 
    Please enter the workflowengine password [****]: 
    Please enter the workflowengine password [****]:  (confirm): 
[[/warning]]


## Copying the Files in the Correct Directories

From now on everything is installed.
We should only put the generated code in the right location and start creating root object tasklets.

* The applicationservice:

    mkdir /opt/qbase5/apps/applicationserver/services/cloud_api
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/example.py /opt/qbase5/apps/applicationserver/services/cloud_api/.
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/BaseCloudAPI.py /opt/qbase5/apps/applicationserver/services/cloud_api/.
    touch /opt/qbase5/apps/applicationserver/services/cloud_api/__init__.py
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/applicationserverservice.cfg /opt/qbase5/cfg/qconfig/. #Do this step only when you have no other services!
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/cloud_api_rootobjects /opt/qbase5/lib/python/site-packages/.
    touch /opt/qbase5/lib/python/site-packages/cloud_api_rootobjects/__init__.py
    mkdir /opt/qbase5/lib/pymonkey/extensions/example_api
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/extensions/* /opt/qbase5/lib/pymonkey/extensions/example_api/.

* Some extra helper libraries:

    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/cloud_api_rootobjects /opt/qbase5/lib/python/site-packages/.
    touch /opt/qbase5/lib/python/site-packages/cloud_api_rootobjects/__init__.py
    mkdir /opt/qbase5/lib/pymonkey/extensions/example_api
    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/extensions/* /opt/qbase5/lib/pymonkey/extensions/example_api/.

* Some 'default' generated tasklets for the workflowengine:

    cp -rf /opt/qbase5/apps/cloud_api_generator/generatedServer/tasklets/example /opt/qbase5/apps/workflowengine/tasklets/rootobject/.
    touch /opt/qbase5/apps/workflowengine/tasklets/rootobject/tasklets_updated

* Installing the client:

    mkdir /opt/qbase5/lib/pymonkey/extensions/cloud_api_client
    cp /opt/qbase5/apps/cloud_api_generator/generatedClient/* /opt/qbase5/lib/pymonkey/extensions/cloud_api_client/.
    touch /opt/qbase5/lib/pymonkey/extensions/cloud_api_client/__init__.py

* Finally configure the client:

Here we add a cloud API connection named 'main'.
[[note]]
**Note** 

Choose 'admin' for customer login and customer password.
[[/note]]

    In [1]: i.config.cloudApiConnection.add('main')                                  
     Enter (IP) address of the Application Server [127.0.0.1]: 
    Enter port of the Application Server [80]: 8888
    Enter URL path of the XML-RPC transport of the Application Server [/appserver/xmlrpc/]: /RPC2                       
    Enter customer login (optional): admin 
    Enter customer password (optional): 
    Enter customer password (optional) (confirm): 


## Testing the Client

    In [1]: conn.example.create('main')
    Out[1]: {'jobguid': None, 'result': ''}

What happens here, is that the machine_create tasklet is executed, but as you can see, it does not contain much information and the 'result' field is empty.
As an example, let's try and change the 'result' field to display the name.

To change this we will need to change the 'example_create' tasklet in: /opt/qbase5/apps/workflowengine/tasklets/rootobject/example/

    vi /opt/qbase5/apps/workflowengine/tasklets/rootobject/example/create/example_create.py

Modify the 'main' function to return the 'name' in the 'result' as below:

[[code]]
__author__ = 'aserver'
__author__ = 'aserver'
__tags__ = 'example', 'create'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = params['name']

def match(q, i, params, tags):
    return True
[[/code]]

After changing:

    touch /opt/qbase5/apps/workflowengine/tasklets/rootobject/tasklets_updated

Get the cloud API connection you created before:

    conn = i.config.cloudApiConnection.find('main') 

Now you can test again and see that the result field takes the name:

    In [1]: conn.example.create('main')
    Out[1]: {'jobguid': None, 'result': 'main'}

    In [1]: conn.example.create('bla')
    Out[1] {'jobguid': None, 'result': 'bla'}
