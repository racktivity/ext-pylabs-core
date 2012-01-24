from pylabs import q, p
from Cheetah.Template import Template

from epydoc.markup import epytext

import pymodel as model

import os
import re
import imp
try:
    import pydot
except ImportError:
    pydot = None
import inspect
import itertools

wfe_amqp = False

try:
    from workflowengine import amqp
    wfe_amqp = True
except:
    pass

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

def getTypeConverter(pymodelType):
    typeMapping = dict()
    typeMapping['String'] = "str"
    typeMapping['Object'] = 'str'
    typeMapping['Boolean'] = 'str'
    typeMapping['DateTime'] = 'str'
    typeMapping['Float'] = 'float'
    typeMapping['Integer'] = 'int'
    typeMapping['GUID'] = 'str'
    typeMapping['Enumeration'] = 'str'
    typeMapping['Dict'] = 'eval'
    typeMapping['List'] = 'eval'

    return typeMapping[pymodelType]



def getUIType(pymodelType):
    typeMapping = dict()
    typeMapping['String'] = "Text"
    typeMapping['Object'] = 'Text'
    typeMapping['Boolean'] = 'YesNo'
    typeMapping['DateTime'] = 'DateTime'
    typeMapping['Float'] = 'Integer'
    typeMapping['Integer'] = 'Integer'
    typeMapping['GUID'] = 'Text'
    typeMapping['Enumeration'] = 'Choice'
    typeMapping['Dict'] = 'Text'
    typeMapping['List'] = 'Text'

    return typeMapping[pymodelType]


def getOsisType(pymodelType):
    typeMapping = dict()
    typeMapping['String'] = "STRING"
    typeMapping['Object'] = 'BINARY'
    typeMapping['Boolean'] = 'BOOLEAN'
    typeMapping['DateTime'] = 'DATETIME'
    typeMapping['Float'] = 'FLOAT'
    typeMapping['Integer'] = 'INTEGER'
    typeMapping['GUID'] = 'UUID'
    typeMapping['Enumeration'] = 'STRING'
    typeMapping['Dict'] = 'STRING'
    typeMapping['List'] = 'STRING'

    return typeMapping[pymodelType]

    #these types needs to review their mapping , is that possble to get these types in the model specs?
    #model.Model

        #model.Dict
        #model.Enumeration
        #model.List

        #typeMapping['']='TEXT'
        #typeMapping['']='BIGINT'

def listFields(claZ):
    fields = list()
    for att in  claZ.PYMODEL_MODEL_INFO.attributes:
        if att.name in ["_baseversion", "version", "guid", "creationdate"]:
            continue
        field = dict()
        field ['name'] =  att.name
        field ['type'] =  att.attribute.__class__.__name__
        field ['Osistype'] = getOsisType(field ['type'])
        field ['uitype'] = getUIType(field ['type'])
        field ['converter'] = getTypeConverter(field ['type'])

        if field ['type'] == "Enumeration":
            field ['enum'] = att.attribute.type_.__name__

        fields.append(field)

    return fields

def getTemplateParams(specFile, appname = "", domain = "", params = dict() ):
    className = specFile.split(os.sep)[-1].split(".")[0]
    claZ = getClass(specFile,className)
    fieldsList = listFields(claZ)
    className = getClassName(claZ)
    params['rootobject'] = className
    params['fields'] = fieldsList
    params['domain'] = domain
    params['appname'] = appname
    return params

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
        self.requireAuthorization = False
        self.groups = list()
        if self.docs.find('@security admin') != -1:
            self.requireAuthorization = True
            self.groups.append('administrators')
        # Set  custom properties
        # Custom properties can be set in the docstring using key=value pairs in the following format:
        # @key = value
        # e.g. @security = admin
        #      @execution_method = async
        # and will be available in the properties dict:
        #      >>> method.properties['security']
        #      >>> 'admin'
        #      >>> method.properties['execution_method']
        #      >>> 'async'

        RE_KEY_VALUES = "^\s*(?:@+)(?P<key>\w+)\s*=+[\t\f\v ]*(?P<value>.*)[\t\f\v ]*$"
        self.properties = dict(re.findall(RE_KEY_VALUES, self.docs, re.M))



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

    for _, arg in enumerate(args):
        if arg == 'self':
            continue
        argument = Argument(arg, defaults[argList.index(arg)]) if defaults and arg in argList else Argument(arg, hasdefault=False)
        arguments.append(argument)

    return arguments

def getMethodProperties(method):
    args, _, _, defaults = inspect.getargspec(method)
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

def _encode(contents):
    #quickfix
    contents = contents.replace('{','\{')
    tags = { '\\{no'  :'{no',
             '\{toc'  :'{toc',
             '\{code' :'{code' }

    for tag in tags.iterkeys():
        contents = contents.replace(tag,tags[tag])

    return contents

def getClassMethods(specFile, className):
    claZ = getClass(specFile, className)
    methods = list()
    for funcName, func in listMethods(claZ).iteritems():
        method = getMethod(func, funcName)
        methods.append(method)
    return methods

def getClassName(claZ):
    pattern = re.compile('ro_', re.IGNORECASE)
    name = pattern.split(claZ.__name__)[-1]
    return name.lower()

