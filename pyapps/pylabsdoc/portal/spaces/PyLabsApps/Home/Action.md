@metadata title=Actions Interface
@metadata order=30
@metadata tagstring=action interface ro create

[pyappdir]: /pylabsdoc/#/PyLabsApps/Introduction


#Defining Actions Interface on Root Objects

In the previous chapter you have learned how you have to create the model of your Root Objects. Each manipulation that you want to do on a Root Object must be defined and modelled as an action. The assembly of the actions is often referred to as "interface".
For each Root Object you have to create one `.py`-file that contains the Root Object's complete interface. See the [PyApps Directory Structure][pyappdir] for more information about the location of the files.

##File Structure
The interface file of a Root Object is a Python class-file. The file contains one class with the name of the Root Object.

[[code]]
class MyRootObject:
   """
   Some documentation about this Root Object
   """
[[/code]]

Each Root Object action is defined as a method in this class.


##Basic Actions
Each Root Object has some common actions, such as:

* find: find a Root Object based on search criteria
* create: create a new Root Object
* delete: delete a Root Object
* update: update a Root Object
* list: list all occurrences of the Root Object with some basic search criteria
* getObject: get the complete Root Object

Besides these common actions, you can create your own actions, for example a specific find-action, or show a specific list of properties.


##Defining an Action
The definition of an Action is described in the docstring of the method. This docstring is the only attribute of the method.


###Documentation and Options
The first lines of the action must contain the documentation of the action and can contain some options.

[[code]]
class MyRootObject:
    """
    Some documentation about this Root Object
    """

    def create(self, arg1, arg2, arg3=None, jobguid=None, executionparams=None)
        """
        Oneliner about the function

        #optional
        @security user group
        @execution_method = sync
        """
[[/code]]

Keep the documentation of the action concise, but clear.

The optional parameters are:

* `@security`: defines which user group can execute the function, for example `@security    administrators`
* `execution_method`: by default this value is async and omitted. If the action needs to be executed in a synchronized way, you have to define this option with `sync`. When this option is activated, no other action can be started prior to the end of this action. Synchronized actions are typically updates or retrievals of objects.


###Defining the Action Arguments
In the method declaration you add the arguments and keyworded arguments. In the docstring you add the definition of the argument as follows:

    @param argX:    some explanation about the argument
    @type argX:     type of the argument

where the type of the argument are the built-in Python types, such as float, integer, string, dictionary, ...

Every action must have the arguments `jobguid` and `executionparams`. The `jobguid` is required as internal argument for the PyLabs framework. The `executionparams` is used for the workflow engine of the PyLabs framework.


###Return Values
Each action will have a return value which can be of any type. In this interface file you define what the type must be and also what the return value must look like.

    @return:    A list of guids as result and jobguid: {'result': [], 'jobguid': guid}
    @rtype:     list

The way the return value must look like is denoted with the `@note:` keyword, possibly spread over multiple lines for readability reasons. It is very important that you define the return value as clear as possible so that you know how to implement the action.

    @note:      Example return value
    @note:      {'result':'[FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
    @note:       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}


###Error and Exception Handling
You also have to define what to do in case an action does not succeed, show a warning, or raise an exception. 

    @raise e:   throw an exception in case of an error
    @warning:   only to be used with PyLabs client


###Example Interface of a Root Object
A basic root object can be:

[[code]]
class MyRootObject
    """
    Example Rootobject
    """

    def create(self, name, description=None, jobguid=None, executionparams=None):
        """
        Create a new Example Rootobject

        @execution_method = sync
        @security administrators

        @param name:            Name of the Example
        @type name:             string

        @param description:     description of the Example
        @type description:      string

        @param jobguid:         Guid of the job if available else empty string
        @type jobguid:          guid
       
        @param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:  dictionary

        @return:                dictionary with Example as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                 dictionary

        @raise e:               In case an error occurred, exception is raised
        """
    
    def delete(self, exampleguid, jobguid=None, executionparams=None)
       """
        Delete a Example

        @execution_method = sync
        @security administrators

        @param exampleguid:             Guid of the example to be deleted
        @type name:                     guid
       
        @param jobguid:                 Guid of the job if available else empty string
        @type jobguid:                  guid
       
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary

        @return:                       dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary

        @raise e:                      In case an error occurred, exception is raised
        """

    def find(self, name=None, descripion=None, jobguid=None, executionparams=None)
        """
        Returns a list of cable guids which met the find criteria.

        @execution_method = sync
        @security administrators

        @param name:                Name of the Example
        @type name:                 string

        @param description:         description of the Example
        @type description:          string

        @param jobguid:             Guid of the job if available else empty string
        @type jobguid:              guid
       
        @param executionparams:     dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:      dictionary

        @return:                    A list of Guids as result and jobguid: {'result': [], 'jobguid': guid}
        @rtype:                     list

        @note:                      Example return value:
        @note:                      {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
        @note:                       'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}


        @raise e:                   In case an error occurred, exception is raised
        """
       
      def getObject(self, rootobjectguid, jobguid=None,executionparams=None):
        """
        Gets the rootobject.

        @execution_method = sync
        
        @param rootobjectguid:      Guid of the cable Example rootobject
        @type rootobjectguid:       guid

        @return:                    rootobject
        @rtype:                     Object

        @warning:                   Only usable using the python client.
        """

    def getYaml(self, exampleguid, jobguid=None, executionparams=None)
        """
        Gets a string representation in YAML format of the cable rootobject.

        @execution_method = sync
        
        @param exampleguid:           Guid of the Example rootobject
        @type exampleguid:            guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      YAML representation of the Example
        @rtype:                       string
        """

    def getXml(self, exampleguid, jobguid=None, executionparams=None)
        """
        Gets a string representation in XML format of the cable rootobject.

        @execution_method = sync
        
        @param exampleguid:           Guid of the Example rootobject
        @type exampleguid:            guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      XML representation of the Example
        @rtype:                       string
        """
 
    def getXmlSchema(self, exampleguid, jobguid=None, executionparams=None):
        """
        Get a string representation in XSD format of the Example Rootobject
        
        @execution_method = sync
        
        @param exampleguid:           Guid of the Example rootobject
        @type exampleguid:            guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
        

        @return:                      XSD representation of the Example
        @rtype:                       string

        @todo:                        Will be implemented in phase2
        """
        raise NotImplementedError('Not implemented yet.')

    def list(self, exampleguid=None, jobguid=None, executionparams=None):
        """
        Filtered list which returns main parameters of every Example in dict format
  
        @execution_method = sync
        
        @param exampleguid:           Guid of the Example rootobject
        @type exampleguid:            guid

        @param jobguid:               Guid of the job if avalailable else empty string
        @type jobguid:                guid

        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary

        @return:                      dictionary with array of Example info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'machineguid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'name': 'MyWebServer',
        @note:                                           'description': 'My Personal Web Server'}]}

        @raise e:                     In case an error occurred, exception is raised
        """
[[/code]]

##What's Next?
In the previous chapter and this chapter you have done all the modeling work of your PyApp, design the different Root Objects and define each interface.
In a next step you will learn how to create OSIS views and the purpose of these views.
