#Form API

In this section you can find the API documentation of the methods to create forms in a PyLabs Application.
The methods to create a form are available in the name space `q.gui.form.`.


###createForm()

This method instructs the wizard engine to create new form. The return value is a new wizard form object.

Example:
    q.gui.form.createForm(?<ENTER>
    
    Definition:     q.gui.form.createForm(self)
    Documentation:
        Create new wizard form object
    
        Returns: WizardForm object
    
    
    form = q.gui.form.createForm()


###askForm()

This method presents the constructed form to the end-user and wait until this user completes the wizard.

Example:

    form = q.gui.form.createForm()
    tab = form.addTab('general', 'General')
    tab.message('message_hello', 'Hello World!')
    retvalue = q.gui.dialog.askForm(form)


###loadForm()

Load a form object from a result of the askForm call.
This transforms the dict to a form object.

Example:

    form = q.gui.form.loadForm(q.guid.dialog.askForm(form))


###addTab()

Multiple tab pages can be created on a wizard form object. Tab pages allow you to group a set of related controls.
At least 1 tab must be created before you can start adding other controls.

Example:

    form.addTab(?<ENTER>
    
    Definition:     form.addTab(self, name, text)
    Documentation:
        Add new tab to form
    
    
        Parameters:
    
        - name: Unique name for this control
        - text: Text to be displayed in tab label
    
        Returns: WizardTab object
    
    tab = form.addTab('tab_general', 'General')


###message()

The message control allows you to display read-only information to the end-user.
Message controls can only be added on tab pages.

Example:

    tab.message(?<ENTER>
    
    Definition:     tab.message(self, name, text, bold=False, multiline=False)
    Documentation:
        Create a display action containing label.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - bold:          Define if the font should be bold
        - multiline:     Use multiline label
    
    tab.message('msg_welcome', 'Welcome to the sample wizard', True, False)


###addText()

The text control allows you to retrieve string input from the end-user.
Text controls can only be added on tab pages.

Example:

    tab.addText(?<ENTER>
    
    Definition:     tab.addText(self, name, text, value=None, multiline=False, validator=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing textbox control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - value:         Text to pre-populate textbox field with
        - multiline:     Use multiline label
        - validator:     Define validator to restrict text input
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addText(name='txt_name', text='Please give name',value='<YOUR NAME>', multiline=False, validator='[az-AZ-09]', helpText='Please provide your name. Allowed characters are A to Z and 0 to 9')


###addMultiline()

The multiline control allows you to retrieve large string input from the end-user.
Multiline controls can only be added on tab pages.

Example:

    tab.addMultiline(?<ENTER>
    Definition:     tab.addMultiline(self, name, text, value=None, validator=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing multiline textbox control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - value:         Text to pre-populate textbox field with
        - validator:     Define validator to restrict text input
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addMultiline(name='txt_notes', text='Additional notes', helpText='Please provide additional notes')


###addInteger()

The integer control allows you to retrieve integer value input from the end-user.
Integer controls can only be added on tab pages.

Example:

    tab.addInteger(?<ENTER>

    Definition:     tab.addInteger(self, name, text, minValue=None, maxValue=None, value=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing integer selector control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - minValue:      Minimum value for the number
        - maxvalue:      Maximum value for the number
        - value:         Number to pre-populate textbox field with
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addInteger(name='num_licenses', text='Number of licenses', minValue=1, maxValue=100, selectedValue=1)


###addIntegers()

The integers control allows you to retrieve a list of comma separated integer values from the end-user.
Integer controls can only be added on tab pages.

Example:

    tab.addIntegers(?<ENTER>

    Definition:     tab.addIntegers(self, name, question, value=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing integers selector control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - question:      Question to display in the label
        - value: Numbers to pre-populate textbox field with
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
     tab.addIntegers(name='num_list', question='Please provide 2 numbers between 1 and 10', helpText='Provide 2 numbers separated by a comma')


###addPassword()

The password control allows you to retrieve password input from the end-user.
Password controls can only be added on tab pages.

Example:

    tab.addPassword(?<ENTER>

    Definition:     tab.addPassword(self, name, text, value=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing password textbox control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - value:         Number to pre-populate textbox field with
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addPassword(name='passwd', text='Enter your password', helpText='Please provide your desired password')


###addYesNo()

The YesNo control allows you to retrieve boolean input from the end-user.
YesNo controls can only be added on tab pages.

Example:

    tab.addYesNo(?<ENTER>

    Definition:     tab.addYesNo(self, name, question, selectedValue=None, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing yes/no control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - question:      Question to display in the label
        - selectedValue: Index of the item to select
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addYesNo(name='yesno_finish', question='Are you sure this information is correct?')


###addChoice()

The choice control allows you to retrieve 1 selected value from a list of choices from the end-user. If the list of possible values contains 5 items or less, radio buttons are shown.
If the list of possible values is more than 5, the control automatically shows a dropdown list.
Choice controls can only be added on tab pages.

Example:

    tab.addChoice(?<ENTER>

    Definition:     tab.addChoice(self, name, text, values, selectedValue=0, optional=False, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing item selector control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - values:        Items to select out (dictionary)
        - selectedValue: Index of the item to select
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
     tab.addChoice(name='sel_department', text='Select department', values={'ENG': 'Engineering', 'SAL': 'Sales', 'MAR' : 'Marketing'},
                   selectedValue='ENG', helpText='Please select your department')


###addChoiceMultiple()

The multiple choice control allows you to retrieve multiple values from a list of choices from the end-user.
Multiple choice controls can only be added on tab pages.

Example:

    tab.addChoiceMultiple(?<ENTER>

    Definition:     tab.addChoiceMultiple(self, name, text, values, selectedValue=0, optional=False, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing multi items selector control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - values:        Items to select out (dictionary or list)
        - selectedValue: A list of indexes if 'values' is defined as a list. Otherwise, a list of keys from the 'values' dictionary.
        - optional:      Boolean indicating if selection is required
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control        @param trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    
    Example using dictionary as values :
    tab.addChoiceMultiple(name='sel_supported_os', text='Select supported operating systems', values={'WIN': 'Windows platforms', 'LIN': 'Linux platforms', 'OSX': 'MAC OS X platforms'},
                          selectedValue=['WIN', 'OSX'] , helpText='Please select all supported operating systems')
    
    
    
    Example using a list as values :
    tab.addChoiceMultiple(name='sel_supported_os', text='Select supported operating systems', values=('Windows platforms','Linux platforms','MAC OS X platforms'),
                          selectedValue=[0,2], helpText='Please select all supported operating systems')


###addDropDown()

The drop down control allows you to retrieve one value from a list of values from the end-user.
Drop down controls can only be added on tab pages.

Example:

    tab.addDropDown(?<ENTER>

    Definition:     tab.addDropDown(self, name, text, values, selectedValue=0, optional=False, message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing multi items dropdown control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - text:          Text to display in the label
        - values:        Items to select out (dictionary)
        - selectedValue: Index of the item to select
        - optional:      Boolean indicating if selection is required
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control        @param trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addDropDown(name='dd_supported_os', text='Select supported OS', values={'WIN': 'Windows platforms', 'LIN': 'Linux platforms', 'OSX': 'MAC OS X platforms'},
                    selectedValue='WIN', helpText='Please select the supported operating system')


###addDate()

The date control allows you to retrieve a date value from the end-user. In a wizard UI the date is selected from a UI date selector.
Date controls can only be added on tab pages.

Example:

    tab.addDate(?

    Definition:     tab.addDate(self, name, question, minValue=None, maxValue=None, selectedValue=None, format='YYYY/MM/DD', message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing date control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - question:      Question to display in the label
        - minValue:      Minimum value for the date
        - maxvalue:      Maximum value for the date
        - selectedValue: Default date
        - format:        Format to display date
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addDate(name='date_birth', question='Enter date of birth', helpText='Please enter your date of birth')


###addDateTime()

The datetime control allows you to retrieve a date / time value from the end-user. In a wizard UI the date and time are selected from a UI date and time selector.
Datetime controls can only be added on tab pages.

Example:

    tab.addDateTime(?<ENTER>

    Definition:     tab.addDateTime(self, name, question, minValue=None, maxValue=None, selectedValue=None, format='YYYY/MM/DD hh:mm', message='', status='', trigger=None, callback=None, helpText='')
    Documentation:
        Create a display action containing datetime control.
    
    
        Parameters:
    
        - name:          Unique name for the control
        - question:      Question to display in the label
        - minValue:      Minimum value for the date
        - maxvalue:      Maximum value for the date
        - selectedValue: Default datetime
        - format:        Format to display datetime
        - message:       Message to use for the tooltip or error message (depending on status)
        - status:        Current status of this control
        - trigger:       Event where the control should trigger on
        - callback:      Method that will be called, if event has been triggered
        - helpText:      Information about the usage/functionality of the control
    
    tab.addDateTime(name='start_time', question='Enter start time', helpText='Please enter the start time')


##Callbacks

The wizard framework allows you to create highly interactive interfaces. A callback mechanism is available to implement such functionality.

Every interactive control (text, password, yesno, choice, ...) provide the following parameters to allow immediate user interaction:

* trigger: this is the event where the control should trigger on. For now we only support 'click' and 'change'.
* callback: this method that will be called, if the event has been triggered. The callback method must be implemented in the same tasklet as where the wizard is defined. 
The method name must start with 'callback_' followed by the name specified in the callback parameter.
* message: message to show based on status of the control
* status: current status of this control. For now only 'error' status is supported.

Example:

    __tags__= 'wizard','wizard_name'
    __author__='incubaid'
    
    def callback_get_employees(q,i,params,tags):
        form = q.gui.form.createForm()
        formData = params['formData']
        form.loadForm(formData)
        ddGrp = form.tabs['tabGeneral'].elements['cboGroups']
        ddEmpl = form.tabs['tabGeneral'].elements['cboEmployee']
    
        if ddGrp.value == '1':
            ddEmpl.values = {1:'John',2:'Michael',3:'Graham',4:'Terry J'}
        if ddGrp.value == '2':
            ddEmpl.values = {1:'Terry G',2:'Eric'}
        if ddGrp.value == '3':
            ddEmpl.values = {1:'Andrew',2:'Connie'}
        if ddGrp.value == '4':
            ddEmpl.values = {1:'Brian',2:'Prunella'}
        return form
    
    def main(q,i,params,tags):
    
        helpTxt = 'See here some helptext to explain this control.\nIf you are still reading this, please go back to work, this is for testpurposes only :)'
        form = q.gui.form.createForm()
        tab1 = form.addTab('tabGeneral','General')
        form.tabs['tabGeneral'].message('labelGeneral','Callback sample' , bold=True)
        form.tabs['tabGeneral'].addChoice('cboGroups','Select your department',{1:'Engineering',2:'Sales', 3:'Marketing', 4:'Financial'}, trigger='change',callback='get_employees', helpText=helpTxt)
        form.tabs['tabGeneral'].addDropDown('cboEmployee','Select yourself',{}, helpText=helpTxt)
        q.gui.dialog.askForm(form)

    def match(q,i,params,tags):
        return True


##Sessionstate functionality

Sessionstate parameter gives the possibility to transfer metadata from the main method to the callbacks methods.
The metadata can be any type (string, integer, object...).

Example:

    __tags__= 'wizard','wizard_name'
    __author__='incubaid'
    
    def callback_retrieve_sessionstate(q,i,params,tags):
        session = params['SESSIONSTATE']
        info = session['myMetaData']
    
        form = q.gui.form.createForm()
        formData = params['formData']
        form.loadForm(formData)
        if form.tabs['tabGeneral'].elements['chcYesNo'].value:
            form.tabs['tabGeneral'].message('labelSessionState', 'Sessionstate content: %s'%info)
    
    def main(q,i,params,tags):
        params['SESSIONSTATE']['myMetaData'] = 'This is the metadata of the session state'
    
        form = q.gui.form.createForm()
        tab1 = form.addTab('tabGeneral','General')
        form.tabs['tabGeneral'].message('labelGeneral', 'Sessionstate sample', bold=True)
        form.tabs['tabGeneral'].addYesNo('chcYesNo','Retrieve sessionstate', trigger='change',callback='retrieve_sessionstate')
    
    def match(q,i,params,tags):
        return True

##Screenshots

![Example 1](images/pyapps//wizard_sample1.png)

![Example 2](images/pyapps/wizard_sample2.png)

![Example 3](images/pyapps/wizard_sample3.png)
