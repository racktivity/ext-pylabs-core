@metadata title=Creating an Extension
@metadata order=10
@metadata tagstring=extension test create

#Creating and Testing an Extension

In this section we show you step by step how you can create a Pylabs extension. A simple Hello World application is used as example.


##1. Creating the Extension Files
A first step to create a Pylabs extension is to create the extension files.

1. Go to `/opt/qbase5/lib/pylabs/extensions` and create a directory in it, for example `demo`.
2. Create the file `extension.cfg` and add the following content:
    
    [hook1]
    qlocation=q.demoExtension.demoHelloWorld
    modulename=DemoHelloWorld
    classname=ClassHelloWorld
    enabled=1

3. Create the file `DemoHelloWorld.py` and add this code to it:

[[code]]
from pylabs import q

class ClassHelloWorld:
    '''HelloWorld class for demonstration purposes'''
    
    def do(self):
        '''Say Hello World'''
        q.gui.dialog.message('Hello World!')
[[/code]]


##2. Testing the Extension

Open a Q-Shell session and type `q.` + TAB.

    In [1]: q.
    q.action                 q.cmdtools               q.doctools               q.init_final(            q.qshellconfig
    q.agentid                q.codetools              q.enumerators            q.logger                 q.remote
    q.application            q.config                 q.errorconditionhandler  q.manage                 q.system
    q.base                   q.console                q.eventhandler           q.messagehandler         q.tasklet
    q.basetype               q.db                     q.extensions             q.platform               q.taskletengine
    q.clients                q.debugger               q.flexui                 q.pylabs                 q.tools
    q.cloud                  q.debugging              q.generator              q.pymodel                q.transaction
    q.cluster            ==> q.demoExtension <==      q.gui                    q.qp                     q.vars
    q.cmdb                   q.dirs                   q.init(                  q.qpackagetools          q.workflowengine
    
Select `demoExtension` and drill down to `demoHelloWorld`:

[[code]]
    In [1]: q.demoExtension.demoHelloWorld
[[/code]]
    
This is the `qlocation` from the extension file. From this location you can access all methods that you defined in your class, in this example there is only the `do` method.

[[code]]
    In [1]: q.demoExtension.demoHelloWorld.do(?
    Definition: q.demoExtension.demoHelloWorld.do(self)
    Documentation:
        Say Hello World
    
    
    In [2]: q.demoExtension.demoHelloWorld.do(??
    Definition: q.demoExtension.demoHelloWorld.do(self)
    Source:
        def do(self):
            '''Say Hello World'''
            q.gui.dialog.message('Hello World!')
    
    In [3]: q.demoExtension.demoHelloWorld.do()
     Hello World!
[[/code]]
     

##Multi-Hook

To hook multiple classes on the `q.` object in one extension, add the hook definitions in the configuration file, optionally you can create a module per hook.

Updated `extension.cfg`:

    [hook1]
    qlocation=q.demoExtension.demoHelloWorld
    modulename=DemoHelloWorld
    classname=ClassHelloWorld
    enabled=1
    
    [hook2]
    qlocation=q.demo.helloworld
    modulename=Hook2HelloWorld
    classname=ClassHelloWorld
    enabled=1
     
    [hook3]
    qlocation=q.hello.hook3
    modulename=Hook3HelloWorld
    classname=ClassHelloWorld
    enabled=1

Copy `DemoHelloWorld.py` to `Hook2HelloWorld.py` and `Hook3HelloWorld.py` and update the new files as shown below:

Hook2HelloWorld.py:

[[code]]
from pylabs import q

class ClassHelloWorld:
    '''HelloWorld class for demonstration purposes'''
    
    def do(self):
        '''Say Hello World from Hook 2'''
        q.gui.dialog.message('Hello World from Hook 2!')
[[/code]]

Hook3HelloWorld.py:

[[code]]
from pylabs import q

class ClassHelloWorld:
    '''HelloWorld class for demonstration purposes'''
    
    def do(self):
        '''Say Hello World from Hook 3'''
        q.gui.dialog.message('Hello World from Hook 3!')
[[/code]]


##Testing Multi-Hook

Open or restart the Q-Shell and check the `do` functions:

[[code]]
In [1]: q.demo.helloworld.do()
 Hello World from Hook 2!
 
In [2]: q.hello.hook3.do()
 Hello World from Hook3!
[[/code]]