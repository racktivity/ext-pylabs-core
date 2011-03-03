
from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="suggarsync"

q.application.start()

from  SugarsyncClient import SugarsyncClient

sc=SugarsyncClient()
sc.login()
sc.getFolderContents("/")

ipshell()

q.application.stop()
