class product:
    """
    Product actions API
    """
 
    def create(self, code, description, price, duration, jobguid="", executionparams=dict()):
        """
        Create a product
 
        @security administrators
 
        @param code:  code of the product
        @type code: string
 
        @param description: description of the product
        @type description: string

        @param price: price of the product
        @type price: float

        @param duration: duration of the product
        @type duration: string

        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the product guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
     
    def delete(self, productguid, jobguid="", executionparams=dict())
       """
        Delete a product
 
        @security administrators
 
        @param productguid:  guid of the product to be deleted
        @type name: guid
        
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
 
    def find(self, code="", description="", price="", duration="", jobguid="", executionparams=dict())
        """
        Returns a list of products which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        @param code:  code of the product
        @type code: string
 
        @param description: description of the product
        @type description: string

        @param price: price of the product
        @type price: float

        @param duration: duration of the product
        @type duration: string
 
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
        
      def getObject(self, productguid, jobguid="",executionparams=dict()):
        """
        Gets the rootobject.
 
        @execution_method = sync
         
        @param productguid:      	guid of the product
        @type productguid:       	guid
 
        @return:                    PyModel object
        @rtype:                     Object
 
        @warning:                   Only usable using the python client.
        """
 
    def list(self, jobguid="", executionparams=dict()):
        """
        Filtered list which returns main parameters of every product in dict format
   
        @execution_method = sync
        @security administrators
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
 
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
 
        @return:                      dictionary with array of product info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'guid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'code': 'VMWIN2K8_16GB_250GB',
        @note:                                           'description': 'Windows 2008 Server / 16GB RAM / 250GB storage',        
        @note:                                           'price': 10,                
        @note:                                           'duration': '1y'}]}      
 
        @raise e:                     In case an error occurred, exception is raised
        """