class DotGenerator:
    def __init__(self, appname):
        self.appname = appname
        self.ignore_properties = ['_baseversion']
        self.ignore_domains = ['enumerators']

        self.graph = pydot.Dot()

        self.api = p.application.getAPI(appname, context=q.enumerators.AppContext.WFE)

        self.nodes = []
        self.links = {}

    def add_destination(self, source, destination, rootobject=False):
        if source in self.links.keys():
            self.links[source].append({'dest': destination, 'rootobject': rootobject})
        else:
            self.links[source] = [{'dest': destination, 'rootobject': rootobject}]

    def process_list(self, domain, classname, attr):
        if hasattr(attr.attribute.type_, 'type_') and hasattr(attr.attribute.type_.type_, 'PYMODEL_MODEL_INFO'):
            self.nodes.append(self.loop_attributes(domain=domain, classname=classname, model_info=attr.attribute.type_.type_.PYMODEL_MODEL_INFO, nodelabel='{ %s%s |' % (classname, attr.attribute.name)))

    def process_helper(self, domain, classname, attribute, property_name):
        self.add_destination('%s%s' % (domain, classname), '%s%s%s' % (domain, classname, attribute.name))

        self.nodes.append(self.create_subnode(domain=domain, classname=classname, attribute=attribute, property_name=property_name, sublabel='{ %s%s |' % (classname, property_name)))

    def create_subnode(self, domain, classname, attribute, property_name, sublabel):
        if '_pm_enumeration_items' in dir(attribute.type_):
            for key, value in attribute.type_._pm_enumeration_items.items():
                sublabel += '%s - %s \\n' % (key, value)
        elif 'PYMODEL_MODEL_INFO' in dir(attribute.type_):
            return self.loop_attributes(domain=domain, classname=classname, model_info=attribute.type_.PYMODEL_MODEL_INFO, nodelabel=sublabel)
        sublabel += '}'
        self.add_destination('%s%s' % (domain, classname), '%s%s%s' % (domain, classname, property_name))
        return pydot.Node(name='%s%s%s' % (domain, classname, property_name), label=sublabel, shape='record')

    def loop_attributes(self, domain, classname, model_info, nodelabel):
        for attr in itertools.ifilter(lambda x: x not in self.ignore_properties, model_info.attributes):
            nodelabel += '%s \\n' % attr.name
            if hasattr(attr.attribute, 'type_'):
                if isinstance(attr.attribute, model.List):
                    self.process_list(domain=domain, classname=classname, attr=attr)
                elif isinstance(attr.attribute, model.Object):
                    self.process_helper(domain=domain, classname=classname, attribute=attr.attribute, property_name=attr.name)
                    continue
                else:
                    self.nodes.append(self.create_subnode(domain=domain, classname=classname, attribute=attr.attribute, property_name=attr.name, sublabel='{ %s%s |' % (classname, attr.name)))
            elif type(attr.attribute) == model.GUID and attr.name != 'guid':
                destinationname = attr.name
                if attr.name.endswith('guid'):
                    destinationname = destinationname[0:-4]
                if attr.name.startswith('parent'):
                    destinationname = destinationname[6:]
                destinationname = '%s%s' % (domain, destinationname)
                self.add_destination('%s%s' % (domain, classname), destinationname, rootobject=True)
            if attr.name.endswith('s'):
                destinationname = '%s%s' % (domain, attr.name)
                self.add_destination('%s%s' % (domain, classname), destinationname, rootobject=True)

        nodelabel += '}'

        return pydot.Node(name='%s%s' % (domain, classname), label=nodelabel, shape='record')

    def generate_modelspec(self):
        self.process_model()
        self.create_graph()
        dest = q.system.fs.joinPaths(q.dirs.pyAppsDir, self.appname, "portal", "static" , "images", "modelspec.jpg")
        self.write_file(dest)

    def create_graph(self):
        for node in self.nodes:
            self.graph.add_node(node)

        nodenames = map(lambda x: x.get_name(), self.nodes)

        for source, destitems in self.links.items():
            for destitem in destitems:
                if destitem['rootobject']:
                    style = 'solid'
                else:
                    style = 'dashed'
                dest = destitem['dest']
                if dest.endswith('s') and dest not in nodenames:
                    dest = dest[:-1]
                if dest in nodenames:
                    self.graph.add_edge(pydot.Edge(src=source, dst=dest, style=style))

    def write_file(self, path):
        self.graph.write_jpeg(path)

    def process_model(self):
        for domain in itertools.ifilter(lambda x: x not in self.ignore_domains and not x.startswith('__'), dir(self.api.model)):
            for classname in itertools.ifilter(lambda x: not x.startswith('_'), dir(getattr(self.api.model, domain))):
                modelinfo = getattr(getattr(self.api.model, domain), classname)._ROOTOBJECTTYPE.PYMODEL_MODEL_INFO
                self.nodes.append(self.loop_attributes(domain=domain, classname=classname, model_info=modelinfo, nodelabel='{ %s |' % classname))

