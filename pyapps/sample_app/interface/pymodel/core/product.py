from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 
# @doc Product status enumeration
class productstatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('ACTIVE')
                cls.registerItem('INACTIVE')
                cls.finishItemRegistration()

# @doc Product object
class product(model.RootObjectModel):
 
        #@doc short code of this product
        code = model.String(thrift_id=1)

        #@doc description of this product
        description = model.String(thrift_id=2)

        #@doc unit price in EURO of this product
        price = model.Float(thrift_id=3)

        #@doc duration of the product. uses smart time annotation (1d = 1 day, 1w = 1 week, 1y = 1 year)
        duration = model.String(thrift_id=4)

        #@doc status of the customer
        status = model.Enumeration(productstatus,thrift_id=5)
        
        
