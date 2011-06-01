from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
 
#   
class permission(model.RootObjectModel):
 
        name = model.String(thrift_id=1)


        uri = model.String(thrift_id=2)

        