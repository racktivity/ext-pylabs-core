from pylabs.InitBase import q,i
from xml.dom.minidom import parse, parseString
from Cheetah.Template import Template

from epydoc.docbuilder import build_doc, build_doc_index
from epydoc.docparser import parse_docs
from epydoc.docintrospecter import introspect_docs
from epydoc.apidoc import ClassDoc, RoutineDoc
from epydoc.markup import ParsedDocstring


import re
import imp
import inspect

def getClass(filePath, className=""):
    module =  imp.load_source(filePath, filePath)
    if className:
        claZ = getattr(module, className)
    else:
        for att in dir(module):
            cl = getattr(module, att)
            if inspect.isclass(cl):
                claZ = cl
    return claZ

def listMethods(claZ):
    methods = dict()
    for att in  dir(claZ):
        if att.startswith('_') or att.startswith('pm'):
            continue
        method = getattr(claZ, att)
        if inspect.ismethod(method):
            methods[att] = method
    return methods

class Extension:
    def __init__(self, className, moduleName, qlocation):
        self.className = className
        self.moduleName = moduleName
        self.qlocation = qlocation

class Method:
    def __init__(self, name, args, docs, params=dict(), argNames=list(), argClasses=None):
        self.args = args
        self.name = name
        self.docs = docs
        self.params = params
        self.argNames = argNames
        self.argClasses = argClasses

class Argument:
    def __init__(self, name, value='', argtype='', hasdefault=True):
        self.name = name
        self.value = value
        self.argtype = argtype
        self.hasdefault=hasdefault

    def __str__(self):
        return '%s = %s'%(self.name, self.value if not self.value=="" and not isinstance(self.value, basestring) else '"%s"'%self.value) if self.hasdefault else '%s'%self.name

    def __repr__(self):
        return str(self)


def getArguments(args, defaults):
    arguments = list()
    length = 0
    if defaults:
        length = len(defaults)
    argList = args[-length:]

    for index, arg in enumerate(args):
        if arg == 'self':
            continue
        argument = Argument(arg, defaults[argList.index(arg)]) if defaults and arg in argList else Argument(arg, hasdefault=False)
        arguments.append(argument)

    return arguments

def getMethodProperties(method):
    args, varargs, varkw, defaults = inspect.getargspec(method)
    arguments = getArguments(args, defaults)
    params = dict()
    for arg in arguments:
        if arg.name in ('jobguid','executionparams'):
            continue
        params[arg.name] = arg.name
    return arguments, params

def getMethod(method, methodName):
    arguments, params = getMethodProperties(method)
    args = ', '.join([str(arg) for arg in arguments])
    argsNames = [arg.name for arg in arguments]
    doc = method.__doc__
    method = Method(methodName, args, doc, params, argsNames, arguments)
    return method


def getClassMethods(specFile, className):
    claZ = getClass(specFile, className)
    methods = list()
    for funcName, func in listMethods(claZ).iteritems():
        method = getMethod(func, funcName)
        methods.append(method)
    #methods.sort(lambda x,y:cmp(x.name,y.name))
    return methods

def getClassName(claZ):
    pattern = re.compile('ro_', re.IGNORECASE)
    name = pattern.split(claZ.__name__)[-1]
    return name.lower()


def getMethodTypedArgument(specFile):
    val_doc = parse_docs(specFile)
    doc = build_doc(specFile)
    moduledoc = introspect_docs(filename=specFile)
    methodDetails = dict()
    for ckey in moduledoc.variables.iterkeys():
        classdoc = moduledoc.variables[ckey].value
        for rkey in classdoc.variables.iterkeys():
            routinedoc = classdoc.variables[rkey].value
            if isinstance(routinedoc, RoutineDoc):
                argType=dict()
                for arg in routinedoc.arg_types.iterkeys():
                    argument = str(routinedoc.arg_types[arg])
                    paramType = re.findall('<epytext><para inline=True>(?P<paramtype>.*)</para></epytext>', argument)[0]
                    argType[arg] = paramType
                methodDetails[rkey] = argType
    return methodDetails