class CloudApiGenerator:
    rootobject_clientTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','template.tmpl')
    rootobject_serverTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','PylabsApp', 'AppApiActionService.tmpl')
    baseSpecDir = q.system.fs.joinPaths(q.dirs.tmpDir, 'ssospecs')
    specDir = q.system.fs.joinPaths(baseSpecDir, '1.1', 'codepackages', 'Actions_Interface_Rootobject')
    specDirActors = q.system.fs.joinPaths(baseSpecDir, '1.1', 'codepackages', 'Actions_Interface_Actor')
    rootobject_clientOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedClient')
    rootobject_serverOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer')
    rootobject_serverExtensionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'PylabsApp', 'AppApiAction.tmpl')
    rootobject_serverExtensionDest=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer','extensions')
    extensionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'extensionTemplate.tmpl')
    cloudapiqconfig=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'connectionTemplate.tmpl')
    cloudapiClientsTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiclientsTemplate.tmpl')
    serviceTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','servicestemplate.tmpl')
    exceptionTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','exception.tmpl')
    rootobjects_libDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedServer','cloud_api_rootobjects')
    rootobject_libTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','serverrootobjectlib.tmpl')
    basecloudapitemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'BaseCloudAPI.tmpl')
    taskletTemplate=q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','tasklets.tmpl')
    wizardTemplate =q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','wizardTemplate.tmpl')
    actorTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'PylabsApp', 'AppApiActor.tmpl')
    importSubModulesTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates', 'PylabsApp', 'AppImportSubmodules.tmpl')
    actorOutputDir =q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'actor')
    flexClientTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiFlexClient.tmpl')
    flexClientOutputDir = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedFlexClient')
    flexClientservicetemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','cloudapiFlexclientService.tmpl')
    roMainDirRest = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'doc')
    roMainDirXmlrpc = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'doc')
    flexServiceFileName='CloudApiRestService.as'
    documentationDest = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'doc')
    restDocumentationTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'restDocumentationTemplate.tmpl')
    xmlrpcDocumentationTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'xmlrpcDocumentationTemplate.tmpl')
    serviceAlkiraDocumentationTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'serviceAlkiraDocumentationTemplate.tmpl')
    apiAlkiraHomeTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'apiAlkiraHome.tmpl')
    apiAlkiraPageTree = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'apiAlkiraPageTree.tmpl')
    apiXmlrpcTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'apiXmlrpcTemplate.tmpl')
    apiRestTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'apiRestTemplate.tmpl')
    apiDomainTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'apiDomainTemplate.tmpl')
    dotModelTemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'templates', 'dotModelTemplate.tmpl')
    roDirRest = q.system.fs.joinPaths(documentationDest,'REST')
    roDirXmlrpc = q.system.fs.joinPaths(documentationDest, 'XMLRPC')
    _documentationFormat = 'alkira'

    def __init__(self, appName):
        self._appName = appName

    def _generateCodeStr(self, templatePath, params):
        template = Template(q.system.fs.fileGetContents(templatePath), params)
        return str(template)

    def _generateCode(self, templatePath, params, destPath):

        if not q.system.fs.exists(q.system.fs.getDirName(destPath)):
            q.system.fs.createDir(q.system.fs.getDirName(destPath))

        contents = self._generateCodeStr(templatePath, params)

        q.system.fs.writeFile(destPath, contents)


    def _generateModelImpl(self, specFile, appname, domain):
        params = getTemplateParams(specFile, appname, domain)

        params['table'] = "%s_view_%s_list"% (params['domain'], params['rootobject'] )
        params['schema'] = "%s_%s"% (params['domain'], params['rootobject'] )

        sqlSelect = "Select "
        for field in params['fields']:
            sqlSelect += "%s.%s, " %(params['table'], field['name'])
        sqlSelect =sqlSelect[:-2]
        sqlSelect += " FROM %s.%s "%(params['schema'] , params['table'])
        params['sqlSelect'] = sqlSelect


        actionsList = []
        #generating view files
        actionsList.append( ['ModelView.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "impl", "setup", "osis", "%s_%s_view.py"% (params['domain'],params['rootobject']))])

        #_generateOsisStoreDeleteCode
        actionsList.append( ['ModelStore.tmpl',q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "osis", "osis" , "store", "3_%s_%s_store.py"% (params['domain'],params['rootobject']))])
        actionsList.append( ['ModelDelete.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl" , "osis", "osis" , "delete", "1_%s_%s_delete.py"%(params['domain'],params['rootobject']))])

        #genarting action files
        actionsList.append( ['ModelCreateAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "create",  "1_%s_create.py"% params['rootobject'])])
        actionsList.append( ['ModelDeleteAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "delete",  "1_%s_delete.py"% params['rootobject'])])
        actionsList.append( ['ModelGetObjectAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "getObject",  "1_%s_getObject.py"% params['rootobject'])])
        actionsList.append( ['ModelListAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "list", "1_%s_list.py"% params['rootobject'])])
        actionsList.append( ['ModelUpdateAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "update", "1_%s_update.py"% params['rootobject'])])
        actionsList.append( ['ModelFindAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "action" , params["domain"], params["rootobject"], "find", "1_%s_find.py"% params['rootobject'])])
        actionsList.append( ['GenerateModelDetailsPage.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "events" , "page_generator" , "generate_%s_page.py"% params['rootobject'])])
        actionsList.append( ['ModelOverview.md.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "portal", "spaces" , params["domain"], "%sOverview.md"% params['rootobject'].capitalize())])

        #generateViewWizards
        actionsList.append( ['ModelCreateWizard.tmpl',q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "ui", "form", params["domain"], "%s_create"% params["rootobject"],   "1_%s_create.py"% params['rootobject'])])
        actionsList.append( ['ModelEditWizard.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "ui", "form", params["domain"], "%s_edit"% params["rootobject"],   "1_%s_edit.py"% params['rootobject'])])
        actionsList.append( ['ModelDeleteWizard.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "ui", "wizard", params["domain"], "%s_delete"% params["rootobject"],   "1_%s_delete.py"% params['rootobject'])])

        #generateinterfaceaction
        if domain != 'core' and domain != 'ui':
            actionsList.append( ['InterfaceAction.tmpl', q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "interface", "action", params["domain"], "%s.py"% params["rootobject"])])


        generatedFiles = []
        action = None
        for action in actionsList:
            templatePath = q.system.fs.joinPaths(self._template_path, 'CRUD', action[0])
            if  not q.system.fs.exists(action[1]):
                self._generateCode(templatePath, params, action[1])
                generatedFiles.append(action[1])

        try :
            templatePath = q.system.fs.joinPaths(self._template_path, "consumer.cfg.tmpl")
            dest = q.system.fs.joinPaths(q.dirs.pyAppsDir, params['appname'], "impl", "events" , "page_generator" , "consumer.cfg")
            self._generateCode(templatePath, params, dest)
            generatedFiles.append(action[1])

        except:
            q.logger.log('Error Generating consumer.cfg file', level=2)

        return generatedFiles

    def _generateClientCode(self, specFile, serviceName, templatePath, destPath, className ="", domain=""):
        claZ = getClass(specFile, className)
        methods = getClassMethods(specFile, className)
        for method in methods:
            #parse docstring for method
            errors = list()
            docInfo = epytext.parse(method.docs, errors)
            if not docInfo:
                continue

            #get type for every argument
            typedArgs = dict()
            for info in docInfo.children:
                if info.tag == "fieldlist":
                    for field in info.children:
                        name = None
                        isType = False
                        _type = None
                        for param in field.children:
                            if param.tag == "arg":
                                name = param.children[0]
                            elif param.tag == "tag":
                                isType = param.children[0] == "type"
                            elif param.tag == "para":
                                _type = param.children[0]

                        if isType:
                            typedArgs[name] = _type

            for arg in method.argClasses:
                if arg.name in typedArgs:
                    arg.argtype = typedArgs[arg.name]

        name = getClassName(claZ)
        methodsinfo = [(method.name, method) for method in methods]

        self._generateCode(templatePath, {'className': name, 'methods':methods, 'serviceName':serviceName}, destPath)

        if self._documentationFormat == 'confluence':
            roDirRestClass = q.system.fs.joinPaths(self.roDirRest, 'rest_%s'%name)
            roDirXmlrpcClass = q.system.fs.joinPaths(self.roDirXmlrpc, 'xmlrpc_%s'%name)
            if not q.system.fs.exists(roDirRestClass): q.system.fs.createDir(roDirRestClass)
            if not q.system.fs.exists(roDirXmlrpcClass): q.system.fs.createDir(roDirXmlrpcClass)

        if self._documentationFormat == 'confluence':
            self._generateCode(self.restDocumentationTemplate, {'className': name, 'methods':methods}, q.system.fs.joinPaths(roDirRestClass, 'rest_%s.txt'%name ))
            self._generateCode(self.xmlrpcDocumentationTemplate, {'className': name, 'methods':methods}, q.system.fs.joinPaths(roDirXmlrpcClass, 'xmlrpc_%s.txt'%name))
        elif self._documentationFormat == 'alkira':
            self._generateCode(self.apiAlkiraHomeTemplate, {}, q.system.fs.joinPaths(self.documentationDest, 'Home.md'))
            self._generateCode(self.apiAlkiraPageTree, {}, q.system.fs.joinPaths(self.documentationDest, 'pagetree.md'))
            self._generateCode(self.dotModelTemplate , {}, q.system.fs.joinPaths(self.documentationDest, 'Home', 'dotModel.md'))
            if not q.system.fs.exists(q.system.fs.joinPaths(self.documentationDest, 'Home', '%s.md' % domain)):
                self._generateCode(self.apiDomainTemplate, {'root': domain, 'name':domain}, q.system.fs.joinPaths(self.documentationDest, 'Home', '%s.md' % domain))
            if not q.system.fs.exists(q.system.fs.joinPaths(self.documentationDest, 'Home', domain, '%s_%s.md' % (domain, name))):
                self._generateCode(self.apiDomainTemplate, {'root':'%s_%s'%(domain,name), 'name':name}, q.system.fs.joinPaths(self.documentationDest, 'Home', domain, '%s_%s.md' % (domain, name)))
            for methodname, method in methodsinfo:
                self._generateCode(self.serviceAlkiraDocumentationTemplate, {'appname': self._appName,'className': name, 'method':method, 'domain':domain}, q.system.fs.joinPaths(self.documentationDest, 'Home', domain, '%s_%s' % (domain, name), '%s_%s_%s.md' % (domain, name, methodname)))

        return name

    def _generateServerCode(self, specFile, templatePath, destPath, serverExtensionTemplate="", serverExtensionDest="",rootobjectslibDest="", rootobjectlibTemplate="", className="", wizards=True, params=None):
        claZ = getClass(specFile, className)
        methods = getClassMethods(specFile, className)
        name = getClassName(claZ)

        params = params or {}
        params.update({'className': name, 'methods': methods, 'appname': self._appName, 'wfe_amqp': wfe_amqp})

        self._generateCode(templatePath,  params, destPath)

        if serverExtensionDest and serverExtensionTemplate:
            self._generateCode(serverExtensionTemplate,  params, serverExtensionDest)
            self._generateCode(rootobjectlibTemplate, params, rootobjectslibDest)

        """
        taskletsDir = q.system.fs.joinPaths(q.system.fs.getDirName(destPath), 'tasklets', str(name))
        if q.system.fs.exists(taskletsDir):
            q.system.fs.removeDirTree(taskletsDir)
        q.system.fs.createDir(taskletsDir)
        self._generateTasklets(str(name), methods, taskletsDir, self.taskletTemplate)
        """

        return name

    def _generateTasklets(self, rootobject, listOfMethods, outputDir, template):
        for method in listOfMethods:
            tasklets = q.system.fs.joinPaths(outputDir, method.name)
            q.system.fs.createDir(tasklets)
            self._generateCode(template, {'rootobject':rootobject, 'methodName':method.name}, q.system.fs.joinPaths(tasklets, '%s_%s.py'%(rootobject, method.name)))

    def generatePythonRoot(self):
        """
        Input Dir = specDir
        --------------------------------------------------------------------------------------------------------
        |Code Generated                | Templates                         |     Output Dir                    |
        --------------------------------------------------------------------------------------------------------
        |Cloudapi service code         |rootobject_serverTemplate          | rootobject_serverOutputDir        |
        |                              |basecloudapitemplate               |                                   |
        |                              |serviceTemplate                    |                                   |
        --------------------------------------------------------------------------------------------------------
        |Cloudapi rootobject lib       |rootobject_libTemplate             |rootobjects_libDir                 |
        --------------------------------------------------------------------------------------------------------
        |Cloudapi rootobject extension |rootobject_serverExtensionTemplate |rootobject_serverExtensionDest     |
        |                              |extensionTemplate                  |                                   |
        --------------------------------------------------------------------------------------------------------
        |Cloudapi client               |cloudapiClientsTemplate            |rootobject_clientOutputDir         |
        |                              |exceptionTemplate                  |                                   |
        |                              |extensionTemplate
        |                              |cloudapiqconfig                    |                                   |
        --------------------------------------------------------------------------------------------------------
        |Wizards skeleton              | wizardTemplate                    |rootobject_serverOutputDir/wizards |
        --------------------------------------------------------------------------------------------------------
        |Rootobject tasklets skeleton  |taskletTemplate                    |rootobject_serverOutputDir/tasklets|
        --------------------------------------------------------------------------------------------------------
        """

        q.system.fs.createDir(self.rootobject_clientOutputDir)
        q.system.fs.createDir(self.rootobject_serverOutputDir)
        q.system.fs.createDir(self.rootobject_serverExtensionDest)
        q.system.fs.createDir(self.rootobjects_libDir)

        modules = dict()
        #extensions = list()

        ##generate root object actions

        domains = list()


        for domain_spec in q.system.fs.listDirsInDir(self.specDir):

            domain = domain_spec.split(os.sep)[-1]
            domains.append({'modulename': domain, 'classname': domain})

            actions = list()

            for spec in q.system.fs.listFilesInDir(domain_spec, filter='*.py'):
                fileName = q.system.fs.getBaseName(spec)
                if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
                    continue
                #rootObject = fileName.split('.')[0].split('ro_')[-1]
                rootObject = fileName.split('.')[0]
                self._generateClientCode(spec, rootObject,self.rootobject_clientTemplate, q.system.fs.joinPaths(self.rootobject_clientOutputDir, domain, 'client_%s.py' % rootObject), domain=domain)
                #services[rootObject] = '%s.%s.%s' % (rootObject, domain, className)
                # Check whether this specification belongs to a configuration model specification or not
                isconfig = q.system.fs.exists(spec.replace('action', 'config'))
                params = {'domain': domain, 'appname': self._appName, 'isconfig': isconfig}

                className = self._generateServerCode(spec,self.rootobject_serverTemplate, q.system.fs.joinPaths(self.rootobject_serverOutputDir, domain, '%s.py'%rootObject), \
                                                     self.rootobject_serverExtensionTemplate, q.system.fs.joinPaths(self.rootobject_serverExtensionDest, domain, '%s.py'%rootObject),\
                                                     q.system.fs.joinPaths(self.rootobjects_libDir, 'cloud_api_%s.py'%rootObject), self.rootobject_libTemplate, params=params)

                actions.append({'modulename': rootObject, 'classname': className})

                self._generateCode(self.importSubModulesTemplate, {'imports':actions, 'classname': domain}, q.system.fs.joinPaths(self.rootobject_serverExtensionDest, domain, '__init__.py'))

                modules[rootObject] = className
                #extensions.append(Extension(className, className, 'q.actions.rootobject.%s'%className))
        self._generateCode(self.importSubModulesTemplate, {'imports':domains, 'classname': 'actions'}, q.system.fs.joinPaths(self.rootobject_serverExtensionDest, '__init__.py'))

        #self._generateCode(self.extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(self.rootobject_serverExtensionDest, 'extension.cfg'))
        extensions = list()
        #self._generateCode(self.basecloudapitemplate, {},  q.system.fs.joinPaths(self.rootobject_serverOutputDir, 'BaseCloudAPI.py'))
        #self._generateCode(self.serviceTemplate, {'services':services},  q.system.fs.joinPaths(self.rootobject_serverOutputDir, 'applicationserverservice.cfg'))
        ####
        #self._generateCode(self.exceptionTemplate, {}, q.system.fs.joinPaths(self.rootobject_clientOutputDir, 'Exceptions.py'))
        extensions.append(Extension('CloudApiConnectionsConfig', 'cloud_api_connections', 'i.config.cloudApiConnection'))
        #self._generateCode(self.extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(self.rootobject_clientOutputDir, 'extension.cfg'))
        self._generateCode(self.cloudapiClientsTemplate, {'modules':modules}, q.system.fs.joinPaths(self.rootobject_clientOutputDir, 'cloud_api_clients.py'))

        #self._generateCode(self.cloudapiqconfig, {}, q.system.fs.joinPaths(self.rootobject_clientOutputDir, 'cloud_api_connections.py'))

    def generatePythonActor(self):
        """
        Input Dir = specDir
        --------------------------------------------------------------------------------------------------------
        |Code Generated                | Templates                         |     Output Dir                    |
        --------------------------------------------------------------------------------------------------------
        |Actor Action extension        |actorTemplate                      | actorOutputDir                    |
        |                              |extensionTemplate                  |                                   |
        --------------------------------------------------------------------------------------------------------
        |Rootobject tasklets skeleton  |taskletTemplate                    |actorOutputDir/tasklets            |
        --------------------------------------------------------------------------------------------------------
        """
        ##generate actor actions
        q.system.fs.createDir(self.actorOutputDir)
        #extensions = list()
        domains = list()

        for domain_spec in q.system.fs.listDirsInDir(self.specDirActors):

            domain = domain_spec.split(os.sep)[-1]
            domain_path = q.system.fs.joinPaths(self.actorOutputDir, domain)
            q.system.fs.createDir(domain_path)

            params = {'domain': domain, 'appname': self._appName}
            domains.append({'modulename': domain, 'classname': domain})
            actors = list()

            for spec in q.system.fs.listFilesInDir(domain_spec, filter='*.py'):
                fileName = q.system.fs.getBaseName(spec)
                if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
                    continue
                moduleName =  fileName.split('.')[0]

                className = self._generateServerCode(spec,self.actorTemplate, q.system.fs.joinPaths(domain_path, fileName), wizards=False, params=params)

                #modules['client_ro_%s'%rootObject] = className/
                actors.append({'modulename': moduleName, 'classname': className})
                #extensions.append(Extension(className, moduleName, 'p.api.actor.%s.%s' % (domain, moduleName)))
            ##

            self._generateCode(self.importSubModulesTemplate, {'imports':actors, 'classname': domain}, q.system.fs.joinPaths(self.actorOutputDir, domain_path, '__init__.py'))
        #self._generateCode(self.extensionTemplate, {'extensions':extensions}, q.system.fs.joinPaths(self.actorOutputDir, 'extension.cfg'))


        self._generateCode(self.importSubModulesTemplate, {'imports':domains, 'classname': 'actors'}, q.system.fs.joinPaths(self.actorOutputDir, '__init__.py'))


    def generateFlexRoot(self):

        q.system.fs.createDir(self.flexClientOutputDir)
        ##generate root object actions
        for spec in q.system.fs.listFilesInDir(self.specDir, filter='*.py'):
            fileName = q.system.fs.getBaseName(spec)
            if  fileName in ('__init__.py', 'ro_DEFAULT.py'):
                continue
            rootObject = fileName.split('.')[0].split('ro_')[-1]
            self._generateClientCode(spec, 'cloud_api_%s'%rootObject,self.flexClientTemplate, q.system.fs.joinPaths(self.flexClientOutputDir, '%s.as'%rootObject.capitalize()))

        self._generateCode(self.flexClientservicetemplate, {}, q.system.fs.joinPaths(self.flexClientOutputDir, self.flexServiceFileName))

    def generateAll(self, documentationFormat='confluence'):
        """
        Generates all documentation and APIs.

        @type documentationFormat: String
        @param documentationFormat: The format you want the documentation to be generated in. NOTE: Value can only be 'alkira' or 'confluence'!
        """
        if documentationFormat == 'alkira':
            self._documentationFormat = 'alkira'
        elif documentationFormat == 'confluence':
            self._documentationFormat = 'confluence'
        else:
            q.errorconditionhandler.raiseError("Documentation format %s is unknown." %documentationFormat)

        self.generatePythonRoot()
        self.generatePythonActor()
        ##generate flex amf client
        self.flexClientOutputDir =q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator', 'generatedFlexAMFClient')
        self.flexClientTemplate =  q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','flexclient.tmpl')
        self.flexClientservicetemplate = q.system.fs.joinPaths(q.dirs.appDir, 'cloud_api_generator','templates','flexamfservice.tmpl')
        self.flexServiceFileName = 'CloudApiAMFService.as'
        self.generateFlexRoot()

    def _forceCreatePage(self, space, parentid, pageTitle, contents):
        pageid = self._checkPageExists(space, pageTitle)
        if pageid:
            q.clients.confluence.removePage(pageid)
        _id = q.clients.confluence.addPage(space, pageTitle, parentid, contents)
        return _id


    def _checkPageExists(self, space, pageTitle):
        try:
            page = q.clients.confluence.findPage(space, pageTitle)
        except:
            return None
        return page.id


    def _login(self, URI, login, password):
        if q.clients.confluence._impl:
            q.clients.confluence.logout()
            q.clients.confluence.connect(URI, login, password)
        else:
            q.clients.confluence.connect(URI, login, password)

    def checkoutSpecs(self, destination = '', remoteUrl="bitbucket.org/despiegk/ssospecs/", login="", password=""):
        if not destination:
            destination = self.baseSpecDir
        self.baseSpecDir = destination
        self.specDir = q.system.fs.joinPaths(self.baseSpecDir, '1.1', 'codepackages', 'Actions_Interface_Rootobject')
        self.specDirActors = q.system.fs.joinPaths(self.baseSpecDir, '1.1', 'codepackages', 'Actions_Interface_Actor')
        remoteurl = "http://%s:%s@%s" % (login, password, remoteUrl)
        q.clients.mercurial.getclient(self.baseSpecDir,remoteurl)

    def publishDocumentation(self,confluenceUri, login, password, space, parentpage):
        self._login(confluenceUri, login, password)

        try:
            parent = q.clients.confluence.findPage(space, parentpage)
        except:
            raise
        parentid = parent.id

        #Creating REST Documentation


        page = 'CLOUD_API'
        contents = '{children}'
        mainid    = self._forceCreatePage(space, parentid, page, contents)

        page = 'REST'
        contents = '{children}'
        restid = self._forceCreatePage(space, mainid, page, contents)

        for _dir in q.system.fs.listDirsInDir(self.roDirRest):
            rootobject = q.system.fs.getBaseName(_dir)
            rootobjectcontent = q.system.fs.fileGetContents(q.system.fs.joinPaths(_dir, "%s.txt"%rootobject))
            self._forceCreatePage(space, restid, rootobject, _encode(rootobjectcontent))

        page = 'XMLRPC'
        contents = '{children}'
        xmlrpcid = self._forceCreatePage(space, mainid, page, contents)

        for _dir in q.system.fs.listDirsInDir(self.roDirXmlrpc):
            rootobject = q.system.fs.getBaseName(_dir)
            rootobjectcontent = q.system.fs.fileGetContents(q.system.fs.joinPaths(_dir, "%s.txt"%rootobject))
            self._forceCreatePage(space, xmlrpcid, rootobject, _encode(rootobjectcontent))

    def publishToAlkira(self, space, main_page='Cloud API Documentation', parent_name=None, hostname='127.0.0.1'):
        """
        Publishes the Cloud API documentation to an Alkira space.

        @type space: String
        @param space: The name of the space.

        @type main_page: String
        @param main_page: The name of the page.

        @type parent_name: String
        @param parent_name: Name of a parent page in case you want the documentation page to be a child of it.

        @type hostname: String
        @param hostname: The IP that the Alkira Client will use to get a connection and add the pages.
        """
        alkira_client = q.clients.alkira.getClient(hostname)
        main_content = '# %s' % main_page

        if parent_name:
            alkira_client.createPage(space, main_page, content=main_content, parent=parent_name)
        else:
            alkira_client.createPage(space, main_page, content=main_content)

        for path in q.system.fs.listDirsInDir(self.documentationDest):
            domainname = q.system.fs.getBaseName(path)
            q.logger.log('Publishing %s domain page' % domainname, 2)
            domaincontent = q.system.fs.fileGetContents(q.system.fs.joinPaths(path, '%s.md' % domainname))
            alkira_client.createPage(space, domainname, domaincontent, parent=main_page)
            for rootobjectpath in q.system.fs.listDirsInDir(path):
                rootobjectname = q.system.fs.getBaseName(rootobjectpath).split('_')[1].split('.')[0]
                q.logger.log('Publishing %s rootobject page' % rootobjectname, 2)
                rootobjectcontent = q.system.fs.fileGetContents(q.system.fs.joinPaths(rootobjectpath, '%s_%s.md' % (domainname, rootobjectname)))
                alkira_client.createPage(space, rootobjectname, rootobjectcontent, parent=domainname)
                for methodpath in q.system.fs.listFilesInDir(rootobjectpath):
                    methodname = q.system.fs.getBaseName(methodpath).split('_')[2].split('.')[0]
                    methodcontent = q.system.fs.fileGetContents(methodpath)
                    alkira_client.createPage(space, '%s_%s_%s' % (domainname, rootobjectname, methodname), methodcontent, parent=rootobjectname)


class AppAPIGenerator(object):

    def __init__(self):
        self._template_path = q.system.fs.joinPaths(os.path.dirname(__file__), 'templates')
    def generateCRUDImpl(self, appname, domain = None, modelSpec = None):
        specDir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "interface", "model")
        print "(generateCRUDImpl(self, %s, %s,%s):)"%(appname, domain , modelSpec )
        if not appname:
            raise Exception ("appname should be provided ")

        if appname and not domain and not modelSpec:
            result = dict()
            for domain_spec in q.system.fs.listDirsInDir(specDir):
                domain = domain_spec.split(os.sep)[-1]
                domainFiles = self._generateCRUDImplForDomain(appname, domain)
                result[domain] =  domainFiles
        elif appname and domain and not modelSpec:
            return self._generateCRUDImplForDomain(appname, domain)

        elif appname and domain and modelSpec:
            return self._generateCRUDImplForModel(appname, domain, modelSpec )


    def _generateCRUDImplForDomain(self, appname, domain ):
        print "    _generateCRUDImplForDomain( %s, %s )"%(appname, domain)
        domainSpecDir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "interface", "model", domain)
        generatedFiles = dict()
        for _model in q.system.fs.listFilesInDir(domainSpecDir, filter='*.py'):
            _model = _model.split(os.sep)[-1]
            _model = _model.split(".")[0]
            files = self._generateCRUDImplForModel(appname, domain, _model)
            generatedFiles[_model] = files
        return generatedFiles

    def _generateCRUDImplForModel(self, appname, domain, modelSpec ):
        """
        Generates CRUD files for model spec file
        modelSpecFile: can be the full path of model file ,
                       or can be the class name , in case of class name , spec file will be retrived from
                       /opt/qbase/pyapps/<appname>/interface/model/<domain>/<modelSpec>.py
                       N.B: in both cases , file name should be the same as model class name
        """

        modelSpecFile = None
        if not q.system.fs.isFile(modelSpec):
            model_spec_dir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "interface", "model")
            modelSpecFile =  q.system.fs.joinPaths (model_spec_dir, domain, "%s.py"%modelSpec )
        self._generator = CloudApiGenerator(appname)
        self._generator._template_path = self._template_path

        modelFiles = self._generator._generateModelImpl(modelSpecFile, appname, domain )

        print "Generated Files are :%s"%modelFiles
        return modelFiles
    def _generateBaseDirs(self, appname):
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'interface', 'actor'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'interface', 'action'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'interface', 'model'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'interface', 'config'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'interface', 'monitoring'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'authenticate'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'authorize'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'ui', 'form'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'ui', 'wizard'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'setup', 'osis'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'osis'))

    def getSpacePage(self, space):
        """
        Gets the content of a space
        """
        self._generator = CloudApiGenerator("")
        return self._generate_str("SpacePage.tmpl", {'space': space})


    def generate(self, appname):
        """
        For a given application:
            * Generates base services.
            * Generates action API.
            * Generates actor API.

        @type appname: String
        @param appname: The name of your application.
        """
        self._generateBaseDirs(appname)
        self._generator = CloudApiGenerator(appname)
        q.action.start('Generating base services')
        self._generate_default_services(appname)
        q.action.stop()

        q.action.start('Generating API for %s application' % appname)
        app_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname)
        if not q.system.fs.exists(app_path):
            raise ValueError('Application %s not found', appname)

        interface_path = q.system.fs.joinPaths(app_path, 'interface')
        if not q.system.fs.exists(interface_path):
            raise ValueError('Interfaces for application %s not found' % appname)

        q.action.start('Generating action API')
        spec_path = q.system.fs.joinPaths(interface_path, 'action')
        if not q.system.fs.exists(spec_path):
            raise ValueError('Interfaces of type "action" for application %s not found' % appname)

        self._generator.importSubModulesTemplate = q.system.fs.joinPaths(self._template_path, 'AppImportSubmodules.tmpl')

        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'service'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'action'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'impl', 'actor'))

        docdir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'portal', 'spaces', 'api')
        self._create_folder(docdir)

        self._create_file(q.system.fs.joinPaths(q.dirs.pyAppsDir, '__init__.py'))
        self._create_file(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, '__init__.py'))
        self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'client'))
        self._create_file(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'client', '__init__.py'))


        self._generator.specDir = spec_path
        self._generator.rootobject_serverTemplate = q.system.fs.joinPaths(self._template_path, 'AppApiActionService.tmpl')
        self._generator.rootobject_serverExtensionTemplate = q.system.fs.joinPaths(self._template_path, 'AppApiAction.tmpl')
        self._generator.rootobject_clientOutputDir = q.system.fs.joinPaths(app_path, 'tmp', 'action', 'client')
        self._generator.rootobjects_libDir  = q.system.fs.joinPaths(app_path, 'tmp', 'action', 'lib')
        self._generator.rootobject_serverOutputDir  = q.system.fs.joinPaths(app_path, 'impl', 'service')
        self._generator.rootobject_serverExtensionDest  = q.system.fs.joinPaths(app_path, 'client', 'action')

        self._generator.roDirRest = docdir
        self._generator.roDirXmlrpc = docdir
        self._generator.documentationDest = docdir

        #self._generator.rootobject_serverExtensionDest  = q.system.fs.joinPaths(app_path, 'tmp', 'action', 'extension')
        self._generator.generatePythonRoot()
        q.action.stop()

        q.action.start('Generating actor API')
        spec_path = q.system.fs.joinPaths(interface_path, 'actor')
        if not q.system.fs.exists(spec_path):
            raise ValueError('Interfaces of type "actor" for application %s not found' % appname)

        self._generator.actorTemplate = q.system.fs.joinPaths(self._template_path, 'AppApiActor.tmpl')
        self._generator.specDirActors = spec_path
        self._generator.actorOutputDir = q.system.fs.joinPaths(app_path, 'client', 'actor')
        self._generator.generatePythonActor()
        q.action.stop()

        if pydot:
            dg = DotGenerator(appname)
            dg.generate_modelspec()

        q.action.stop()



    def _generate_default_services(self, appname):

        print 'Generate Default Services'

        # Generate default services
        params = {'appname': appname}

        #Create folders
        self._generateFolders(appname)

        files = [{'template':'SchedulerService.tmpl', 'params':params,
                            'destination':['impl', 'service', 'Scheduler.py']},

           {'template':'OsisService.tmpl', 'params':params,
                               'destination':['impl', 'service', 'osissvc.py']},

           {'template':'WizardService.tmpl', 'params':params,
                               'destination':['impl', 'service', 'ui', 'wizard.py']},

           {'template':'PortalService.tmpl', 'params':params,
                               'destination':['impl', 'service', 'ui', 'portal.py']},

           {'template':'services/ide.tmpl', 'params':params,
                               'destination':['impl', 'service', 'ui', 'ide.py']},

           {'template':'services/oauth.tmpl', 'params':params,
                               'destination':['impl', 'service', 'ui', 'oauth.py']},

           {'template':'services/auth.tmpl', 'params':params,
                               'destination':['impl', 'service', 'ui', 'auth.py']},

           {'template':'AgentService.tmpl', 'params':params,
                               'destination':['impl', 'service', 'AgentSVC.py']}]

        for _file in files:
            path = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, *_file['destination'])
            if not q.system.fs.exists(path):
                self._generate_file(_file['template'], _file['params'], path)

        defaults_path = q.system.fs.joinPaths( q.dirs.extensionsDir, 'api_generator', 'defaults')

        defaults = q.system.fs.walk(defaults_path, recurse=1)

        for _file in defaults:
            app_file = _file.replace(defaults_path, q.system.fs.joinPaths(q.dirs.pyAppsDir, appname))
            if not q.system.fs.exists(app_file):
                q.system.fs.copyFile(_file, app_file)


    def _generate_str(self, template, params):
        return self._generator._generateCodeStr(
            q.system.fs.joinPaths(self._template_path, template), params)

    def _generate_file(self, template, params, path):
        self._generator._generateCode(
            q.system.fs.joinPaths(self._template_path, template),
            params, path)

    def _generateFolders(self, appname):
        folders = [['impl', 'schedule'],
            ['impl', 'osis'],
            ['impl', 'ui'],
            ['impl', 'portal'],
            ['interface', 'action', 'core'],
            ['interface', 'action', 'ui'],
            ['interface', 'model', 'core'],
            ['interface', 'model', 'ui'],
            ['impl', 'action', 'core', 'job', 'clear'],
            ['impl', 'action', 'core', 'job', 'create'],
            ['impl', 'action', 'core', 'job', 'delete'],
            ['impl', 'action', 'core', 'job', 'find'],
            ['impl', 'action', 'core', 'job', 'findLatestJob'],
            ['impl', 'action', 'core', 'job', 'getJobTree'],
            ['impl', 'action', 'core', 'job', 'getLogoInfo'],
            ['impl', 'action', 'core', 'job', 'getObject'],
            ['impl', 'action', 'core', 'job', 'getXML'],
            ['impl', 'action', 'core', 'job', 'getXMLSchema'],
            ['impl', 'action', 'core', 'job', 'getYAML'],
            ['impl', 'action', 'ui', 'page', 'create'],
            ['impl', 'action', 'ui', 'page', 'delete'],
            ['impl', 'action', 'ui', 'page', 'find'],
            ['impl', 'action', 'ui', 'page', 'getObject'],
            ['impl', 'action', 'ui', 'page', 'update'],
            ['impl', 'setup', 'osis'],
            ['impl', 'osis', 'osis', 'delete'],
            ['impl', 'osis', 'osis', 'store'],
            ['impl', 'osis', 'osis', 'findasview'],
            ['impl', 'osis', 'osis', 'findobject'],
            ['impl', 'osis', 'osis', 'get'],
            ['impl', 'osis', 'osis', 'query'],
            ['impl', 'init', 'portal']
            ]
        for folder in folders:
            self._create_folder(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname,*folder))


    def _create_folder(self, path):
        if not q.system.fs.exists(path):
            q.system.fs.createDir(path)

    def _create_file(self, path):
        if not q.system.fs.exists(path):
            q.system.fs.createEmptyFile(path)
