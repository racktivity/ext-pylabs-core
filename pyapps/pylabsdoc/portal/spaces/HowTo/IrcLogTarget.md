## How to use the IRC log target

@todo needs to be checked if this code still works and where the extension is, the IrcTarget should be packages as real extension

PyLabs contains a logging framework which supports multiple log handlers. One of these handlers can be used to send all log messages to a channel on an IRC server.

Using it is very simple: you need to create a handler, register it to the logging subsystem, and start logging messages.

Here's a demo in Q-shell. First, make sure you've joined the IRC channel you're about to log to with some IRC client. We'll use the _#pmlogger_ test channel on the Freenode network in this test:

    In [1]: from pylabs.log.irc import IrcTarget
    
    In [2]: target = IrcTarget('irc.freenode.net', 6667, 'my_logger', '#pmlogger')
    
    In [3]: q.logger.addLogTarget(target)
    
    In [4]: q.logger.log('Hello IRC LogTarget world', 1)

Using the log target in a script is similar. There's one catch though: because the IRC client used to submit log messages should run next to the script, in its own thread, logging is asynchronous (your script continues to run even if the logged messages aren't actually submitted yet). Logging in to the IRC server takes some time as well. To get around this we need to add some timeouts in the script:

[[code]]
import time

from pylabs.InitBase import q
from pylabs.log.irc import IrcTarget

q.application.appname = 'irctest'
q.application.start()

target = IrcTarget('irc.freenode.net', 6667, 'my_logger', '#pmlogger')
target.maxVerbosityLevel = 4
q.logger.addLogTarget(target)

#Give the IRC client time to connect
time.sleep(5)

q.logger.log('Hello world', 3)

#Make sure all messages can be submitted
time.sleep(1)

q.application.stop()
[[/code]]

The log target code might be changed in the near future to remove the need for these sleep calls.