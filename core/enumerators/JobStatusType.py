
from pylabs.baseclasses import BaseEnumeration


class JobStatusType(BaseEnumeration):
    """
    Iterrator for jobstatus #@todo check
    0: unknown
    1: created
    2: waiting
    3: running
    4: done
    5: error
    """    
    def __init__(self, level):
        self.level = level

    def __int__(self):
        return self.level
    
    def __cmp__(self, other):
        return cmp(int(self), int(other))


JobStatusType.registerItem('unknown', 0)
JobStatusType.registerItem('created', 1)
JobStatusType.registerItem('scheduled', 2)
JobStatusType.registerItem('running', 3)
JobStatusType.registerItem('done', 4)
JobStatusType.registerItem('error', 5)

JobStatusType.finishItemRegistration()


