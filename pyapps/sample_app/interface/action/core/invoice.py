class invoice:
    """
    Invoice actions API
    """
 
    def create(self, orderguid, jobguid="", executionparams=dict()):
        """
        Create a invoice
 
        @param orderguid:  guid of the order for which an invoice will be created
        @type orderguid: string
 
        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the invoice guid as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """

    def renew(self, invoiceguid, jobguid="", executionparams=dict()):
        """
        Renews an invoice
 
        @param invoiceguid:  guid of the invoice to confirm
        @type invoiceguid: string

        @param jobguid: guid of the job if available else empty string
        @type jobguid: guid
        
        @param executionparams:        dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:         dictionary
 
        @return:                       dictionary with the guid of the new invoice as result and jobguid: {'result': guid, 'jobguid': guid}
        @rtype:                        dictionary
 
        @raise e:                      In case an error occurred, exception is raised
        """
      
    def find(self, customerguid="", orderguid="", code="", description="", amountvatexcl="", amountvatincl="", vatpercentage="", invoicedate="", jobguid="", executionparams=dict())
        """
        Returns a list of invoices which met the find criteria.
 
        @execution_method = sync
        @security administrators
 
        #@doc guid of the related customer
        customerguid = model.GUID(thrift_id=1)

        #@doc guid of the related order
        orderguid = model.GUID(thrift_id=2)

        #@doc short code of this invoice
        code = model.String(thrift_id=3)

        #@doc description of this invoice
        description = model.String(thrift_id=4)

        #@doc amount VAT exclusive in EURO of this invoice
        amountvatexcl = model.Float(thrift_id=5)

        #@doc amount VAT inclusive in EURO of this invoice
        amountvatincl = model.Float(thrift_id=6)

        #@doc VAT percentage of this invoice
        vatpercentage = model.Float(thrift_id=7)

        #@doc date of this invoice
        invoicedate = model.DateTime(thrift_id=8)

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
        
      def getObject(self, invoiceguid, jobguid="",executionparams=dict()):
        """
        Gets the rootobject.
 
        @execution_method = sync
         
        @param invoiceguid:      	guid of the invoice
        @type invoiceguid:       	guid
 
        @return:                    PyModel object
        @rtype:                     Object
 
        @warning:                   Only usable using the python client.
        """
 
    def list(self, jobguid="", executionparams=dict()):
        """
        Filtered list which returns main parameters of every invoice in dict format
   
        @execution_method = sync
        @security administrators
        
        @param jobguid:               guid of the job if avalailable else empty string
        @type jobguid:                guid
 
        @param executionparams:       dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:        dictionary
 
        @return:                      dictionary with array of invoice info as result and jobguid: {'result': array, 'jobguid': guid}
        @rtype:                       dictionary
        @note:                              {'jobguid': '22544B07-4129-47B1-8690-B92C0DB21434',
        @note:                               'result: [{ 'guid': '33544B07-4129-47B1-8690-B92C0DB21434',
												         'orderguid': 'B41F4CD9-C767-4047-8C26-D08A08E02BBA',  
        @note:                                           'customerguid': 'E4422BFD-E80C-405C-A780-8994AAA11905',  
        @note:                                           'code': 'INV-2011-0000001',          
        @note:                                           'description': 'Invoice description',                  
        @note:                                           'amountvatexcl': 10,                          
        @note:                                           'amountvatincl': 12.1,                                  
        @note:                                           'vatpercentage': 21,          
        @note:                                           'invoicedate': '2011-01-01',                  
        @note:                                           'invoicelines': [{'description': 'Windows 2008 Server 16GB / 250GB / 12 months',
        @note:															 'amountvatexcl': 10'}}]}]}      
 
        @raise e:                     In case an error occurred, exception is raised
        """