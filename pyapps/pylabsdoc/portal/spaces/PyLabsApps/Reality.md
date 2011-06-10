[imgPyAppArch]: images/images50/pyapps/PyApp_Architecture.png
[model]: /pylabsdoc/#/PyLabsApp/Modeling
[actions]: /pylabsdoc/#/PyLabsApp/Action
[osisview]: /pylabsdoc/#/PyLabsApp/OsisViews
[osisoperations]: /pylabsdoc/#/PyLabsApp/OsisOperations
[actiontasklet]: /pylabsdoc/#/PyLabsApp/ActionTasklet
[pyappdir]: /pylabsdoc/#/PyLabsApp/Sampleapp
[SAL]: /pylabsdoc/#/PyLabs50/Architecture



#From DRP to Reality
The PyLabs framework is not limited to creating objects in the DRP, creating views on Root Objects, or creating wizards and forms. PyLabs gives you also the possibility to interact with the reality, for example sending e-mails.

If you take a look at the architecture schema of a PyApp, we have focused so far on the  DRP, Actions, and the UI wizards sections. In this section we will focus on the interaction between the PyLabs framework and the reality. The reality can be of any kind. Besides the given reality example, e-mail, the reality can also be manipulations of servers, configuration of systems, ...

![PyApp_Architecture][imgPyAppArch]

Just like other Root Objects, you can consider the mail server as a Root Object. Therefore, the creation of the mail server and its functions takes the same steps as the other Root Objects:

1. [Modeling the Mail Server][model]: define the model of the POP3 server, such as IP address, login, and password
2. [Define the Actions on the POP3 Server][actions]: define the different methods on the POP3 server, such as creating a POP3 configuration
3. [Create OSIS View on the POP3 Server][osisview]
4. [Create OSIS Operations on the POP3 Server][osisoperations]
5. [Implement the POP3 Server Configuration Actions][actiontasklet]

The POP3 Server configuration does not need a form nor wizard, since this should be a one time only action. 
By executing the five steps above, you are able to configure a POP3 server for your sample application.

By configuring a mail server, you are able to interact with the reality, for example sending and retrieving mails.


##Overview
To interact with the reality, you have to define the "Actor Actions" and create "RScripts".

In the Action layer you define the different actions that are available on the different objects. An action must be executed by an actor; this is defined in the "Actor Action" layer. The defined actor is still an abstract definition, for example hypervisor or a mailprocessor. Therefore the actor is defined in the `interface` section of your PyApp.

One level further to the reality, you must implement the actor interface. In this implementation you define the actual actor. The actor provides an RScript to an agent who does the actual action in the reality.


##Actor Actions
In the actor interface, you define the actions that the actor can execute. In case your PyApp needs to send out mails, you will need an actor who can execute this action.
In the given example you can define the action `sendMail`. The definition is similar to defining the [actions on Root Objects][actions].

The interface definition is located in `<pyapp name>/interface/actor/<domain>`. See the [PyApps Directory Structure][pyappdir] for more information about the location of the files. The interface contains one class with the name of the actor.

[[code]]
class mailprocessor:
    """
    Mail processor actions API
    """
[[/code]]    

This class contains the different actions that the actor can execute. In this example we will only provide an action that can send out mails.

[[code]]
def sendMail(self, sender, replyto, to, subject, message, cc="", bcc="", jobguid="", executionparams=None):
    """
    Create a mailprocessor

    @param sender:  sender address for the email
    @type sender: string

    @param replyto:  replyto address for the email
    @type replyto: string
 
    @param to:  to address for the email
    @type to: string

    @param subject: subject for the email
    @type subject: string

    @param message: message body for the email
    @type message: string

    @param cc:  cc address for the email
    @type cc: string

    @param bcc: bcc address for the email
    @type bcc: string
 
    @param jobguid: guid of the job if available else empty string
    @type jobguid: guid
        
    @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
    @type executionparams:         dictionary
 
    @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
    @rtype:                        dictionary
 
    @raise e:                      In case an error occurred, exception is raised
    """
[[/code]]    


##Implementation of an Actor Action
The implementation of the actor action is creating a tasklet. The tasklet is located in `<pyapp name>/impl/actor/<domain>/<actor name>/<action name>`. See the [PyApps Directory Structure](/sampleapp/#/pyappsdoc/sampleapp) for more information about the location of the files. The file name of an action tasklet has always the following structure:

`<priority>_<rootobject>_<action>.py`

See the [Action Tasklets](actiontasklet) section for more information about the file name.

The tasklet does nothing more than providing an actor and RScript the the workflow engine of PyLabs. The proper agent in the framework will pick up the action and execute the RScript. The RScript is the actual execution in the reality.
The RScript must be located in a sub-directory of the actor action tasklet.


###Actor Action
The `main` function of the tasklet must contain at least the command `q.workflowengine.agentcontroller.executeActorActionScript()` including a couple of arguments.
The following arguments are required for the `executeActorActionScript` command:

* agentguid: guid of the agent who must execute the RScript
* scriptname: name of the RScript, without extension
* params: a dictionary of parameters, in this situation this is the `params` dictionary provided by the PyLabs framework
* executionparams: extra dictionary with parameters, specific for the execution of the RScript.

For example:

[[code]]
params['result'] = q.workflowengine.agentcontroller.executeActorActionScript(agentguid       = 'agent1', 
                                                                             scriptname      = 'sendMail', 
                                                                             params          = params, 
                                                                             executionparams = {"maxduration": 30, "description": "Sending welcome mail to customer"})['result']
[[/code]]                                                                             


###RScript
The RScript contains the actual code that will execute something in reality. Just like tasklets, the RScript also receives the `params` dictionary, containing the key/value combinations as gathered in the tasklet, which calls the RScript.

The file name of an RScript must have the following structure:
    <action>.rscript

The action is the name of the method as defined in the interface file. 

Besides the PyLabs system abstraction layer ([SAL][]), the RScript can also make use of standard Python libraries. If the RScript needs standard Python libraries, you have to import them into the RScript. The PyLabs libraries are all available without importing.

[[code]]
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart('alternative')
msg['Subject'] = params['subject']
msg['From'] = params['replyto']
msg['To'] = params['to']
msg.attach(MIMEText(params['message'], 'plain'))

q.logger.log('Set SMTP server')    
server = smtplib.SMTP('relay.aserver.com')
server.sendmail(params['replyto'], params['to'], msg.as_string())
params['result'] = True
[[/code]]
