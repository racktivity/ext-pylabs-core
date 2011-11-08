@metadata spaceorder=80
@metadata title=Contributing in Style
@metadata tagstring=code contribute style guide

#Contributing in Style

This chapter is a short intermezzo to provide you the coding guidelines of Pylabs. 
When contributing to Pylabs, contribute in style and follow the rules as described on this page.


## `q` Should Be a Global Var

When you want to use the core Pylabs class `q`, make sure you call it the right way. 


## Import All Relevant Pylabs Packages

* e.g. `from event import QEvent`


## Private and Public methods

* Make sure that protected methods are really _protected_.
* Make sure that protected properties are really _protected_.
* Only expose _public_ method names.


## Do Not Use Getters and Setters

* Use properties instead.
* Use the code formatter functionality to generate the properties automatically for you


## Add Logging 

Use the Pylabs logging system with `q.logger.log(...)`

* There are 9 log levels.
** Use the appropriate level.
* Put clear and useful descriptions in logging.


## Throw Events
Use the Pylabs event management `q.eventhandler`

* There are 4 event levels.
** Use the appropriate level.
* Put clear and useful description in the event.
* The `raise` statement can be used but will always result in a _critical_ event or use `q.eventhandler.raiseWarning(...)`.


## Use the Type Classes in Types Package

Use the Pylabs enumerators, available in `q.enumerators`

* e.g. `q.enumerators.PlatformType.LINUX64


## Add Documentation

It is very important to make your code as clear as possible. By adding concise but clear documentation, it is easier to examine your code and you provide interactive help to the users.


### Document a Module

[[code]]
"""Short description on single line
<empty line here>
multiple lines
for a full module
has to be put at top of page
"""
import ...
[[/code]]


###Document a Class

[[code]]
class testclass(...):
    """Short description on single line
    <empty line here>
    multiple lines
    for a class
    has to be put just underneathclass"""
[[/code]]


###Document a Method

[[code]]
class testclass(...):

    def afunction(self,param):
        """Short description on single line
            <empty line here>
            multiple lines
        for a method
        has to be put just underneath method"""
        print "test"
[[/code]]


###Document a Parameter of a Method

[[code]]
class testclass(...):

    def afunction(self,param1,param2):
        """Short description on single line
            <empty line here>
            multiple lines
        for a method
        has to be put just underneath method

        #now follows how to document a parameter
        @type param1: type of the param
        @param param1: param1 is used to ...
        @type param2: type of the param
        @param param2: param2 is used to ...
        """
        print "test"
[[/code]]


##Coding Guidelines

Here are some basic coding guidelines.


###Naming Conventions

* Q-Package names are lowercase
* Class names are camelcase with leading capital
* Class method and attribute names are camelCase with leading lowercase
* Function names are camelCase with leading lowercase
* Constants are all upper case.
* If the constant will be used outside the module that defines it, it should be declared as a Pylabs enumeration.
* Global variables should be prefixed with a `g` (e.g. `gCounter`)

* Root object file naming conventions
    ** Root objects are represented as directories. The name of the root object is all lowercase.
    ** Each root object action has its own subdirectory located in the root object directory. The name of the action is written in camelCase with leading lowercase.
    ** Each root object action directory has a single Python file containing the corresponding tasklet. The name of the file is `<priority>_<rootobject>_<action>.py`

* Actor action file naming conventions
    ** Actor objects are represented as directories. The name of the actor object is all lowercase.
    ** Each actor action has its own subdirectory located in the actor object directory. The name of the action is written in camelCase with leading lowercase.
    ** Each actor action directory has a Python file containing the corresponding tasklet. The name of the file is `<priority>_<actorobject>_<action>.py`
    ** If the action can launch RScripts, the actor action directory will have a subdirectory named "scripts". The RScripts will be located in this directory.

* RScript naming conventions
    ** Each rscript has the extension `.rscript`.
    ** The file name of the RScript is camelCase with leading lowercase


###Architectural Conventions

####Tasklets

* Provide sensible values for:
    ** \_\_author\_\_
    ** (optional) \_\_tags\_\_
    ** (optional) \_\_priority\_\_

* Match functions are lightweight:
    ** Do not make DRP requests
    ** Do not access the file system
    ** Do not access the network
    ** Do not use any locking


####Root Object Actions

* Are the only WFE tasklets allowed to perform DRP calls in their main function
* Are not allowed to make blocking calls
    ** Do not access the file system or the network. With the exception of the following:
        *** DRP calls through the DRP tasklet
    ** What about limiting the list of Python modules that can be used?
    ** Do not use locking
* Are the only WFE tasklets allowed to trigger other root object actions or actor actions
* Are not allowed to run RScripts

####Actor Actions

* Are not allowed to make DRP calls
* Are not allowed to make blocking calls
    ** Are not allowed to access the file system or the network. With the exception of the following:
        *** Logging (until we have queues?)
        *** Events (until we have queues?)
    ** What about limiting the list of Python modules that can be used?
    **  Do not use locking
* Are not allowed to trigger other actor actions or root object actions
* Are allowed to run RScripts


####RScripts

* Are not allowed to access DRP
* Are not allowed to invoke root object or actor actions
* Are the only place in the job execution stack to make blocking calls
    ** All access to the network and file system go here
    ** All synchronization that requires locking goes here
* Standardize on (execution)params
    ** In: name, description, userErrormsg, internalErrormsg, maxduration, wait, timetostart, priority
    ** Out (Modified params dictionary):
    ** result

###Documentation

####Logging

LogLevel classifies the message towards its intended reader and/or targeted device for reading.

<table width="400">
<tr>
<th align="left" width="250" bgcolor="#D8D8D8">Loglevel</th><th width="150" bgcolor="#D8D8D8">Numeric Code</th>
</tr>
<tr>
<td>ENDUSERMESSAGE</td><td align="center">1</td>
</tr>
<tr>
<td>OPERATORMESSAGE</td><td align="center">2</td>
</tr>
<tr>
<td>STDOUT</td><td align="center">3</td>
</tr>
<tr>
<td>STDERR</td><td align="center">4</td>
</tr>
<tr>
<td>TRACING1</td><td align="center">5</td>
</tr>
<tr>
<td>TRACING2</td><td align="center">6</td>
</tr>
<tr>
<td>TRACING3</td><td align="center">7</td>
</tr>
<tr>
<td>TRACING4</td><td align="center">8</td>
</tr>
<tr>
<td>TRACING5</td><td align="center">9</td>
</tr>
<tr>
<td>SPECIALLEVEL</td><td align="center">10</td>
</tr>
</table>
