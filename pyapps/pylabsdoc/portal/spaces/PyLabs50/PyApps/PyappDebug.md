[as]: /pylabsdoc/#/PyLabs50/components


#PyLabs Debugger Support

When you create a PyApp, it is very likely that not everything works as it should be, and in many cases you have to debug your PyApp. In the PyLabs framework this can be easily done, since it contains number of debugging aids.  
The debugging tools are accessible under `q.debugger`.

There are three procedures available: `shell`, `configure`, and `setbreakpoint`.

* shell: launch a Q-Shell session in an interactive environment
* configure: configure a Python debugger, for example pdb or ipython
* setbreakpoint: a breakpoint in your script results in a debug session in the configured debugger


##Launching an Interactive Shell

At any stage in a script (which is executed in an interactive environment), a call to `q.debugger.shell()` will launch a shell, similar to the Q-Shell environment you are used to.

The shell will execute in a *copy* of the namespace in which it is launched. As such, you can not overwrite variables. See the demo session below for an example.

Do note the implementation of `q.debugger.shell` does not (and can not) make sure it is being called in an interactive session. As such, one should always remove calls to `q.debugger.shell()` once the call is no longer required. Otherwise the call could launch a shell in a non-interactive environment, for example when the code is executed inside the Applicationserver or Workflow Engine. This situation can lead to blocked processes.

Here is a sample session:

    $ cat shelldemo.py 
    from pylabs.InitBase import q

    j = 10
    print 'j =', j

    q.debugger.shell()

    print 'j =', j

    $ python shelldemo.py 
    j = 10

    Welcome to qshell

    ?          -> Introduction to features.
    help()     -> python help system.
    object?    -> Details about 'object'.
    object??   -> Extended details about 'object'.

    Type q. and press [TAB] to list qshell library
    Type i. and press [TAB] to list interactive commands



    In [1]: print j
    10

    In [2]: j = 100 

    In [3]: print j
    100

    In [4]: ^D
    Do you really want to exit ([y]/n)? 

    j = 10


##Debugger Configuration
PyLabs supports several Python debuggers, including standard PDB, the IPython enhanced PDB, and RPDB2/WinPDB (when available on the system). The debugger to be used can be configured using `q.debugger.configure()`. A specific debugger
can also be selected by calling `q.debugger.configure('name')`, where *name* should be one of 'pdb', 'ipython', 'winpdb' or 'disabled' (to disable all breakpoint calls).


##Setting Breakpoints

Whenever you want to break into a running script, a call to `q.debugger.setbreakpoint()` launches the configured debugger. 

Similar to calls to `q.debugger.shell()`, this should only be called during interactive execution of the code, unless the 'disabled' debugger is configured, or the 'winpdb' debugger is being used, since the 'winpdb' system is client-server based (and as such suited to debug code running in a non-interactive process).

