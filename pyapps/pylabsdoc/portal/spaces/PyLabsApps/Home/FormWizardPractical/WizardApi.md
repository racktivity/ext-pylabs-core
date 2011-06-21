@metadata title=Wizard API
@metadata order=30
@metadata tagstring=wizard api

#Wizard API

In this section you can find the API documentation of the methods to create wizards in a PyLabs Application.
The methods to create a wizard are available in the name space `q.gui.dialog.`.


##askChoice

[[code]]
def askChoice(self, question, choices, defaultValue = None, pageSize = 10, sortChoices=False, sortCallBack=None):
    """
    Ask the user the supplied question and list the choices to choose from, if no response given the default value is used

    @param question: question to be display to the user
    @param choices: list of choices for the user to choose from
    @param defaultValue: the value that will be used if no response given
    @param pageSize: max number of choices that can be prompted to the user in a single screen
    @param sortChoices: if True, choices will be sorted before showing them to the user
    @param sortCallBack: A callback function to handle the sorting of the choices (will only be used if sortChoices is set to True)

    @return:  selected choice
    """
[[/code]]    
        
Example:

    choices = ['foo', 'bar', 'baz']
    question = 'Make your choice:'
    In [1]: choices = ['foo', 'bar', 'baz']

    In [2]: question = 'Make your choice:'

    In [3]: mychoice = q.gui.dialog.askChoice(question, choices)
    Make your choice:
        1: foo
        2: bar
        3: baz
        Select Nr (1-3): 1

    In [4]: mychoice
    Out[4]: 'foo'
    
        
##askChoiceMultiple

[[code]]
def askChoiceMultiple(self, question, choices, defaultValue = None, pageSize = 10, sortChoices=False, sortCallBack=None):
    """
    Ask the user the supplied question and list the choices to choose from, if no response given the default value[s] is used

    @param question: question to be display to the user
    @param choices: list of choices for the user to choose from
    @param defaultValue: default value assumed if no user response is given, default value can be a single value or a comma separated list of values
    @param pageSize: max number of choices that can be prompted to the user in a single screen
    @param sortChoices: if True, choices will be sorted before showing them to the user
    @param sortCallBack: A callback function to handle the sorting of the choices (will only be used if sortChoices is set to True)

    @return:  list of selected choice[s] or default value[s]
    """
[[/code]]    
        
Example:

    choices = ['foo', 'bar', 'baz']
    question = 'Make your choice:'
    In [1]: choices = ['foo', 'bar', 'baz']

    In [2]: question = 'Make your choice:'

    In [3]: mychoices = q.gui.dialog.askChoice(question, choices)
    Make your choice:
        1: foo
        2: bar
        3: baz
        Select Nr, use comma separation if more e.g. "1,4": 1,2

    In [4]: mychoices
    Out[4]: ['foo', 'bar']        
    
        
##askDate

[[code]]
def askDate(self, question, minValue = None, maxValue = None, selectedValue = None, format = 'YYYY/MM/DD'):
    """
    Asks user a question that its answer is a date between minValue and maxValue

    Note: this note my seem out of place, but is is important to note that currently in the EasyDialogConsole implementation only dates with format YYYY/MM/DD are supported

    @param question: question that will be prompted to the user
    @param minValue: optional value for the lower boundary date
    @param maxValue: optional value for the upper boundary date
    @param selectedValue:
    @param  format: the format of the input date
    """
[[/code]]    
        
Example:

    In [1]: date = q.gui.dialog.askDate('')
 
    Enter a date with format YYYY/MM/DD, where year can be 09 or 2009, day is 2 or 02:
    1939/10/27
    
    In [2]: date
    Out[2]: '1939/10/27'
       
        
##askDateTime

[[code]]
def askDateTime(self, question, minValue = None, maxValue = None, selectedValue = None, format = 'YYYY/MM/DD hh:mm'):
    """
    Asks user a question that its answer is a datetime between minValue and maxValue

    Note: this note my seem out of place, but is is important to note that currently in the EasyDialogConsole implementation only dates with format YYYY/MM/DD are supported

    @param question: question that will be prompted to the user
    @param minValue: optional value for the lower boundary date
    @param maxValue: optional value for the upper boundary date
    @param selectedValue:
    @param  format: the format of the input date
    """
[[/code]]    
        
        
##askDirPath

