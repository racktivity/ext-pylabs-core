from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from EjabberdCommon import setRestartRequired

class EjabberdACL(CMDBSubObject):

    name = q.basetype.string(doc='name of the ACL', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    options = q.basetype.list(doc='list of ACL options', allow_none=False, flag_dirty=True,fset=setRestartRequired)

    def addOption(self, option):
        """
        Add an option
        """
        if option in self.options:
            raise ValueError('Option [%s] already exists'%option)
        self.options.append(option)

    def removeOption(self, option):
        """
        Remove option
        """
        if option not in self.options:
            raise ValueError('Option [%s] does not exist'%option)
        self.options.pop(option)

    def __str__(self):
        options = [ '"%s"' % option for option in self.options ]
        return '{acl, %s, {%s}}.'%(self.name, ','.join(options).replace("'", '"') )

    def __repr__(self):
        return str(self)



