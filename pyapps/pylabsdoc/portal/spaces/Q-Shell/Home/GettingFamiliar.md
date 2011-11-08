@metadata title=Getting Familiar
@metadata order=10
@metadata tagstring=getting familiar

[imgQshell1]: images/images51/qshell/Q-Shell_01.png
[imgQshell2]: images/images51/qshell/Q-Shell_02.png
[imgQshell3]: images/images51/qshell/Q-Shell_03.png
[imgQshell4]: images/images51/qshell/Q-Shell_04.png
[imgQshell5]: images/images51/qshell/Q-Shell_05.png


#Getting Familiar with the Q-Shell

## Starting the Q-Shell
When you have installed Pylabs, go to the folder `/opt/qbase5`.

Enter the following command to launch the Q-Shell: `./qshell`

![Q-Shell window][imgQshell1]


## Name Spaces

The Q-Shell has three main name spaces:

* **q.**: the main name space of Pylabs, used for automation scripts, configuring Pylabs extensions, ...
* **i.**: interactive name space, functions in this name space require user input
* **p.**: the name space to manage Pylabs applications


## Using the Q-Shell

Throughout the complete Q-Shell you can use TAB-completion for minimizing the time in entering commands and avoiding to enter erroneous commands.

Type `q.` and press TAB and you see the list of name spaces of the `q` name space.

![q Name Space][imgQshell2]

Now add `gu` + TAB to enter the `gui` name space. Press '.d' + TAB to go into the `dialog` section, followed by '.m' + TAB to call the `message` function.
Add a string message, close with a bracket, and press ENTER.

![Show message][imgQshell3]

If you need help with a function, you can call the help-function by appending `?` to `q.qui.dialog.message(` and, then press ENTER.

![Help function][imgQshell4]

You can even open the source code of the function by adding a double question mark behind the function.

![Help function source][imgQshell5]
