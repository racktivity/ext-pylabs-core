class lead:
    """
    Lead actions API
    """
 
    def create(self, name, code, customerguid="", source="", type="", status="", amount="", probability="", jobguid="", executionparams=dict()):
        """
        Create a lead
 
        @security administrators
 
        @param name:  name of the lead
        @type name: string
 
        @param code: login of the lead
        @type code: string

        @param customerguid: customerguid of the lead
        @type customerguid: string

        @param source: source of the lead
        @type source: string

        @param type: type of the lead
        @type type: string

        @param status: status of the lead
        @type status: string

        @param amount: amount of the lead
        @type amount: float

        @param probability: probability of the lead
        @type probability: integer
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the lead guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def update(self, name="", code="", customerguid="", source="", type="", status="", amount="", probability="", jobguid="", executionparams=dict()):
        """
        Update a lead
 
        @security administrators
 
        @param name:  name of the lead
        @type name: string
 
        @param code: login of the lead
        @type code: string

        @param customerguid: customerguid of the lead
        @type customerguid: string

        @param source: source of the lead
        @type source: string

        @param type: type of the lead
        @type type: string

        @param status: status of the lead
        @type status: string

        @param amount: amount of the lead
        @type amount: float

        @param probability: probability of the lead
        @type probability: integer
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
     
    def delete(self, leadguid, jobguid="", executionparams=dict()):
       """
        Delete a lead
 
        @security administrators
 
        @param leadguid:  guid of the lead to be deleted
        @type name: guid
        
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
 
    def find(self, name="", code="", customerguid="", source="", type="", status="", amount="", probability="", jobguid="", executionparams=dict()):
        """
        Returns a list of leads which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        @param name:  name of the lead
        @type name: string
 
        @param code: login of the lead
        @type code: string

        @param customerguid: customerguid of the lead
        @type customerguid: string

        @param source: source of the lead
        @type source: string

        @param type: type of the lead
        @type type: string

        @param status: status of the lead
        @type status: string

        @param amount: amount of the lead
        @type amount: float

        @param probability: probability of the lead
        @type probability: integer
 
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
        
    def getObject(self, leadguid, jobguid="",executionparams=dict()):
        """
        Gets the rootobject.
 
        @execution_method = sync
         
        @param leadguid:      	guid of the lead
        @type leadguid:       	guid
 
        @return:                    PyModel object
        @rtype:                     Object
 
        @warning:                   Only usable using the python client.
        """
 
    def list(self, jobguid="", executionparams=dict()):
        """
        Filtered list which returns main parameters of every lead in dict format
   
        @execution_method = sync
        @security administrators
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
 
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
 
        @return:                      dictionary with array of lead info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'guid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'name': 'Steve Jobs',
        @note:                                           'code': 'LEAD_APPLE',        
        @note:                                           'customerguid': '33644B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'source': 'COLDCALL',
        @note:                                           'type': 'NEWBUSINESS',
        @note:                                           'status': 'PROSPECTING',
        @note:                                           'amount': 100000,        
        @note:                                           'probability': 50}]}      
        @raise e:                     In case an error occurred, exception is raised
        """