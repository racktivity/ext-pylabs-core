#CRUD Generation 

CRUD Generation creates all layers required to have a new module up and running.  
It takes as input model and action interfaces. Files should be located in:
 
* /opt/qbase5/pyapps/sampleapp/interface/model/domain/rootobject.py
* /opt/qbase5/pyapps/sampleapp/interface/action/domain/rootobject.py

To generate CRUD for a new model, follow the following steps: 

##1. Generate Model

Below is a sample of a model file:  

    from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
    import pymodel as model
    
    #@doc order status enumeration
    class orderstatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
            cls.registerItem('ORDERED')
            cls.registerItem('SHIPPED')
            cls.registerItem('DELIVERED')
            cls.registerItem('WAITINGPAYMENT')                
            cls.registerItem('CLOSED')                                
            cls.finishItemRegistration()
    
    #@doc order object
    class order(model.RootObjectModel):
    
        #@doc name of the order
        name = model.String(thrift_id=1)
    
        #@doc customer of the order
        customer = model.String(thrift_id=2)
    
        #@doc status of the order
        status = model.Enumeration(orderstatus, thrift_id=4)
    
        #@doc total price of the order
        price = model.Integer(thrift_id=8)
    
    def __str__(self)
        return self.name


__N.B:__ The method \_\_str\_\_ should be implemented since it used to show a human readable representation of the object. 

##2. Generate Action Interface  

Below is a sample of an action interface file:

    class order:
	    """
	    order actions API
	    """
	    def create(self, name , customer , status, price, jobguid=None, executionparams=None):
	        """
	        @security administrators
	        """

	    def update(self, orderguid, name, customer, status, price, jobguid=None, executionparams=None):
	        """ 
	        @security administrators
	        """

	    def delete(self, orderguid, jobguid=None, executionparams=None):
	       """
	        Delete an order
	 
	        @security administrators
	        """
	 
	    def find(self, name, customer, status, price, jobguid=None, executionparams=None):
	        """
	        Returns a list of leads which met the find criteria.
	 
	        @execution_method = sync
	        @security administrators
	        """
	        
	    def getObject(self, orderguid, jobguid=None,executionparams=None):
	        """
	        Gets the rootobject.
	 
	        @execution_method = sync
	         """
	 
	    def list(self, jobguid=None, executionparams=None):
	        """
	        @execution_method = sync
	        @security administrators        
	        """

__Notes:__   
* Name of parameters *must* be <rootobject>guid and all attribute names should be the same as defined in the model.
* Methods that return objects, like 'getObject', should have "@execution_method = sync" in its doc string.

##3. Auto-Generate CRUD Files

Run the following command on Q-Shell: 

    p.core.codemanagement.api.generateCRUDImpl("sampleapp","crm","order")

__N.B:__ This method may take:
 
* The application name only: In this case it will make auto generation for all domains under the interface folder. This will override __*all*__ CRUD written code.
* Application Name & Domain Name: This will generate all CRUD files for models under the given domain. 
* Application Name, Domain Name & Model Name: This will generate CRUD for specified model.

After successfull generation, the following files will be generated for every model:

* /opt/qbase5/pyapps/sampleapp/impl/setup/osis/order\_view.py
* /opt/qbase5/pyapps/sampleapp/impl/osis/osis/store/3\_order\_store.py
* /opt/qbase5/pyapps/sampleapp/impl/osis/osis/delete/1\_order\_delete.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/create/1\_order\_create.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/delete/1\_order\_delete.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/getObject/1\_order\_getObject.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/list/1\_order\_list.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/update/1\_order\_update.py
* /opt/qbase5/pyapps/sampleapp/impl/action/crm/order/find/1\_order\_find.py
* /opt/qbase5/pyapps/sampleapp/impl/events/page\_generator/generate\_order\_page.py
* /opt/qbase5/pyapps/sampleapp/portal/spaces/crm/OrderOverview.md
* /opt/qbase5/pyapps/sampleapp/impl/ui/form/crm/order\_create/1\_order\_create.py
* /opt/qbase5/pyapps/sampleapp/impl/ui/form/crm/order\_edit/1\_order\_edit.py
* /opt/qbase5/pyapps/sampleapp/impl/ui/wizard/crm/order\_delete/1\_order\_delete.py

##4. Re-Installing the Application

After generating the files, it is required to re-install the application; run the following command in the Q-Shell: 

    p.application.install("sampleapp")
