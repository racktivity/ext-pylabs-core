from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 
# @doc Order status enumeration
class orderstatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('ORDERED')
                cls.registerItem('CONFIGURED')
                cls.registerItem('INVOICED')                
                cls.finishItemRegistration()

# @doc Orderline object
class orderline(model.Model):
 
        #@doc guid of the related product
        productguid = model.GUID(thrift_id=1)
 
        #@doc quantity ordered
        quantity = model.Integer(thrift_id=2)
 
# @doc Order object
class order(model.RootObjectModel):
 
        #@doc guid of the related customer
        customerguid = model.GUID(thrift_id=1)
 
        #@doc total price in EURO of this order
        price = model.Float(thrift_id=2)

		#@doc list of orderlines
        orderlines = model.List(model.Object(orderline),thrift_id=3)

        #@doc status of the customer
        status = model.Enumeration(orderstatus,thrift_id=4)
