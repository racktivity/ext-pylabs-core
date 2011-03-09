from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from EjabberdCommon import setRestartRequired

class EjabberdAccessRule(CMDBSubObject):

    name = q.basetype.string(doc='name of the access rule', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    options = q.basetype.list(doc='list of access rule options', allow_none=True, default=list(), flag_dirty=True,fset=setRestartRequired)

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
        return '{access, %s, [%s]}.'%(self.name, ",".join(self.options).replace("'", '"'))

    def __repr__(self):
        return str(self)



