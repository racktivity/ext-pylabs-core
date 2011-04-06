#Creating Forms and Wizards

In the PyLabs 5 framework, wizards are used to execute actions on a certain Root Object. As most of the functionality, wizards can also be defined by writing a simple tasklet.
Wizards are the way to make highly interactive windows which result in executing one or more cloudAPI calls.

Wizards should only use the cloudAPI to fetch required information and to execute actions.

The wizard dialect is fully integrated in the PyLabs framework. The main entry point to define wizards is located at 'q.gui.form'.

##General Structure of a Wizard Tasklet

Since a wizard is implemented by using the [tasklet] (http://confluence.incubaid.com/display/PYLABS/Tasklets) framework, it contains all sections like any other tasklet.

Sections:
* Tags: instruct the wizard engine which tasklets should be triggered under which circumstances.
* Author: allows you to identify who was the creator of the corresponding wizard.
* Callback method(s): see Callbacks-section for more information
* Main method: this method contains the actual implementation of the wizard
* Match method: this method is invoked before the main method is executed. The Main method is only executed if match method returns True. For wizard tasklets, the match method must always return True. Multiple implementations of the same wizard are not supported.

Example skeleton for a wizard tasklet:

    \# 'wizard' tag is required, second tag is the name of the wizard rootobject_action e.g. vdc_start
    __tags__= 'wizard','wizard_name'
    __author__='incubaid'
    
    def main(q, i, params, tags):
        cloudApi = i.config.cloudApiConnection.find('main')
    
    def match(q, i, params, tags):
        return True

The wizard tasklets are stored in the directory `<pyapp name>/impl/ui/<form/wizard>/<domain>`. See the [PyApps Directory Structure] (sampleapp.md) for more information about the location of the files.

##