Here is a demonstration of using the 'IPython' debugger:

    $ cat tasklets/1_demo.py
    __tags__ = 'demo',

    def main(q, i, p, params, tags):
        q.logger.log('Running demo tasklet', 4)

        q.debugger.setbreakpoint()

        clusters = q.manage.arakoon.listClusters()

        q.logger.log('There are %d configured clusters' % len(clusters), 5)


    $ cat debugdemo.py 
    from pylabs.InitBase import q
    q.application.appname = 'debugdemo'

    q.debugger.configure('ipython')

    engine = q.taskletengine.get('tasklets')

    params = {
        'demo1': 1,
        'demo2': 2,
    }

    engine.execute(params, tags=('demo', ))

    $ python debugdemo.py 
    > /home/holygrail/tasklets/1_demo.py(8)main()
          7 
    ----> 8     clusters = q.manage.arakoon.listClusters()
          9 

    ipdb> print params
    {'demo2': 2, 'demo1': 1, 'taskletlastexecutiontime': 0.0}
    ipdb> print q.application.appname
    debugdemo
    ipdb> step
    --Call--
    > /opt/qbase5/lib/pylabs/core/pylabs/extensions/PMExtensionsGroup.py(64)__getattribute__()
         63 
    ---> 64     def __getattribute__(self, name):
         65         """

    ipdb> next

Several calls to 'next' later, once we are outside the PyLabs extension loading mechanism:

    ipdb> 
    --Call--
    > /opt/qbase5/lib/pylabs/extensions/servers/arakoon/ArakoonManagement.py(126)listClusters()
        125 
    --> 126     def listClusters(self):
        127         """

    ipdb> step
    > /opt/qbase5/lib/pylabs/extensions/servers/arakoon/ArakoonManagement.py(130)listClusters()
        129         """
    --> 130         config = q.config.getInifile("arakoonclusters")
        131         return config.getSections()

    ipdb> next
    > /opt/qbase5/lib/pylabs/extensions/servers/arakoon/ArakoonManagement.py(131)listClusters()
        130         config = q.config.getInifile("arakoonclusters")
    --> 131         return config.getSections()
        132 

    ipdb> print config
    <IniFile> filepath: /opt/qbase5/cfg/qconfig/arakoonclusters.cfg 
    ipdb> print config.getSections()
    ['sampleapp']
    ipdb> next
    --Return--
    ['sampleapp']
    > /opt/qbase5/lib/pylabs/extensions/servers/arakoon/ArakoonManagement.py(131)listClusters()
        130         config = q.config.getInifile("arakoonclusters")
    --> 131         return config.getSections()
        132 

    ipdb> 
    > /home/holygrail/tasklets/1_demo.py(10)main()
          8     clusters = q.manage.arakoon.listClusters()
          9 
    ---> 10     q.logger.log('There are %d configured clusters' % len(clusters), 5)

    ipdb> continue


##Debugging the Workflow Engine and Actions Tasklets

In order to debug the workflow engine, you need to start it in debug mode. This can be achieved with:

    q.manage.workflowengine.start(appname, debug=True)   

Where:  

* __appname:__ is the name of your application.   
* __debug:__ specifies whether you want to start the workflow engine in normal (recommended) or in debug mode.   

*Note: If the workflow engine is already running, you need to stop it first.*   

After you start the workflow engine in debug mode, you can open its screen using the command below:
    
    screen -x wfe.appname

Where 'appname' is the name of your application. For example: sampleapp.   
This will open a screen with the following:
    
     0 jobs to reset
    Ready !
    

In that screen you will be able to interactively debug your PyApp on workflow engine level.

If you want to leave the screen session and want the workflow engine to stay running in debug mode, press CTRL+a followed by the `d` key.
However, it is recommended not to run the workflow engine in debug mode for better performance.

To end the debug mode, press CTRL+c in your screen session and restart the workflow engine in the Q-Shell.

    root@mm64:/opt/qbase5# screen -x wfe --> press CTRL+c in your screen session
    [screen is terminating]
    root@mm64:/opt/qbase5#
    
    #in Q-Shell:
    In [2]: q.manage.workflowengine.start('sampleapp')
    Starting the workflowengine.
     Waiting for initialization
    Workflowengine started
    

## Debugging the Application Server

Similar to debugging the workflow engine, you can also debug the [PyLabs Application Server][as]. Therefore run the application server in debug mode:

    q.manage.applicationserver.start(appname, debug=True)
    
Where:  

* __appname:__ is the name of your application.   
* __debug:__ specifies whether you want to start the application server in normal (recommended) or in debug mode.   

*Note: If the workflow engine is already running, you need to stop it first.* 

After you start the application server in debug mode, you can open its screen using the command below:
    
    screen -x applicationserver.appname
    
Replace _appname_ by the name of your PyApp, for example _sampleapp_.

*Tip: enter `screen -ls` to get a list of active screen sessions.*

In that screen you will be able to interactively debug your PyApp on application server level. To return to the normal mode of the application server, see the previous paragraph.
