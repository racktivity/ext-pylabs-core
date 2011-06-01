from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 

 

class user(model.RootObjectModel):
 
        #@doc name of the lead
        name = model.String(thrift_id=1)

        #@doc code of the lead
        password = model.String(thrift_id=2)
        
        #@comma separated values of groups 
        groups = model.String(thrift_id=3)

