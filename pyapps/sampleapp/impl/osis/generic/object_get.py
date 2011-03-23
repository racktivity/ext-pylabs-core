__tags__ = 'osis', 'get'
__priority__= 1 # Lowest priority 

from pymodel.serializers import ThriftSerializer
from pymodel import ROOTOBJECT_TYPES

def main(q, i, params, tags):
    domain = params['domain']
    type_ = params['rootobjecttype']
    key  = 'osis.%s.%s.%s'  % (domain, type_, params['rootobjectguid'])
    arakoonClient = q.clients.arakoon.getClient('sampleapp')
    root = arakoonClient.get(key)
    rootobject =  ThriftSerializer.deserialize(ROOTOBJECT_TYPES[domain][type_], root)
    params['rootobject'] = rootobject
    return rootobject
