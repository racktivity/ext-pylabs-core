#Wizard Conventions

Below are some wizard conventions to use:

* Avoid low level talk and expressions.
* When displaying a value, put single quotes around the value.
* When using 'askYesNo', first put a 'message' with the question, then add the 'askYesNo' without the question.
* Do not use exclamation marks
* Do not use capitalized words unless it is an acronym.
* The log field must be seen as error field. No 'affirmative' or 'positive' logging may be done, since it will be displayed in red, and red represents a problem.
* Avoid the phrase: 'Are you sure'.

Use:

    Delete customer 'Doe Inc'?

Instead of:

    Are you sure you want to delete customer 'Doe Inc'?


## Naming Conventions

Use the following naming conventions for each parameter below:

* name: spaces are replaced by an underscore.
* tag: put root object first and then the action. For example: customer_edit.
* filename: should be the same as the tag + '.py'


##Navigation Conventions

To refresh the GUI after updating or creating a root object:


    q.gui.dialog.navigateTo("cmc://<rootobject>?action=refresh")


To refresh the GUI after the deletion of a root object:


    q.gui.dialog.navigateTo("cmc://<rootobject>?action=delete")


To force the GUI to navigate to the job detail page (eg. commands started with the parameter 'wait':False):


    q.gui.dialog.navigateTo("cmc://job?action=view&jobguid=<jobguid>")



## Wizard Structure

All text messages in messageboxes, labels must be grouped as CONSTANTS at the top of the wizard source file:

    __author__ = 'incubaid'
    __tags__ = 'wizard','customer_delete'
    __priority__= 3

    CUSTOMERGUID_MISSING = "No Customer Identifier was provided - Aborting."
    CUSTOMERGUID_MISSING_TITLE = "Missing parameter"

The main method only contains:
* Cloud API calls to retrieve information.
* Form definitions.

Other points:

* Minimize the usage of the showLogging statements. Use messageboxes instead.
* Whenever an action is about to make changes to the model, ask for a confirmation.
* All cloud API calls to perform the action are grouped in the 'callCloudAPI' method.
* All validation of input is centralized into a 'ValidateInput' method.

*Note:* For the previous two points. pass the cloud API as a parameter instead of creating a new connection.

The wizard ends with a navigateTo following the conventions mentioned above.


## Tips & Tricks

This section will help you write better efficient code.

* Avoid retrieving a full Root Object (`getObject`-method), (de)serializing is a costly method. Most of the time a list method suffices:

Do:

    customer = cloudAPI.customer.list(customerguid=customerguid)['result']
    customername = customer[0]['name']

Don't:

    customer = cloudAPI.customer.getObject(customerguid)

* Use `map` and `lambda` expression for building lists to be displayed in a wizard, even if map and lambda expressions are harder to read, they are a lot more efficient:

Do:

    map(lambda x: customers.__setitem__(x['guid'], '%s'%x['name']), result)

Don't:

    for customer in customers:
        user[customer['guid']] = customer['name']

* Avoid loops when possible:

Do:

    if 'customerguid' in params['extra'].iterkeys():
        customerguid = params['extra']
    else:
        q.gui.dialog.showMessageBox(message = 'No customerguid found - Aborting', title='myTitle')
        return
{code}h1. Wizard Conventions

Below are some wizard conventions that we use:

* Always avoid low level talk and expressions.
* When displaying a machine name, always insure you put single quotes around the name.
* When using 'askYesNo', first put a 'message' with the question, then add the 'askYesNo' without the question.
* Avoid using exclamation marks or capitalized words unless it's absolutely necessary or if it's an abbreviation.
* The log field must be seen as error field. No 'affirmative' or 'positive' logging may be done, since it will be displayed in red, and red represents a problem.
* Avoid the phrase: 'Are you sure'.
{tip:title=Example:}
Use:
{code:none}
Delete machine 'dingske'?
{code}
Instead of:
{code:none}
Are you sure you want to delete machine 'dingske'?
{code}
{tip}

h2. Naming Conventions

Use the following naming conventions for each parameter below:

* *name*: spaces are replaced by an underscore.
* *tag*: put root object first and then the action. For example: smart_client_edit.
* *filename*: should be the same as the tag + '.py'

h2. Navigation Conventions

To refresh the GUI after updating or creating a root object:

{code:none}
q.gui.dialog.navigateTo("cmc://<rootobject>?action=refresh")
{code}

To refresh the GUI after the deletion of a root object:

{code:none}
q.gui.dialog.navigateTo("cmc://<rootobject>?action=delete")
{code}

To force the GUI to navigate to the job detail page (eg. commands started with the parameter 'wait':False):

{code:none}
q.gui.dialog.navigateTo("cmc://job?action=view&jobguid=<jobguid>")
{code}


h2. Wizard Structure

All text messages in messageboxes, labels must be grouped as CONSTANTS at the top of the wizard source file:

{info:title=Example:}
{code}
__author__ = 'aserver'
__tags__ = 'wizard','smart_client_delete'
__priority__= 3

MACHINEGUID_MISSING = "No Smart Client Identifier was provided - Aborting."
MACHINEGUID_MISSING_TITLE = "Missing parameter"
{code}
{info}

The main method only contains:
* Cloud API calls to retrieve information.
* Form definitions.

Other points:

* Minimize the usage of the showLogging statements. Use messageboxes instead.
* Whenever an action is about to make changes to the model, ask for a confirmation.
* All cloud API calls to perform the action are grouped in the 'callCloudAPI' method.
* All validation of input is centralized into a 'ValidateInput' method.

{note}
*Note:* For the previous two points. pass the cloud API as a parameter instead of creating a new connection.
{note}

The wizard ends with a navigateTo following the conventions mentioned above.

## Tips & Tricks

This section will help you write better efficient code.

* Avoid using 'getObject' as serializing is a costly method, check whether a list method suffices:

{tip:title=Do:}
{code}
machine = cloudAPI.machine.list(machineguid=machineguid)['result']
machinename = machine[0]['name']
{code}
{tip}

{warning:title=Don't:}
{code}
machine = cloudAPI.machine.getObject(machineguid)
{code}
{warning}

* Use map and lambda expression for building lists to be displayed in a wizard, even if map and lambda expressions are harder to read, they are a lot more efficient:

{tip:title=Do:}
{code}
map(lambda x: qlans.__setitem__(x['guid'], '%s'%x['name']), result)
{code}
{tip}

{warning:title=Don't:}
{code}
for qlan in qlans:
    networkDict[qlan['guid']] = qlan['name']
{code}
{warning}

* Avoid loops when possible:

{tip:title=Do:}
{code}
    if 'machineguid' in params['extra'].iterkeys():
        machineguid = params['extra']
    else:
        q.gui.dialog.showMessageBox(message = 'No machineguid provided - Aborting!', title='myTitle')
        return

Don't:

    for key in params['extra'].iterkeys():
        if key == 'customerguid':
            customerguid = extra['customerguid']
