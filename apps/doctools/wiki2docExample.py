from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.appname="setup wizardrunner"
q.application.start()

from pymonkey.Shell import *

q.qshellconfig.interactive=True
q.doctools.wiki2IntermediateFormat("wikiexamples/DCdesignBook.wiki","wikiexamples/")


