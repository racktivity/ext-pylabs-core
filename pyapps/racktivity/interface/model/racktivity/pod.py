from enumerations import *
import pymodel as model
from acl import acl
# @doc pod
class pod(model.RootObjectModel):
    
    #@doc enterprise offical name
    name = model.String(thrift_id=1)
    
    alias = model.String(thrift_id=2)

    #@doc Room where the pod is located
    room = model.GUID(thrift_id=3)
    
    #@doc Position of the corners of the pod, relative to the subobject left under corner
    position = model.List(model.List(model.Integer()), thrift_id=4)
    
    #@doc List of racks in the pod
    racks = model.List(model.GUID(), thrift_id=5)
    
    #@doc additional remarks on the pod
    description = model.String(thrift_id=6)
    
    #@doc system 
    system = model.Boolean(thrift_id=7)
    
    #@doc series of tags format
    tags = model.String(thrift_id=8)

    #@doc access control list
    acl = model.Object(acl,thrift_id=9)