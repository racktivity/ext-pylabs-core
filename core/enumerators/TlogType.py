
from pymonkey.baseclasses import BaseEnumeration



class TlogType(BaseEnumeration):
    """
    iterator for types of events (is not same as errorconditions)
    """

    def __init__(self, level):
        self.level = level

    def __int__(self):
        return self.level
    
    def __cmp__(self, other):
        return cmp(int(self), int(other))

TlogType.registerItem('rootobject', 0)
TlogType.registerItem('roaction', 1)
TlogType.registerItem('uiaction', 2)
TlogType.registerItem('actoraction', 3)
TlogType.registerItem('monitoringinfo', 4)
TlogType.registerItem('monitoringaction', 5)
TlogType.registerItem('errorcondition', 6)
TlogType.registerItem('other', 7)
TlogType.finishItemRegistration()

