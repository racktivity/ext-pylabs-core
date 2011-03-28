from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
  
# @doc POP3 configuration object
class eventqueue(model.RootObjectModel):
 
        #@doc name of the event queue
        name = model.String(thrift_id=1)
 
        #@doc number of events on the queue
        numberofevents = model.Integer(thrift_id=2)

