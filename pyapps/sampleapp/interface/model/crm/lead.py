from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 

# @doc Lead status enumeration
class leadstatus(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('PROSPECTING')
                cls.registerItem('VALUEPROPOSITION')
                cls.registerItem('CLOSEDWON')                
                cls.registerItem('CLOSEDLOST')                                
                cls.finishItemRegistration()

# @doc Lead type enumeration
class leadtype(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('EXISTINGBUSINESS')
                cls.registerItem('NEWBUSINESS')
                cls.finishItemRegistration()

# @doc Lead source enumeration
class leadsource(BaseEnumeration):
        @classmethod
        def _initItems(cls):
                cls.registerItem('COLDCALL')
                cls.registerItem('PARTNER')
                cls.registerItem('TRADESHOW')                
                cls.finishItemRegistration()
 
# @doc Lead object
class lead(model.RootObjectModel):
 
        #@doc name of the lead
        name = model.String(thrift_id=1)

        #@doc code of the lead
        code = model.String(thrift_id=2)

        #@doc guid of the customer in case the lead is related to an existing customer
        customerguid = model.GUID(thrift_id=3)

        #@doc source of the lead
        source = model.Enumeration(leadsource,thrift_id=4)

        #@doc type of the lead
        type = model.Enumeration(leadtype,thrift_id=5)
 
        #@doc status of the lead
        status = model.Enumeration(leadstatus,thrift_id=6)

        #@doc amount of the lead
        amount = model.Float(thrift_id=7)

        #@doc probability in % of the lead
        probability = model.Integer(thrift_id=8)

