

from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="exceptions"

q.application.start()
q.qshellconfig.interactive=True

def cause_error():
    e="d"
    f=5/0

def main():
    x = 33
    cause_error()

r="1"
main()

q.application.stop()