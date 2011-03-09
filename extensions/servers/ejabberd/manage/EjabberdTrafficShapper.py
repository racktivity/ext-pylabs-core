from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject
from EjabberdCommon import setRestartRequired

class EjabberdTrafficShaper(CMDBSubObject):

    name = q.basetype.string(doc='name of the traffic shaper', allow_none=False, flag_dirty=True,fset=setRestartRequired)
    options = q.basetype.list(doc='Shaper kinds', allow_none=False, flag_dirty=True,fset=setRestartRequired)

    def addOption(self, name, value):
        if name in self.options:
            raise ValueError('Option with name [%s] already exists')
        self.options[name] = value

    def removeOption(self, name):
        if name not in self.options:
            raise ValueError('Option with name [%s] does not exist')
        del self.options[na]

    def __str__(self):
        return '{shaper, %s, {%s}}.'%(self.name, ','.join(self.options))

    def __repr__(self):
        return str(self)



