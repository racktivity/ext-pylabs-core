
from pylabs.baseclasses import BaseEnumeration

class ErrorconditionLevel(BaseEnumeration):
    """
    Iterrator for levels of errorconditions
    1: critical
    2: urgent
    3: error
    4: warning
    5: info
    """
    
    def __init__(self, level):
        self.level = level

    def __int__(self):
        return self.level
    
    def __cmp__(self, other):
        return cmp(int(self), int(other))


ErrorconditionLevel.registerItem('unknown', 0)
ErrorconditionLevel.registerItem('critical', 1)
ErrorconditionLevel.registerItem('urgent', 2)
ErrorconditionLevel.registerItem('error', 3)
ErrorconditionLevel.registerItem('warning', 4)
ErrorconditionLevel.registerItem('info', 5)

ErrorconditionLevel.finishItemRegistration()

