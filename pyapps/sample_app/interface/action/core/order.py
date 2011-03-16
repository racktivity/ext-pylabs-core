class order:
    """
    Order actions API
    """
 
    def create(self, customerguid, jobguid="", executionparams=dict()):
        """
        Create a order
 
        @param customerguid:  guid of the customer placing the order
        @type customerguid: string
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the order guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def addItem(self, orderguid, productguid, quantity, jobguid="", executionparams=dict()):
        """
        Add items to an existing order
 
        @param orderguid:  guid of the order to which an item will be added
        @type orderguid: string

        @param productguid:  guid of the product to add to this order
        @type productguid: string

        @param quantity:  quantity of items to add to this order
        @type quantity: float
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def removeItem(self, orderguid, productguid, jobguid="", executionparams=dict()):
        """
        Remove items from an existing order
 
        @param orderguid:  guid of the order from which an item will be removed
        @type orderguid: string

        @param productguid:  guid of the product to remove from this order
        @type productguid: string

        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def confirm(self, orderguid, jobguid="", executionparams=dict()):
        """
        Confirms an order
 
        @param orderguid:  guid of the order to confirm
        @type orderguid: string

        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def cancel(self, orderguid, jobguid="", executionparams=dict()):
        """
        Cancels an order
 
        @param orderguid:  guid of the order to cancel
        @type orderguid: string

        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
     
    def delete(self, orderguid, jobguid="", executionparams=dict())
       """
        Delete a order
 
        @security administrators
 
        @param orderguid:  guid of the order to be deleted
        @type name: guid
        
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
 
    def find(self, customerguid="", price="", jobguid="", executionparams=dict())
        """
        Returns a list of orders which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        @param customerguid:  customerguid of the order
        @type customerguid: string
 
        @param price: price of the order
        @type price: float

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
        
      def getObject(self, orderguid, jobguid="",executionparams=dict()):
        """
        Gets the rootobject.
 
        @execution_method = sync
         
        @param orderguid:      	guid of the order
        @type orderguid:       	guid
 
        @return:                    PyModel object
        @rtype:                     Object
 
        @warning:                   Only usable using the python client.
        """
 
    def list(self, jobguid="", executionparams=dict()):
        """
        Filtered list which returns main parameters of every order in dict format
   
        @execution_method = sync
        @security administrators
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
 
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
 
        @return:                      dictionary with array of order info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'guid': '33544B07-4129-47B1-8690-B92C0DB21434',
        @note:                                           'customerguid': 'E4422BFD-E80C-405C-A780-8994AAA11905',  
        @note:                                           'price': 10,                
        @note:                                           'orderlines': [{'productguid': '031CC97E-4FA4-4329-9A29-AACA96805F65',
        @note:															 'quantity': 1'},
        @note:															{'productguid': '031CC97E-4FA4-4329-9A29-AACA96805F65',
        @note:															 'quantity': 1'}]}]}      
 
        @raise e:                     In case an error occurred, exception is raised
        """