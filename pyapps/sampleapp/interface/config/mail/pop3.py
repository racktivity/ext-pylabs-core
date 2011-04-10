from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
  
# @doc POP3 configuration object
class pop3(model.RootObjectModel):
 
        #@doc POP3 server, can be both DNS or IP address
        server = model.String(thrift_id=1)
 
        #@doc login of the POP3 account
        login = model.String(thrift_id=2)

        #@doc password of the POP3 account
        password = model.String(thrift_id=3)