[[code]]
def askDirPath(self,message, startPath = None):
    """
    Prompts for a selection of a file path starting from startPath if given and '/' if not

    @param message: message that would be displayed to the user above the selection menu
    @param startPath: base dir of the navigation tree
    @return: path to the directory selected
    """
[[/code]]
 
        
##askFilePath

[[code]]
def askFilePath(self,message, startPath = None):
    """
    Prompts for a selection of a file path starting from startPath if given and '/' if not

    @param message: message that would be displayed to the user above the selection menu
    @param startPath: base dir of the navigation tree
    @return: path to the file selected
    """
[[/code]]
        
##askInteger

[[code]]
def askInteger(self, question, defaultValue = None):
    """
    Asks user the supplied question and prompt for an answer, if none given the default value is used, the response and the default value must be valid integer

    @param question: question to be displayed
    @param defaultValue: if the user did not provide a response this value is used as an answer
    @return: response integer or the default value
    """
[[/code]]
        
Example:

    In [1]: age = q.gui.dialog.askInteger('Age')
    Age: 71
    
       
##askIntegers

[[code]]
def askIntegers(self, question):
    """
    Asks user the supplied question and prompt for an answer

    @param question: question to be prompted
    @return: response integer
    """
[[/code]]
        

##askMultiline

[[code]]
def askMultiline(self, question, defaultValue=None):
    """
    Asks the user the supplied question, where the answer could be multi-lines

    @param question: the question to be displayed
    """
[[/code]]
       

##askPassword
Asks for a password (with confirmation), including a check if the entered passwords are identical.

[[code]]
def askPassword(self, question, defaultValue=None):
    """
    Asks the supplied question and prompts for password

    @param question: question to be displayed
    @return: response string
    """
[[/code]]
        
Example:

    In [1]: newpassword = q.gui.dialog.askPassword('Enter new password')
    Enter new password: 
    Enter new password (confirm): 

    #passwords not identical:
    In [2]: newpassword = q.gui.dialog.askPassword('Enter new password')
    Enter new password: 
    Enter new password (confirm): 
     Invalid password!
    Enter new password: 
    Enter new password (confirm): 

    In [3]:
        

##askString

[[code]]
def askString(self,question, defaultValue = None, validator=None):
    """
    Asks the user the supplied question and prompt for an answer, if none given the default value is used
    @param question: question to be displayed
    @param defaultValue: if the user did not provide a response this value is used as an answer
    @param validator: regex validation value
    @return: response string or the default value
    """
[[/code]]
        
Example:

    In [1]: name = q.gui.dialog.askString('Name')
    Name: John Cleese
        
        
##askYesNo

[[code]]
def askYesNo(self,question, defaultValue = None):
    """
    Asks user the supplied question and prompt for an answer, if none given the default value is used, the response and the default value one of the values [y|Y|yes|Yes..n|N|No..]

    Note:For the EasyDialogConol implementation, currently the default value effect is ignored since it would require changing the pylabs vapp
    @param question: question to be prompted
    @param defaultValue: if the user did not provide a response this value is used as an answer
    @return: response answer or the default value
    """
[[/code]]
        
Example:

    In [1]: answer = q.gui.dialog.askYesNo('Are you John Cleese')
    Are you 18 or older (y/n):y   
        

##message

[[code]]
def message(self, message):
    """
    prints the given message to the screen

    @param message: message to print
    """
[[/code]]     
        
Example:

    In [20]: q.gui.dialog.message('Hello World')
     Hello World
        

##showMessageBox

[[code]]
def showMessageBox(self, message, title, msgboxButtons = "OK", msgboxIcon = "Information", defaultButton = "OK"):
    """
    Shows a large message box

    @param message: message for the messagebox
    @param title: title of the messagebox
    @param msgboxButtons: buttons to show in the messagebox. Possible values are 'OKCancel', 'YesNo', 'YesNoCancel', 'OK'
    @param msgboxIcon: icon to show in the messagebox. Possible values are 'None', 'Error', 'Warning', 'Information', 'Question'
    @param defaultButton: default button for the messagebox. Possible values are 'OK', 'Cancel', 'Yes', 'No'
    
    @return: A JSON encoded string containing the selected button clicked
    """
[[/code]]    
        

##showProgress

[[code]]
def showProgress(self, minvalue, maxvalue, currentvalue):
    """
    Shows a progress bar according to the given values

    @param minvalue: minVlue of scale
    @param maxvalue: maxvlaue of scale
    @param currentvalue: the current value to show the progress
    """
[[/code]]                                    