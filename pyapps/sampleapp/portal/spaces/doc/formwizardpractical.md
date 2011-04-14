#Creating Forms and Wizards

In the PyLabs 5 framework, wizards are used to execute actions on a certain Root Object. As most of the functionality, wizards can also be defined by writing a simple tasklet.
Wizards are the way to make highly interactive windows which result in executing one or more cloudAPI calls.

Wizards should only use the cloudAPI to fetch required information and to execute actions.

The wizard dialect is fully integrated in the PyLabs framework. The main entry point to define wizards is located at `q.gui.form`.


##General Structure of a Form/Wizard Tasklet

Since a wizard is implemented by using the [tasklet](http://confluence.incubaid.com/display/PYLABS/Tasklets) framework, it contains all sections like any other tasklet.

Sections:

* Tags: instruct the wizard engine which tasklets should be triggered under which circumstances
* Author: allows you to identify who was the creator of the corresponding wizard
* Priority: execution priority of tasklet, 1 is lowest priority
* Callback method(s): see Callbacks-section for more information
* Main method: this method contains the actual implementation of the wizard
* Match method: this method is invoked before the main method is executed. The Main method is only executed if match method returns True. For wizard tasklets, the match method must always return True. Multiple implementations of the same wizard are not supported.

Example skeleton for a wizard tasklet:

    \# 'wizard' tag is required, second tag is the name of the wizard rootobject_action e.g. vdc_start
    __tags__= 'wizard','wizard_name'
    __author__='incubaid'
    __priority__ = 1
    
    def callCloudAPI(api, arg1, arg2, arg3):
        """execute the cloud API call"""
    	result = api.<sampleapp>.<rootobject>.<function>(arg1, arg2, arg3)['result']    
	    return result

    def main(q, i, params, tags):
        <code to create wizard and form>

        result = callCloudAPI(p.api, 
                              tab.elements['arg1'].value,
                              tab.elements['arg2'].value,
                              tab.elements['arg3'].value)
        params['result']=result
   
    def match(q, i, params, tags):
        return True

The wizard tasklets are stored in the directory `<pyapp name>/impl/ui/<form/wizard>/<domain>`. See the [PyApps Directory Structure](/sampleapp/#/doc/sampleapp) for more information about the location of the files.

It is highly recommended to create `callCloudAPI` method as shown in the tasklet above. This method will call the actual [action tasklet](/sampleapp/#/doc/actiontasklet), which receives the arguments through the `params` dictionary.


##Creating Forms
A form is a GUI element that consists of one tab. This tab contains a number of self-defined fields. A form object is created in the `q.gui.form` name space. This form object must contain tab object, which on its turn will contain different fields. 

When you create a tab in your form, you get always the following two buttons, *OK* and *CANCEL*. The *CANCEL* button will close the form, the *OK* button will continue in the main function, to eventually end in a cloud API call.

Creating a form with one tab goes as follows:

    TAB_GENERAL_TITLE = 'My TAB'

    form = q.gui.form.createForm()
    tab_general = form.addTab('general', TAB_GENERAL_TITLE)

The `addTab` function expects two arguments, a unique ID ('general' in the above example) and  a title name for the tab.

The tab object has several methods to fill your form with text fields, choices, multiple choices, yes/no questions, ... The methods have clear names so you know which type of field you are going to add.
See the [Form and Wizard API](/sampleapp/#/doc/formwizard) for details about the fields.

An example of a basic form:

    TAB_GENERAL_NAME = 'Give your name'
    TAB_GENERAL_AGE = 'How old are you'
    TAB_GENERAL_GENDER = 'Female/Male'

    tab_general.addText(name = 'name', text = TAB_GENERAL_NAME)
    tab_general.addInteger(name = 'age', text = TAB_GENERAL_AGE)
    tab_general.addDropdown(name = 'gender', text = TAB_GENERAL_GENDER, values = genderList(q))

The third field shows a drop-down box with a list that need to be retrieved in the tasklet itself.

    def genderList(q):
        gender = q.enumerators.gender._pm_enumeration_items
        return gender

This function works provided that you created your proper enumerator 'gender'. See [Modeling Root Objects](/sampleapp/#/doc/modeling) to create your custom enumerator.

Once all fields are filled, the user will have to click on one of the provided buttons, *OK* or *CANCEL*. When the user clicks *OK*, the tasklet continues with the main function. Either you call the `callCloudAPI` function, which will execute an action, using the data entered by the user, or you can show a confirmation window.

Below you can see how a pop-up window will appear when the user clicks *OK* on the tab:

    MSGBOX_CREATE_CONFIRMATION = 'Create this new user?'
    MSGBOX_CREATE_CONFIRMATION_TITLE = 'Create User'

    answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
                                         title=MSGBOX_CREATE_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')    

For more details about the `showMessageBox` function, we refer to the [API documentation] (api/index.html) of PyLabs 5.

To trigger an action with the provided data, you have to call the `callCloudAPI` method:

    result = callCloudAPI(p.api,
                          tab_general.elements['name'].value,
                          tab_general.elements['age'].value,
                          tab_general.elements['gender'].value)

    params['result'] = result

The last line is a PyLabs 5 specific dictionary. This `params` dictionary is used throughout the whole PyLabs 5 framework and is a key element to pass on data from one level to another.


##Creating Wizards
Unlike forms, where a user provides data in one window, you can opt for a wizard where you ask your data in multiple tabs. Instead of creating a form in the `main` function, a wizard consists of GUI elements one after each other.
Each request for user interaction occurs in one window. The windows are created via the `q.gui.dialog` name space.

The above form in wizard style then looks like:

    name = q.gui.dialog.askString('Give your name')
    age = q.gui.dialog.askInteger('How old are you')
    gender = q.gui.dialog.askChoice('Female/Male', genderList(q))

    answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
                                         title=MSGBOX_CREATE_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')


##Other Forms
In this section we will show some other common structures with the usage of forms.


###Updating Object Properties
When you want to update the properties of an object, it is likely that the user sees the actual values. The creation of the form and the tab is similar to the given example, except that you now show the actual property of the object. Therefore, the `main` function of your tasklet must also contain a line that retrieves the concerned object.

    user = p.api.action.<sampleapp>.<rootobject>.getObject(params['<rootobjectguid>'], executionparams={'description': 'Retrieving <rootobject> information'})
    
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    tab_general.addText(name = 'name', text = TAB_GENERAL_NAME, value = user.name)
    tab_general.addInteger(name = 'age', text = TAB_GENERAL_AGE, value = user.age)
    tab_general.addDropdown(name = 'gender', text = TAB_GENERAL_GENDER, values = genderList(q), selectedValue = user.gender)


###Load a Form with Provided Data
When you create a form that has more than one tab in which the user must provide information, you may want to show an overview of all entered data before an object is created.

The flow is then as follows:

1. Create form
2. Create tabs on the form, each with its own specific questions
3. Create a new empty form
4. Load the empty form with the form from the first two steps

In the example below, we create a form with two tabs. Each tab will have a number of questions. Before the cloud API call is executed, the user will see a new form with all his provided data.

    form = q.gui.form.createForm()
    tab1 = form.addTab('userTab','General')
    tab2 = form.addTab('infoTab','Information')

    tab1.addText('name', text = TAB_GENERAL_NAME)
    tab1.addInteger(name = 'age', text = TAB_GENERAL_AGE)
    tab1.addDropdown(name = 'gender', text = TAB_GENERAL_GENDER, values = genderList(q))

    tab2.addText('street', text = TAB_INFORMATION_STREET)
    tab2.addInteger(name = 'number', text = TAB_INFORMATION_NUMBER)
    tab2.addText(name = 'zip', text = TAB_INFORMATION_ZIP)
    tab2.addText(name = 'city', text = TAB_INFORMATION_CITY)

Now that you have defined all fields in the two tabs, we create a new empty form. In this empty form we will load the form, created above. This results in a form which contains the tabs and all fields filled out with the user data.

    resultform = q.gui.form.createForm()
    resultform.loadForm(q.gui.dialog.askForm(form))

    answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
                                         title=MSGBOX_CREATE_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')

Displaying the form itself, including its content and values, is done with the command `q.gui.dialog.askForm(form)`.
Similar to the other forms, you must execute a cloud API call for the creation of an object.

    result = callCloudAPI(p.api,
                          tab1.elements['name'].value,
                          tab1.elements['age'].value,
                          tab1.elements['gender'].value,
                          tab2.elements['street'].value,
                          tab2.elements['number'].value,
                          tab2.elements['zip'].value,
                          tab2.elements['city'].value,

    params['result'] = result


##What's Next?
In this chapter you have learned how you can create forms and wizards. For more details about the forms and wizards methods, we refer to the [Form and Wizard API](/sampleapp/#/doc/formwizard)
In the next chapter you will learn the actual implementation of the actions in your PyApp, store, update, delete objects in the DRP, create lists, ...
