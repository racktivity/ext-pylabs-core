
from pylabs.InitBase import *
from pylabs.Shell import *

q.application.appname="filesystemwalk"

q.application.start()

    
#this is function wich will be given to walker to execute
def protectall(arg, path):
    q.console.echo("%s %s" % (arg, path))
    content=q.system.fs.fileGetContents(path)
    te=q.codetools.getTextFileEditor(path)
    te.replaceLines("",["{pyaccess.*}"])
    te.content="{pyaccess:tags=%s}\r\n%s{pyaccess}\r\n" % (arg,te.content)
    te.save()
    
#remove all guci statements, arg is the tags
startpath="guciconfluence/"
startpath="/mnt/confluence/incubaid/Global/GUCI/Home"
q.system.fswalker.walk(root=startpath,callback=protectall,recursive=True,pathRegexIncludes=[".*\.txt\\b"],arg="super")

q.application.stop()