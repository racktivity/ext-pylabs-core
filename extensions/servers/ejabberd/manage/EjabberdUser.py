from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class EjabberdUser(CMDBSubObject):

    name = q.basetype.string(doc='name of the user', allow_none=False)
    password = q.basetype.string(doc='password of the user', allow_none=False)
    server = q.basetype.string(doc='server where the user belongs', allow_none=False)
    _removed = q.basetype.boolean(doc='Flag to determine if the user was removed', allow_none=False, default=False)

    def __str__(self):
        return 'EJabberdUser: %s@%s'%(self.name, self.server)

    def __repr__(self):
        return str(self)
    

