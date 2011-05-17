﻿## Getting Familiar with the Q-Shell

### Starting the Q-Shell
When you have installed PyLabs, go to the folder `/opt/qbase5`.

Enter the following command to launch the Q-Shell: `./qshell`

![Q-Shell window](images/images50/qshell/Q-Shell_01.png)


### Name Spaces

The Q-Shell has three main name spaces:

* **q.**: the main name space of PyLabs, used for automation scripts, configuring PyLabs extensions, ...
* **i.**: interactive name space, functions in this name space require user input
* **p.*: the name space to manage PyLabs applications


### Using the Q-Shell

Throughout the complete Q-Shell you can use TAB-completion for minimizing the time in entering commands and avoiding to enter erroneous commands.

Type `q.` and press TAB and you see the list of name spaces of the `q` name space.

![q Name Space](images/images50/qshell/Q-Shell_02.png)

Now add `gu` + TAB to enter the `gui` name space. Press '.d' + TAB to go into the `dialog` section, followed by '.m' + TAB to call the `message` function.
Add a string message, close with a bracket, and press ENTER.

![Show message](images/images50/qshell/Q-Shell_03.png)

If you need help with a function, you can call the help-function by appending `?` to `q.qui.dialog.message(` and, then press ENTER.

![Help function](images/images50/qshell/Q-Shell_04.png)

You can even open the source code of the function by adding a double question mark behind the function.

![Help function source](images/images50/qshell/Q-Shell_05.png)
