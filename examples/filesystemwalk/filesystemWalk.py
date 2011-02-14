
from pymonkey.InitBase import *
from pymonkey.Shell import *

q.application.appname="filesystemwalk"

q.application.start()

def smallDirPathHandlingTest():
    print q.system.fs.getDirName(path="/opt/qbase/bin/something/test.py", levelsUp=0) #would return something
    print q.system.fs.getDirName(path="/opt/qbase/bin/something/test.py", levelsUp=1) #would return bin
    # print q.system.fs.getDirName(path="/opt/qbase/bin/something/test.py", levelsUp=10) #would raise an error

smallDirPathHandlingTest()    
    
#this is function wich will be given to walker to execute
def list(arg, path):
    q.console.echo("%s %s" % (arg, path))
    q.console.echo("Parent dirname= %s" % (q.system.fs.getDirName(path,levelsUp=1)))
    
#find all python files in rootdir not recursive
q.system.fswalker.walk(root="dirstructure",callback=list,recursive=False)    
    
#find all python files and not in .svn dirs
q.system.fswalker.walk(root="dirstructure",callback=list,pathRegexIncludes=[".*\.py\\b"],pathRegexExcludes=["\.svn"])

#find all python files from level 1 deep (not the root dir but 1 lower)    
q.system.fswalker.walk(root="dirstructure",callback=list,pathRegexIncludes=[".*\.py\\b"],pathRegexExcludes=["\.svn"],depths=[1])    
    
#find all python files which have 'kds' in content    
q.system.fswalker.walk(root="dirstructure",callback=list,pathRegexIncludes=[".*\.py\\b"],pathRegexExcludes=["\.svn"],contentRegexIncludes=["kds"],arg="This directory has kds in content:")

#find all python files which have 'kds' in content but now return as array
print q.system.fswalker.find(root="dirstructure",pathRegexIncludes=[".*\.py\\b"],pathRegexExcludes=["\.svn"],contentRegexIncludes=["kds"])

q.application.stop()