#Form and Wizard Conventions

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

    Are you sure you want to delete customer Doe Inc?


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


To force the GUI to navigate to the job detail page (for example commands started with the parameter 'wait': False):


    q.gui.dialog.navigateTo("cmc://job?action=view&jobguid=<jobguid>")


##Wizard Structure

All text messages in message boxes and labels must be grouped as constants at the top of the wizard source file:

[[code]]
__author__ = 'incubaid'
__tags__ = 'wizard','customer_delete'
__priority__= 3

CUSTOMERGUID_MISSING = "No Customer Identifier was provided - Aborting."
CUSTOMERGUID_MISSING_TITLE = "Missing parameter"
[[/code]]

The main method only contains:
* Cloud API calls to retrieve information.
* Form definitions.

Other points:

* Minimize the usage of the showLogging statements. Use message boxes instead.
* Whenever an action is about to make changes to the model, ask for a confirmation.
* All cloud API calls to perform the action are grouped in the 'callCloudAPI' method.
* All validation of input is centralized into a 'ValidateInput' method.

*Note:* For the previous two points. Pass the cloud API as a parameter instead of creating a new connection.

The wizard ends with a `navigateTo` following the conventions mentioned above.


##Tips & Tricks

This section will help you write better efficient code.

* Avoid retrieving a full Root Object (`getObject`-method), (de)serializing is a costly method. Most of the time a list method suffices:

Do:

    customer = cloudAPI.customer.list(customerguid=customerguid)['result']
    customername = customer[0]['name']

Don't:

    customer = cloudAPI.customer.getObject(customerguid)

* Use `map` and `lambda` expressions for building lists to be displayed in a wizard, even if `map` and `lambda` expressions are harder to read, they are a lot more efficient. More information about the `map` function can be found [here] (http://docs.python.org/library/functions.html?highlight=map#map), about the `lambda` control form [here] (http://docs.python.org/tutorial/controlflow.html#lambda-forms).

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
