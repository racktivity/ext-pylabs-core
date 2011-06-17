@metadata title=Debug Scripts
@metadata tagstring=debug script pdb shell breakpoint

#How to Debug PyLabs Scripts

When creating PyLabs scripts, it is possible that you need to debug some errors. In that case you have two options:

* via the Q-Shell: open a Q-Shell via your script, all data used/created via your script is then available in the Q-Shell
* via debug breakpoints: set breakpoints in your script to start an interactive debugger


##Q-Shell Debug

Let's take this example script. The script is completely functional, but it is used to show its behavior. To start an interactive Q-Shell session, add `q.debbuger.shell()` anywhere in your script.

[[note]]
**Note**
Do not forget to remove this line when your script is completely debugged.
[[/note]]

[[code]]
from pylabs.InitBase import *

q.qshellconfig.interactive = True

age = q.gui.dialog.askInteger('Your age')

q.gui.dialog.message('You are %d years old'%age)

q.debugger.shell()

q.gui.dialog.message('This message is shown after quitting Q-Shell')
[[/code]]

Execute the script with the Q-Shell:

    $ /opt/qbase5# ./qshell -f script.py 
    Your age: 36
     You are 36 years old
    
    Welcome to qshell
    
    ?          -> Introduction to features.
    help()     -> python help system.
    object?    -> Details about 'object'.
    object??   -> Extended details about 'object'.
    
    Type q. and press [TAB] to list qshell library
    Type i. and press [TAB] to list interactive commands
    
    
    
    In [1]: age
    Out[1]: 36
    
    In [2]: age = 63

    In [3]: print age
    63
    
    In [4]: <CTRL-D>
    Do you really want to exit ([y]/n)? 
     This message is shown after quitting Q-Shell
    $ 
        
You notice that the variable `age` is available in the Q-Shell. This allows you to continue in your script with all data to debug your script.
When leaving the Q-Shell, your script continues.


##Debug Breakpoints
PyLabs supports several Python debuggers, including standard PDB, the IPython enhanced PDB, and RPDB2/WinPDB (when available on the system). The debugger to be used can be configured using `q.debugger.configure()`. A specific debugger
can also be selected by calling `q.debugger.configure('name')`, where *name* should be one of 'pdb', 'ipython', 'winpdb' or 'disabled' (to disable all breakpoint calls).

Whenever you want to break into a running script, a call to `q.debugger.setbreakpoint()` launches the configured debugger. 

Similar to calls to `q.debugger.shell()`, this should only be called during interactive execution of the code, unless the 'disabled' debugger is configured, or the 'winpdb' debugger is being used, since the 'winpdb' system is client-server based (and as such suited to debug code running in a non-interactive process).

Here is a demonstration of using the 'IPython' debugger, using the above example again:

[[code]]
from pylabs.InitBase import *

q.qshellconfig.interactive = True
q.debugger.configure('ipython')

age = q.gui.dialog.askInteger('Your age')

q.debugger.setbreakpoint()

q.gui.dialog.message('You are %d years old'%age)
[[/code]]

Below you can see the behavior:

    $ ./qshell -f script.py 
    Your age: 35 
    > /opt/qbase5/script.py(10)<module>()
          8 q.debugger.setbreakpoint()
          9 
    ---> 10 q.gui.dialog.message('You are %d years old'%age)
    
    ipdb> print age
    35
    ipdb> continue
     You are 35 years old
    $
    
Use the command `next` to go to the next line that will be executed, helpful in case of decision trees.
Use the command `continue` to continue with the script.    