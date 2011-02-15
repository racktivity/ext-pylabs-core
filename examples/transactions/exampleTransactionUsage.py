

from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="transactions"

q.application.start()
q.qshellconfig.interactive=True

q.console.width=55
q.console.echo("First demonstrate how actions work")
q.transaction.start("first action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("1")
q.transaction.start("2nd action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("2")
q.logger.log("2",1) 
q.transaction.start("3e action","if an error happens show this","this error cannot resolved because is fake, but normally you can guide the user how to fix the issue")
q.console.echo("3\nmultiline example\nnext line")
q.console.echo("4 go over q.console.width, aa bb cc dd ee ff gg hh ii jj kk ll mm nn oo pp")
q.console.width=120
#raise RuntimeError("error in transaction")
q.transaction.stop()
q.transaction.stop()
q.transaction.stop()

q.console.echo( "Now we are back to normal print mode, but this does not fit on one line.")
q.logger.log("example log message will be on beginning of line",5)

#ipshell()    

q.application.stop()