from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
from osis import model
 
# @doc Customer status enumeration
class customerstatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('ACTIVE')
                cls.registerItem('INACTIVE')
                cls.finishItemRegistration()
 
# @doc Customer object
class customer(model.RootObjectModel):
 
        #@doc name of the customer
        name = model.String(thrift_id=1)
 
        #@doc login of the customer
        login = model.String(thrift_id=2)

        #@doc password of the customer
        password = model.String(thrift_id=3)

        #@doc email address of the customer
        email = model.String(thrift_id=4)

        #@doc address of the customer
        address = model.String(thrift_id=5)

        #@doc VAT number of the customer
        vat = model.String(thrift_id=6)

        #@doc status of the customer
        status = model.Enumeration(customerstatus,thrift_id=7)
