##Simple Configuration

Configuring applications which have simple configurations, which is plain key/value pairs, is very easy and goes in an interactive way.


###Creating a New Configuration

To create a new configuration, call the `add` method without any parameter. As example we take a Mercurial configuration:

[[code]]
In [1]: i.config.clients.mercurial.add()
Please enter a name for the MERCURIAL Connection: my_mercurial_connection
 Enter base URL of repository e.g. http://bitbucket.org/despiegk/my_mercurial_conection: https://bitbucket.org/incubaid/pylabs-core
Username for mercurial connection: your_username_here
Password for mercurial connection: your_password_here
Password for mercurial connection (confirm): your_password_here
Destination folder to clone repository [/opt/qbase5/var/var/mercurial/pylabs-core]: 


In [2]:
[[/code]]


###Updating a Configuration
If you want to change parameters of a configuration, use the `review` function. If there are more than one configurations available, a list is first shown. If only one configuration is available, the review starts immediately.
The default values of each parameter is shown between square brackets. If such a value is not to be updated, just press ENTER, otherwise enter a new value.

[[code]]
In [2]: i.config.clients.mercurial.review()
 Please select a MERCURIAL Connection
    1: my_mercurial_connection
    2: pylabsCore
    3: lfw
    Select Nr (1-3): 1
 Enter base URL of repository e.g. http://bitbucket.org/despiegk/my_mercurial_conection [https://bitbucket.org/incubaid/pylabs-core]: 
Username for mercurial connection [incubaid]: your_username_here
Password for mercurial connection [********]: new_password_here
Password for mercurial connection [********]:  (confirm): new_password_here
Destination folder to clone repository [/opt/qbase5/var/var/mercurial/pylabs-core] [/opt/qbase5/var/var/mercurial/pylabs-core]: 


In [60]:
[[/code]]



###Alternative Way to Update a Configuration
If you need to configure an application via a script, you can not use the interactive way, but you can use the `configure` method.
This method takes two parameters:

* a configuration name
* a dictionary of parameters

[[code]]
i.config.clients.mercurial.configure('my_mercurial_connection', {'login':'my_new_login', 'passwd': 'my_new_password'}
[[/code]]


###Removing a Configuration
If a configuration has become obsolete, you can remove it easily. 

[[code]]
In [74]: i.config.clients.mercurial.remove()
 Please select a MERCURIAL Connection
    1: my_mercurial_connection
    2: pylabsCore
    Select Nr (1-2): 1
    
In [75]: i.config.clients.mercurial.list()
Out[75]: ['pylabsCore']
[[/code]]
