##PyLabs as Scripting Platform

PyLabs can be used as scripting platform. In these scripts you can use the full potential of the PyLabs framework, like interactivity with the user, manage the hardware, ...
When you have created your script, it is possible to integrate it in Q-Shell (as an extension). This gives you the possibility to integrate your script in other scripts or in applications.


###Writing Your First Script
To create a PyLabs compatible script, you have to import PyLabs InitBase. This makes sure that all default and custom (i.e. self-made) PyLabs extensions are loaded into memory.
When done you have the same functionalities as in the Q-Shell.

[[code]]
from pylabs.InitBase import *

q.application.appname = 'myfirstscript'
q.application.start()

q.gui.dialog.message('Hello World!')

q.application.stop()
[[/code]]

Save the above code in a `.py` file and execute it with Q-Shell:

    $ ./qshell -f hello.py
       Hello World!
    $

When you see 'Hello World!' appear, you have successfully created your first PyLabs script.

Next in this chapter you will learn to use the power of PyLabs in your script and make a PyLabs extension of your script.
