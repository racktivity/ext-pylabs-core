from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
from osis import model
 
# @doc Invoice status enumeration
class invoicestatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('CREATED')
                cls.registerItem('INVOICED')
                cls.registerItem('PAID')                
                cls.finishItemRegistration()

# @doc Invoiceline object
class invoiceline(model.Model):
 
        #@doc guid of the related product
        description = model.String(thrift_id=1)
 
        #@doc quantity ordered
        amountvatexcl = model.Float(thrift_id=2)
        
# @doc Invoice object
class invoice(model.RootObjectModel):
 
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

		#@doc list of invoicelines
        invoicelines = model.List(model.Object(invoiceline),thrift_id=9)
        
        #@doc status of the customer
        status = model.Enumeration(invoicestatus,thrift_id=10)
        
        
