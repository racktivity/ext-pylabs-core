class pop3:
    """
    in job embedded there are all jobsteps + logging info
    """

    def create(self, server, login, password, jobguid="", executionparams=dict()):
        """
        Create a new POP3 configuration object.

        @param server:           server of the POP3 account
        @type server:            string

        @param login:            login of the POP3 account
        @type login:             string

        @param password:         password of the POP3 account
        @type password:          string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 dictionary with POP configuration object guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                  dictionary

        @raise e:                In case an error occurred, exception is raised
        """

    def find(self, server="", login="", jobguid="", executionparams=dict()):
        """
        Returns a list of POP3 configuration objects which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        @param server:           server of the POP3 account
        @type server:            string

        @param login:            login of the POP3 account
        @type login:             string
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       A list of guids as result and jobguid: {'result': [], 'jobguid': guid}
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
        
        @param rootobjectguid:   guid of the job rootobject
        @type rootobjectguid:    guid

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary

        @return:                 rootobject
        @rtype:                  rootobject

        @warning:                Only usable using the python client.
        """
        
    def delete(self, pop3guid, jobguid="",executionparams=dict()):
        """
        Delete the POP3 configuration object with the guid specified.
        
        @security: administrator
        
        @execution_method = sync
        
        @param pop3guid:                 guid of the POP3 configuration object
        @type pop3guid:                  guid
        
        @param jobguid:                  guid of the job if available else empty string
        @type jobguid:                   guid

        @param executionparams:          dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:           dictionary
        
        @return:                         dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                          dictionary

        @raise e:                        In case an error occurred, exception is raised
        """
        