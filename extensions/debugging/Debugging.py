from pylabs import *
from pylabs.Shell import *


class Debugging:
    
    def printTraceBack(self, message = 'No message supplied'):
        q.logger.log('go exception: ' + message + '\n', 1)
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)
        q.logger.log('go exception: ' + message + '\n', 1)

    def startDebugger(self):
        import pdb
        pdb.set_trace()

    def testPrintTraceBack(self):
        try:
            t = 1/0
        except:
            self.printTraceBack('Got Exception')