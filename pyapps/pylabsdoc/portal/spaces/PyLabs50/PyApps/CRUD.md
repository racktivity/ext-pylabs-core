[model]: /sampleapp/#/pyappsdoc/Modeling
[action]: /sampleapp/#/pyappsdoc/Action
[dirs]: /sampleapp/#/pyappsdoc/SampleApp


##CRUD Generation 

Some steps of creating a PyApp can be automated. Since all root objects of a PyApp always have some common actions, you can generate these actions. Besides these common actions you have of course to develop the other actions on a Root Object.

The common actions, always available for each Root Object, are the CRUD actions (Create, Read (getObject), Update, and Delete). A PyLabs function generates all layers required to have a new Root Object up and running with these four CRUD actions. 

This PyLabs function takes the [model][] and [action][] interfaces. Files should be located in:
 
* `/opt/qbase5/pyapps/<pyapp name>/interface/model/<pyapp domain>/<rootobject>.py`
* `/opt/qbase5/pyapps/<pyapp name>/interface/action/<pyapp domain>/<rootobject>.py`

To generate CRUD for a new Root Object, follow the following steps: 

###Generate Model

Below is a sample of a model file:  

[[code]]
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
[[/code]]

__Note__ The method \_\_str\_\_ is implemented since it is used to show a human readable representation of the object. 

###Generate Action Interface  

Below is a sample of an action interface file:

[[code]]
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
[[/code]]

[[note]]   
* Name of parameters *must* be <rootobject>guid and all attribute names should be the same as defined in the model.
* Methods that return objects, like 'getObject', should have "@execution_method = sync" in its doc string.
[[/note]]

###Auto-Generate CRUD Files

Run the following command on Q-Shell: 

[[code]]
p.core.codemanagement.api.generateCRUDImpl("sampleapp","crm","order")
[[/code]]

You can execute the `generateCRUDImpl` in three ways:
 
* Application Name only: this creates the CRUD for all domains under the `interface` folder. This action overrides __all__ CRUD written code.
* Application Name and Domain Name: This will generate all CRUD files for models under the given domain. 
* Application Name, Domain Name, and Object Name: this generates the CRUD for the given object.

After successful generation, the following files are generated for every model:

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

For more information about the file locations, see the [PyApps Directory Section][dirs].

When the code is generated, all actions are operational and can be used. However if you require more functionality to these CRUD actions, you can customize the generated code to your own needs.
Defined actions in the `actions` interface of an object, other than the CRUD actions, must be implemented manually.

###Reinstalling the Application

After generating the files, it is required to reinstall the application. Run the following command in the Q-Shell: 

[[code]]
p.application.install("sampleapp")
[[/code]]