#Defining Actions Interface on Rootobjects

All actions on a Rootobject are defined as a simple class with name *RO_ClassName*

    class RO_Example:
       """
       Example Rootobject
       """

##Basic Actions
Some basic actions are defined on every Root Object:

? getObject, get the rootobject by specifying the guid
? getYaml, get the rootobject serialized as yaml file.
? getXml, get the rootobject serialized as XML file.
? getXmlSchema, get a representation in XSD of the rootobject structure
* find, find a rootobject based on the specified search parameters
* create, create a new type of the rootobject
* delete, delete the rootobject
* list, list all occurrences of the rootobject with some basic parameters

##Specification of the Attributes and Behavior

Every action should have a *jobguid(guid)* and *executionparams(dict)* defined as parameters)

Documentation should be specified for every action.
To document arguments and their types use *@argument_name* and *@type*.

    @param name:  Name of the Example
    @type name: string

The Return type can also be specified by using *@return* and *@rtype*

     @return:                      YAML representation of the Example
     @rtype:                       string


To define if a call for a action should wait until the job is fully executed there is a *@execution_method* which can be *sync* or *async*. 
By default this parameter is *async*.
Examples of *async* actions are starting a machine, moving machine. Typically *sync* actions are changing or getting information from the model.

    @execution_method = sync

Other used keywords are *@note* which can be used to give more details around a parameter or return type or *@todo* which is used when a function is specified but not yet implemented. 

You can also use self defined keywords which then can be used in the templates.

    @execution_param_wait = True

##Example

A basic root object can be:

    class RO_Example
        """
        Example Rootobject
        """
    
        def create(self, name, description="", jobguid="", executionparams=dict()):
            """
            Create a new Example Rootobject
    
            @execution_method = sync
            @security administrators
    
            @param name:  Name of the Example
            @type name: string
    
            @param description: description of the Example
            @type description: string
    
            @param jobguid: Guid of the job if available else empty string
            @type jobguid: guid
           
            @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
            @type executionparams:         dictionary
    
            @return:                       dictionary with Example as result and jobguid: {'result': guid, 'jobguid': guid}
            @rtype:                        dictionary
    
            @raise e:                      In case an error occurred, exception is raised
            """
        
        def delete(self, exampleguid, jobguid="", executionparams=dict())
           """
            Delete a Example
    
            @execution_method = sync
            @security administrators
    
            @param exampleguid:  Guid of the example to be deleted
            @type name: guid
           
            @param jobguid: Guid of the job if available else empty string
            @type jobguid: guid
           
            @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
            @type executionparams:         dictionary
    
            @return:                       dictionary with True as result and jobguid: {'result': guid, 'jobguid': guid}
            @rtype:                        dictionary
    
            @raise e:                      In case an error occurred, exception is raised
            """
    
        def find(self, name="", descripion="", jobguid="", executionparams=dict())
            """
            Returns a list of cable guids which met the find criteria.
    
            @execution_method = sync
            @security administrators
    
            @param name:  Name of the Example
            @type name: string
    
            @param description: description of the Example
            @type description: string
    
            @param jobguid: Guid of the job if available else empty string
            @type jobguid: guid
           
            @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
            @type executionparams:         dictionary
    
            @return:                       A list of Guids as result and jobguid: {'result': [], 'jobguid': guid}
            @rtype:                        list
    
            @note:                         Example return value:
            @note:                         {'result': '["FAD805F7-1F4E-4DB1-8902-F440A59270E6","C4395DA2-BE55-495A-A17E-6A25542CA398"]',
            @note:                          'jobguid':'5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
    
    
            @raise e:                      In case an error occurred, exception is raised
            """
           
          def getObject(self, rootobjectguid, jobguid="",executionparams=dict()):
            """
            Gets the rootobject.
    
            @execution_method = sync
            
            @param rootobjectguid:      Guid of the cable Example rootobject
            @type rootobjectguid:       guid
    
            @return:                    rootobject
            @rtype:                     Object
    
            @warning:                   Only usable using the python client.
            """
    
        def getYaml(self, exampleguid, jobguid="", executionparams=dict())
            """
            Gets a string representation in YAML format of the cable rootobject.
    
            @execution_method = sync
            
            @param exampleguid:           Guid of the Example rootobject
            @type exampleguid:              guid
    
            @param jobguid:               Guid of the job if avalailable else empty string
            @type jobguid:                guid
    
            @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
            @type executionparams:        dictionary
    
            @return:                      YAML representation of the Example
            @rtype:                       string
            """
    
    
    
        def getXml(self, exampleguid, jobguid="", executionparams=dict())
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
     
        def getXmlSchema(self, exampleguid, jobguid="", executionparams=dict()):
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
    
        def list(self, exampleguid="", jobguid="", executionparams=dict()):
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