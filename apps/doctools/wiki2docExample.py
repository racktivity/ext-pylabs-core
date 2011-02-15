from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="setup wizardrunner"
q.application.start()

from pylabs.Shell import *

q.qshellconfig.interactive=True
q.doctools.wiki2IntermediateFormat("wikiexamples/DCdesignBook.wiki","wikiexamples/")


