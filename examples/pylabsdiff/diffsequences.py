from pylabs.InitBase import *
from pylabs.Shell import *

class Dummy(object):
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.val1 == other.val1:
                return True
        return False
    def __hash__(self):
        return hash(self.val1)
    def __str__(self):
        return "%s('%s', '%s')"%(self.__class__.__name__, self.val1, self.val2)
    __repr__ = __str__

#The two sequences to be compared
seq1 = [Dummy('a', 'b'), Dummy('c', 'd'), Dummy('e', 'f')]
seq2 = [Dummy('a', 'b'), Dummy('c', 'X'), Dummy('X', 'X')]
# Defining the comparator method
def __mod__(self, other):
    if isinstance(other, self.__class__):
        return self.val2 != other.val2
    return False

comp = q.tools.diff.getSequenceMatcher(seq1,seq2,__mod__)
q.tools.diff.diffSequences(comp)