def generateCode(templatePath, params, destPath):
    template = Template(q.system.fs.fileGetContents(templatePath), params)
    contents = str(template)
    q.system.fs.writeFile(destPath, contents)

def generateClientCode(specFile, serviceName, templatePath, destPath, className =""):
    claZ = getClass(specFile, className)
    methods = getClassMethods(specFile, className)
    typedArgs = getMethodTypedArgument(specFile)
    for method in methods:
        for arg in method.argClasses:
            if typedArgs.has_key(method.name) and typedArgs[method.name].has_key(arg.name):
                arg.argtype = typedArgs[method.name][arg.name]

    name = getClassName(claZ)
    generateCode(templatePath, {'className': name, 'methods':methods, 'serviceName':serviceName}, destPath)
    return name

def generateServerCode(specFile, templatePath, destPath, serverExtensionTemplate="", serverExtensionDest="",rootobjectslibDest="", rootobjectlibTemplate="", className="", wizards=True):
    claZ = getClass(specFile, className)
    methods = getClassMethods(specFile, className)
    name = getClassName(claZ)
    generateCode(templatePath,  {'className': name, 'methods':methods}, destPath)

    if serverExtensionDest and serverExtensionTemplate:
        generateCode(serverExtensionTemplate,  {'className': name, 'methods':methods}, serverExtensionDest)
        generateCode(rootobjectlibTemplate, {'className':name, 'methods':methods}, rootobjectslibDest)

    taskletsDir = q.system.fs.joinPaths(q.system.fs.getDirName(destPath), 'tasklets', str(name))
    if q.system.fs.exists(taskletsDir):
        q.system.fs.removeDirTree(taskletsDir)
    q.system.fs.createDir(taskletsDir)
    generateTasklets(str(name), methods, taskletsDir)
       
    return name

def generateTasklets(rootobject, listOfMethods, outputDir, template=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','tasklets.tmpl')):
    for method in listOfMethods:
        tasklets = q.system.fs.joinPaths(outputDir, method.name)
        q.system.fs.createDir(tasklets)
        generateCode(template, {'rootobject':rootobject, 'methodName':method.name}, q.system.fs.joinPaths(tasklets, '%s_%s.py'%(rootobject, method.name)))

services = dict()
def generatePythonRoot(clientTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','template.tmpl'), serverTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','servertemplate.tmpl'),\
                       specDir = q.system.fs.joinPaths('/root', 'ssospecs', '1.1', 'codepackages', 'Actions_Interface_Rootobject'), clientOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedClient'),\
                       serverOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer'), serverExtensionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'serverextensiontemplate.tmpl'),\
                       serverExtensionDest=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer','extensions'),extensionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'extensionTemplate.tmpl'),
                       cloudapiqconfig=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'connectionTemplate.tmpl'), cloudapiClientsTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiclientsTemplate.tmpl'),\
                       serviceTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','servicestemplate.tmpl'), exceptionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','exception.tmpl'),\
                       rootobjectslibDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer','cloud_api_rootobjects'), rootobjectlibTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','serverrootobjectlib.tmpl')):


    q.system.fs.createDir(clientOutputDir)
    q.system.fs.createDir(serverOutputDir)
    q.system.fs.createDir(serverExtensionDest)
    q.system.fs.createDir(rootobjectslibDir)
    modules = dict()
    extensions = list()
    ##generate root object actions
    for spec in q.system.fs.listFilesInDir(specDir, filter='*.py'):
        fileName = q.system.fs.getBaseName(spec)
        if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
            continue
        rootObject = fileName.split('.')[0].split('ro_')[-1]
        className = generateClientCode(spec, 'cloud_api_%s'%rootObject,clientTemplate, q.system.fs.joinPaths(clientOutputDir, 'client_%s.py'%rootObject))
        services['cloud_api_%s'%rootObject] = 'cloud_api.%s.%s'%(rootObject, className)

        className = generateServerCode(spec,serverTemplate, q.system.fs.joinPaths(serverOutputDir, '%s.py'%rootObject), serverExtensionTemplate, \
                                       q.system.fs.joinPaths(serverExtensionDest, '%s.py'%rootObject), q.system.fs.joinPaths(rootobjectslibDir, 'cloud_api_%s.py'%rootObject), rootobjectlibTemplate)
        modules['client_%s'%rootObject] = className
        extensions.append(Extension(className, className, 'q.actions.rootobject.%s'%className))

    generateCode(extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(serverExtensionDest, 'extension.cfg'))
    extensions = list()
    generateCode(serviceTemplate, {'services':services},  q.system.fs.joinPaths(serverOutputDir, 'applicationserverservice.cfg'))
    ####
    generateCode(exceptionTemplate, {}, q.system.fs.joinPaths(clientOutputDir, 'Exceptions.py'))
    extensions.append(Extension('CloudApiConnectionsConfig', 'cloud_api_connections', 'i.config.cloudApiConnection'))
    generateCode(extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(clientOutputDir, 'extension.cfg'))
    generateCode(cloudapiClientsTemplate, {'modules':modules}, q.system.fs.joinPaths(clientOutputDir, 'cloud_api_clients.py'))

    generateCode(cloudapiqconfig, {}, q.system.fs.joinPaths(clientOutputDir, 'cloud_api_connections.py'))

