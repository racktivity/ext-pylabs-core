from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from EjabberdCommon import setRestartRequired

class EjabberdModule(CMDBSubObject):

    name = q.basetype.string(doc='name of the module', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    options = q.basetype.list(doc='list of module options', allow_none=True, default=list(), flag_dirty=True, fset=setRestartRequired)
    enabled = q.basetype.boolean(doc='flag to indicate if module is enabled', default=True, allow_none=False, flag_dirty=True,fset=setRestartRequired)

    def addOption(self, option):
        """
        Add an option
        """
        if option in self.options:
            raise ValueError('Option [%s] already exists'%option)
        self.options.append(option)
        self.dirtyProperties.add('restartRequired')

    def removeOption(self, option):
        """
        Remove option
        """
        if option not in self.options:
            raise ValueError('Option [%s] does not exist'%option)
        self.options.pop(option)
        self.dirtyProperties.add('restartRequired')

    def __str__(self):
        return ' {%s, [%s]},'%(self.name,'\n'.join('\t\t%s,'%option for option in self.options).replace("'", '"')[:-1]) if self.enabled else ''

    def __repr__(self):
        return str(self)


