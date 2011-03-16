class customer:
    """
    Customer actions API
    """
 
    def create(self, name, login, password, email, address="", vat="", jobguid="", executionparams=dict()):
        """
        Create a customer
 
        @security administrators
 
        @param name:  name of the customer
        @type name: string
 
        @param login: login of the customer
        @type login: string

        @param password: password of the customer
        @type password: string

        @param email: email of the customer
        @type email: string

        @param address: address of the customer
        @type address: string

        @param vat: vat of the customer
        @type vat: string
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the customer guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
     
    def delete(self, customerguid, jobguid="", executionparams=dict())
       """
        Delete a customer
 
        @security administrators
 
        @param customerguid:  guid of the customer to be deleted
        @type name: guid
        
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
 
    def find(self, name="", login="", email="", address="", vat="", jobguid="", executionparams=dict())
        """
        Returns a list of customers which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        @param name:  name of the customer
        @type name: string
 
        @param login: login of the customer
        @type login: string

        @param email: email of the customer
        @type email: string

        @param address: address of the customer
        @type address: string

        @param vat: vat of the customer
        @type vat: string
 
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
        
      def getObject(self, customerguid, jobguid="",executionparams=dict()):
        """
        Gets the rootobject.
 
        @execution_method = sync
         
        @param customerguid:      	guid of the customer
        @type customerguid:       	guid
 
        @return:                    PyModel object
        @rtype:                     Object
 
        @warning:                   Only usable using the python client.
        """
 
    def list(self, jobguid="", executionparams=dict()):
        """
        Filtered list which returns main parameters of every customer in dict format
   
        @execution_method = sync
        @security administrators
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
 
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
 
        @return:                      dictionary with array of customer info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'guid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'name': 'Steve Jobs',
        @note:                                           'login': 'jobss',        
        @note:                                           'address': 'Apple Avenue',                
        @note:                                           'vat': 'BE 000.000.000'}]}      
 
        @raise e:                     In case an error occurred, exception is raised
        """