def generatePythonActor(template=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','actortemplate.tmpl'), specDir = q.system.fs.joinPaths('/root', 'ssospecs', '1.1', 'codepackages', 'Actions_Interface_Actor'),\
                        outputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'actor'), extensionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','extensionTemplate.tmpl')):
    ##generate actor actions
    q.system.fs.createDir(outputDir)
    extensions = list()
    for spec in q.system.fs.listFilesInDir(specDir, filter='*.py'):
        fileName = q.system.fs.getBaseName(spec)
        if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
            continue
        moduleName =  fileName.split('.')[0]
        rootObject = fileName.split('.')[0].split('ro_')[-1]

        className = generateServerCode(spec,template, q.system.fs.joinPaths(outputDir, fileName), wizards=False)

        #modules['client_ro_%s'%rootObject] = className/
        extensions.append(Extension(className, moduleName, 'q.actions.actor.%s'%moduleName))
    ##
    generateCode(extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(outputDir, 'extension.cfg'))


def generateFlexRoot(clientTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiFlexClient.tmpl'), \
                     specDir = q.system.fs.joinPaths('/root', 'ssospecs', '1.1', 'codepackages', 'Actions_Interface_Rootobject'), \
                     clientOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedFlexClient'), \
                     clientServiceTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiFlexclientService.tmpl'), flexServiceFileName='CloudApiRestService.as'):

    q.system.fs.createDir(clientOutputDir)
    modules = dict()
    extensions = list()
    ##generate root object actions
    for spec in q.system.fs.listFilesInDir(specDir, filter='*.py'):
        fileName = q.system.fs.getBaseName(spec)
        if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
            continue
        rootObject = fileName.split('.')[0].split('ro_')[-1]
        className = generateClientCode(spec, 'cloud_api_%s'%rootObject,clientTemplate, q.system.fs.joinPaths(clientOutputDir, '%s.as'%rootObject.capitalize()))

    generateCode(clientServiceTemplate, {}, q.system.fs.joinPaths(clientOutputDir, flexServiceFileName))

generatePythonRoot()
generateFlexRoot()
generatePythonActor()
##generate flex amf client
generateFlexRoot(clientTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','flexclient.tmpl'), \
                 clientOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedFlexAMFClient'), \
                 clientServiceTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','flexamfservice.tmpl'), \
                 flexServiceFileName='CloudApiAMFService.as')

