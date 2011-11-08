@metadata title=Interactive Scripts
@metadata order=40
@metadata tagstring=interactive qshellconfig


#Adding Interactivity to Scripts

The Pylabs framework is designed to create scripts. These scripts can be executed in an unattended way. However sometimes you may need user input to complete a script, for example in an installation script asking for the hostname of the machine.
Pylabs scripts are by default non-interactive and therefore you must enable the interactivity in your scripts, if interactivity is required.

To do so, add this line to your script, at least after the `from pylabs.InitBase import *` line:

[[code]]
q.qshellconfig.interactive = True
[[/code]]


##Interactive Methods in Pylabs
In the Q-Shell, the interactive methods are all located in the `q.gui.dialog` name space:

    q.gui.dialog.askChoice(          q.gui.dialog.askString(
    q.gui.dialog.askChoiceMultiple(  q.gui.dialog.askYesNo(
    q.gui.dialog.askDate(            q.gui.dialog.chooseDialogType(
    q.gui.dialog.askDateTime(        q.gui.dialog.clear(
    q.gui.dialog.askDirPath(         q.gui.dialog.easyDialog
    q.gui.dialog.askFilePath(        q.gui.dialog.message(
    q.gui.dialog.askForm(            q.gui.dialog.navigateTo(
    q.gui.dialog.askInteger(         q.gui.dialog.showLogging(
    q.gui.dialog.askIntegers(        q.gui.dialog.showMessageBox(
    q.gui.dialog.askMultiline(       q.gui.dialog.showProgress(
    q.gui.dialog.askPassword(        q.gui.dialog.type
    
As you can see there are various functions available to create interactive scripts. 
Each of the methods require a string with the question that you want to show to the user. Some of them require some more arguments, to complete the function, for example a list from which the user can select an option.

Some of the functions are so clear that they will not be explained here, for example `q.gui.dialog.askInteger` or `q.gui.dialog.askString`. Others require some attention and will be shown here by means of basic examples.

**q.gui.dialog.askChoice**
This method lets the user make a choice from a list of options.

[[code]]
In [192]: answer = q.gui.dialog.askChoice('Which movie do you prefer:',['Holy Grail','Life of Brian','Meaning of Life'])
 Which movie do you prefer:
    1: Holy Grail
    2: Life of Brian
    3: Meaning of Life
    Select Nr (1-3): 1

In [193]: answer
Out[193]: 'Holy Grail'
[[/code]]

The function returns the value of the list as shown in the example.
If the user may select more than one option, use the `q.gui.dialog.askChoiceMultiple` method. The function returns a list, even if the user only selects one option.

[[code]]
In [195]: answer = q.gui.dialog.askChoiceMultiple('Which movies do you prefer:',['Holy Grail','Life of Brian','Meaning of Life'])
 Which movies do you prefer:
    1: Holy Grail
    2: Life of Brian
    3: Meaning of Life
    Select Nr, use comma separation if more e.g. "1,4": 2,3

In [196]: answer
Out[196]: ['Life of Brian', 'Meaning of Life']
[[/code]]

**q.gui.dialog.askPassword**
This method is used to ask a password. Automatically a confirmation is requested and verified if it matches the first entered password. 

[[code]]
In [219]: pwd = q.gui.dialog.askPassword('Enter your password')
Enter your password: 
Enter your password (confirm): 

In [220]: pwd
Out[220]: 'test'
[[/code]]

**q.gui.dialog.askYesNo**
This method is an easy way to ask a yes/no question. The result is a boolean.

[[code]]
In [224]: answer = q.gui.dialog.askYesNo('Do you like Monthy Python?')
Do you like Monthy Python? (y/n):y

In [225]: answer
Out[225]: True
[[/code]] 


##Example of an Interactive Script
Your first Pylabs script was the Hello World script. In the example below we add some interactivity to this script:

[[code]]
from pylabs.InitBase import *

q.qshellconfig.interactive = True
 
q.application.appname = "exampleApp"
q.application.start()

answer = q.gui.dialog.askYesNo("Do you want to say hello?")
 
if answer:
    q.gui.dialog.message("Hello World!")
 
else:
    q.gui.dialog.message("Bye Bye World!")
 
q.application.stop()
[[/code]]
