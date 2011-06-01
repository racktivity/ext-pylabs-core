from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 

 
# @doc Lead object
class group(model.RootObjectModel):
 
        name = model.String(thrift_id=1)


        permissions = model.String(thrift_id=2)

