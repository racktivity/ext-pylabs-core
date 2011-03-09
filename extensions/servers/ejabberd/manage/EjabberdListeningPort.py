from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from EjabberdCommon import setRestartRequired

class EjabberdListeningPort(CMDBSubObject):

    """
    listen: Which ports will ejabberd listen, which service handles it
    and what options to start it with
    """
    name = q.basetype.string(doc='name of the service ', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    port = q.basetype.integer(doc='port number', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    options = q.basetype.list(doc='Dictionary of module options', allow_none=True, default=list(), flag_dirty=True,fset=setRestartRequired)

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
        if option in self.options:
            self.options.pop(option)
        else:
            raise ValueError('Option [%s] does not exist'%optionname)

    def __str__(self):
        return ' {%s, %s, [\n%s\n\t]},'%(self.port, self.name, '\n'.join('\t\t%s,'%option for option in self.options).replace("'", '"')[:-1])

    def __repr__(self):
        return str(self)
