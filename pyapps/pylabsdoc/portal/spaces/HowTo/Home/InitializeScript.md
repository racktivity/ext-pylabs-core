@metadata title=Initialize Pylabs Scripts
@metadata tagstring=initialize script import custom

[imgInit1]: images/images51/howto/GettingStarted017.png
[imgInit2]: images/images51/howto/GettingStarted018.png


# How to Initialize Pylabs Scripts

Q-Shell scripts are scripts using Pylabs code.

This doc shows you how you can perform a custom Pylabs initialization.

## Example Initialization of Pylabs

Applications using the Pylabs framework are themselves responsible for the initialization of the Pylabs framework. 
There are several initialization methods which be can optionally called before using the Pylabs object called `q`.
In this example we will _not_ perform a custom initialization.

[[code]]
#in all apps use next line to initialize Pylabs, as a result the q global var will be available.
from pylabs.InitBase import *

# at this point your initialization has been done. You still need to set an application name and start the application

q.application.appname = "yourApplicationName"
q.application.start()

# your code here 
q.gui.dialog.message("HelloWorld")

#next line is only needed if you want to execute the qshellStart
from pylabs.Shell import *
ipshell()

q.application.stop(exitcode)
[[/code]]

![defaultInit][imgInit1]


## Custom Initialization Script

Out of the box any script (application) like above does not need a custom initialization. However, you can also create your own initialization routines.

Convention:
Create an `init_<yourapplicationName>.py` file and put in same directory as your application.


### `init_testapp.py`
[[code]]
from pylabs.inifile import IniFile
from pylabs.Vars import Vars
from pylabs.log.LogTargets import LogTargetStdOut, LogTargetFileSystem, LogTargetServer, LogTargetDevNull
from pylabs import q

#set your own directory paths (in example below is same as default init script)
q.dirs.varDir = os.path.join(q.dirs.baseDir, 'var', '')
q.dirs.cfgDir = os.path.join(q.dirs.appDir, 'mycfg', '')
q.dirs.tmpDir = os.path.join(q.dirs.varDir, 'tmp', '')
q.dirs.pidDir = os.path.join(q.dirs.varDir, 'pid', '')
q.dirs.logDir = os.path.join(q.dirs.varDir, 'log', '')
q.dirs.pmdbDir = os.path.join(q.dirs.varDir, 'pmdb', '')
q.dirs.init()

#create new loggers
#remove loggers potentially set before in default initialization
q.logger.resetLogTargets()

maincfg = IniFile(q.dirs.cfgDir+"main.cfg")
lts = LogTargetServer(maincfg.getValue("logging","logserver"), int(maincfg.getValue("logging","logserverport")), int(maincfg.getValue("logging","loglevel")))
q.logger.addLogTarget(lts)

#initialize global vars
#next will fail if there is no section "testsection" with a var called varname
q.vars.setVar("aGlobalVar", maincfg.getValue("testsection","varname"))

q.vars.setVar("testGlobalVar","hello")

q.logger.log("Custom Initialization finished.")
[[/code]]


### `testAppCustomInitialization.py`

[[code]]
#in all apps use next line to initialize pylabs, as a result the q global var will be available.
from pylabs.InitBase import *

from pylabs.Shell import *

#custom initializations script
#DO NOT PUT INITIALIZATION OR CONFIGURATION MANAGEMENT CODE IN APPLICATION CODE!
from init_testapp import *

q.application.appname = "yourApplicationName"
q.application.start()

# your code here 
q.gui.dialog.message("HelloWorld")

#for now open a qshell
#next line is only needed if you want to execute the qshellStart
from pylabs.Shell import *
ipshell()

q.application.stop(exitcode)
[[/code]]

![customInit][imgInit2]


##Remark

The Pylabs singleton is exposed in the main Pylabs package, so any module using it (applications, utility modules, libraries,..) should import it using: 

    from pylabs import q