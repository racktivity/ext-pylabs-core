from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.appname = "testApp"
q.application.start()

#installing the required qpackages
i.qpackages.findFirst("scribe*").install() # this will install fb303, thrift, libboost, libevent
i.qpackages.findFirst("pylabs_logclient").install()
i.qpackages.findFirst("pylabs_logserver").install()

#before testing the logging scenario we should start the log console in another qshell session with: q.logger.console.start(), so that we can connect to it from here
ipshell()


q.logger.log("testing log") 
# this will appear in the log console as following:
#{'level': '5', 'timestamp': '1257849213.29', 'tags': '', 'source': 'qshell', 'message': 'hello there', 'type': 1}

q.eventhandler.raiseCritical('very critical, i can not ping my network service','n5')
# this will appear in the log console as following:
#File "/opt/qbase3/utils/shell.py", line 125, in <module>
#    main()
#  File "/opt/qbase3/utils/shell.py", line 115, in main
#    Shell(debug=options.debug, ns=ns)()
#  File "/opt/qbase3/lib/pymonkey/core/pymonkey/Shell.py", line 703, in __call__
#    myshell(*args, **kwargs)
#
#*************************
#n5
#*************************
#very critical, i can not ping my network service

q.logger.console.disableEvents() # this will disable any event from being displayed in the log console
q.eventhandler.raiseCritical('very critical, i can not ping my network service','n5') # having no effect , because we disabled the events.

q.logger.console.enableEvents()

# this will print all the shown tags in the last five minutes
q.logger.console.showFoundTags(5)


# testing filtering based on the log level
q.logger.console.setMinLevel(5)
q.logger.log("i'm under the minimum level", 2) # this should not be displayed at the log console
q.logger.console.setMinLevel(0) # return to default 


# testing getting the last used source applications in the last five minutes
q.logger.console.showSourceApplications(5)

# testing filtering based on the source application
q.logger.console.filterSourceApplications(['qshells',])
q.logger.log("this will be filtered out because its source is qshell no qshells")
q.logger.log("this will be appeared", source="qshells")



q.application.stop()

