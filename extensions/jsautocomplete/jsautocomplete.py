import pylabs
from pylabs import Pylabs
from pylabs import q, i, p
import inspect
import sys, os
from pylabs.baseclasses import BaseEnumeration

_join = q.system.fs.joinPaths

DONTSCAN = [pylabs, Pylabs, sys, os]

class JSAutoComplete(object):
    def __generate(self, name, obj, f, stack):
        try:
            if obj in stack or obj in DONTSCAN:
                return
        except:
            return
        
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            #build function arglist
            argspecs = inspect.getargspec(obj)
            arglist = list()
            for i, arg in enumerate(argspecs.args):
                if i == 0 and arg in ("self", "cls"):
                    continue
                
                arglist.append(arg)
                
            if argspecs.varargs:
                arglist.append("*%s" % argspecs.varargs)
            
            if argspecs.keywords:
                arglist.append("**%s" % argspecs.keywords)
            
            f.write("'%s(%s)',\n" % (name, ", ".join(arglist)))
            return
        
        if not isinstance(obj, (BaseEnumeration, basestring)):
            stack.append(obj)
            subobjects = dir(obj)
            subobjects.sort()
            #don't dir inside an anumerator
            for subn in subobjects:
                if subn.startswith("_") or subn.startswith("pm_"):
                    continue
                try:
                    #sometimes an extension is broken because of a missing module
                    #like the q.clients.ssh (it seems that it's not used)
                    #what we can do for now is just ignore it.
                    subobj = getattr(obj, subn)
                except:
                    continue
                
                self.__generate("%s.%s" % (name,  subn), subobj, f, stack)
        
            stack.remove(obj)
            
        f.write("'%s',\n" % name)
        
    def generate(self, objects={'q': q, 'i': i, 'p': p}, output=_join(q.dirs.baseDir, "www", "lfw", "js", "autocomp.js")):
        f = open(output, "w")
        f.write("autocompletelist = [");
        try:
            stack = list()
            for n, o in objects.iteritems():
                self.__generate(n, o, f, stack)
        finally:
            f.write("];");
            f.close()