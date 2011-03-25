__author__ = 'incubaid'
__tags__ ='osis', 'store'
__priority__= 3

from pymodel.serializers import ThriftSerializer

def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain']
    key  = 'osis.%s.%s.%s'  % (domain, root.PYMODEL_MODEL_INFO.name, root.guid)
    data = ThriftSerializer.serialize(root)
    arakoonClient = q.clients.arakoon.getClient(p.api.appname)
    arakoonClient.set(key, data)
