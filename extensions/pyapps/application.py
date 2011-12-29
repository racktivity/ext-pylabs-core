import sys
import time
import xmlrpclib

from pylabs import q, p, locale
from pylabs.baseclasses import BaseEnumeration
from pylabs.config.generator import PyAppsConfigGen

class AppContext(BaseEnumeration):
    def __repr__(self):
        return str(self)

AppContext.registerItem('appserver')
AppContext.registerItem('wfe')
AppContext.registerItem('client')
AppContext.finishItemRegistration()


class AppManager(object):

    def __init__(self):
        pass

    def getAPI(self, appname, host='127.0.0.1', context=None, username=None, password=None):
        '''Retrieve api object for an application'''
        api = ApplicationAPI(appname, host, context, username, password)
        if not hasattr(p, 'api'):
            p.api = api
        return api

    def install (self, appname):
        app_dir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname)
        if not q.system.fs.exists(app_dir):
            raise RuntimeError('Application "%s" does not exist'%appname)

        p.core.codemanagement.api.generate(appname)
        p.core.codemanagement.language.compile(appname)
        gen = PyAppsConfigGen(appname)
        q.action.start("Generating config for %s" % appname)
        gen.generateAll()
        q.action.stop()
        q.action.start("Setting up %s" % appname)
        gen.setup()
        q.action.stop()
        q.action.start("Restarting %s" % appname)
        gen.stop()
        gen.start()
        q.action.stop()
        q.action.start("Initializing %s" % appname)
        gen.init()
        q.action.stop()

    def getOsisConnection(self, appname):
        from osis.store.OsisDB import OsisDB
        osis = OsisDB().getConnection(appname)
        return osis

    def getRabbitMqHost(self, appname):
        path = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'cfg', 'rabbitmq')
        return q.config.getConfig(path).get("main", {}).get("host", '127.0.0.1')

    def _validate_user_inputs(self, appname, keepchanges):
        if not q.system.fs.isDir(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname)):
            raise Exception( "%s is not valid application name " % appname)
        if keepchanges is None:
            return q.gui.dialog.askYesNo("Note: Due to design of qshell, qshell must be restarted after the call of reinstall. \nDo you want to keep change? WARRNING: USE THIS OPTION AT YOUR RISK")
        return keepchanges



    def reinstall(self, appname, keepchanges=None):
        """
        reinstalls applicationn apname
        param @keepchanges : find changed files backup  , reinstall, restore
        due to design of qshell, qshell must be restarted after the call of reinstall
        """

        keepchanges = self._validate_user_inputs(appname, keepchanges)
        try:
            p.application.stop(appname)
        except:
            error="Error stopping application, this error probably due to running reinstall twice without restarting qshell,  please restart qshell and try agin"
            q.logger.log(error, 1)

        q.logger.log("Removing postgres database", 1)
        if q.manage.postgresql8.cmdb.databases.has_key(appname):
            try:
                q.manage.postgresql8.stop()
                q.manage.postgresql8.startChanges()
                q.manage.postgresql8.cmdb.removeDatabase(appname)
                q.manage.postgresql8.cmdb.save()
                q.manage.postgresql8.applyConfig()
                q.manage.postgresql8.start()
            except:
                q.manage.postgresql8.cmdb.save()
                q.manage.postgresql8.applyConfig()
                q.manage.postgresql8.start()

        q.logger.log("Removing arakoon db", 1)

        arakoon_db_path = q.system.fs.joinPaths(q.dirs.baseDir, 'var','db', appname)
        q.system.fs.removeDirTree(arakoon_db_path)
        q.system.fs.createDir (q.system.fs.joinPaths(q.dirs.varDir, 'db', appname,appname+"_0"))

        # if changes done
        # check if there is is changes done in the installed app
        if keepchanges:
            changed_files, created_files, deleted_files, is_app_changed = self._getChangedFiles(appname)
            backup_folder = self._backup_changed_files(changed_files, created_files, deleted_files, appname)

            #reinstalling sampleapp package
            package = q.qp.find(appname)[0]
            package.install(reinstall=True)
            self._restore_backup(backup_folder, changed_files, created_files, deleted_files)

        else:
            backup_folder=q.system.fs.joinPaths(q.dirs.varDir, "tmp", "backup", appname, str(time.time()) , "_full")
            appdir=q.system.fs.joinPaths(q.dirs.pyAppsDir, appname)
            q.system.fs.moveDir(appdir, backup_folder)

            package = q.qp.find(appname)[0]
            package.install(reinstall=True)

        q.manage.postgresql8.stop()
        q.manage.postgresql8.start()
        p.application.install(appname)

        q.gui.dialog.message("%s was reinstalled sucessfully .\n Copy of previous app were backedup in %s\n qshell should be restarted , Please restart qshell by choosing yes"%(appname, backup_folder))
        exit()

    def _restore_backup(self, backup_folder, changed_files, created_files, deleted_files):
        for changed_file in changed_files:
            backup_file = q.system.fs.joinPaths(backup_folder, changed_file[1:])
            q.system.fs.copyFile(backup_file, changed_file)
        for created_file in created_files:
            backup_file = q.system.fs.joinPaths(backup_folder, created_file[1:])
            try:
                if q.system.fs.isFile(backup_file):
                    q.system.fs.copyFile(backup_file, created_file)
                else:
                    q.system.fs.createDir(created_file)
            except:
                q.logger.log("Failed to restore %s"% created_file, 1)

        for file in deleted_files:
            try:
                if q.system.fs.isFile(file):
                    q.system.fs.remove(file)
                else:
                    q.system.fs.removeDirTree(file)
            except:
                    q.logger.log("folder %s removed by install job and no mean to delete it "% file, 1)

    def _backup_changed_files(self, changed_files, created_files, deleted_files, appname):
        backup_folder = q.system.fs.joinPaths(q.dirs.varDir, "tmp","backup", appname, str(time.time()))
        q.system.fs.createDir(backup_folder)
        for changed_file in changed_files:
            to_file = q.system.fs.joinPaths(backup_folder, changed_file[1:])
            q.system.fs.copyFile(changed_file, to_file)
        for created_file in created_files:
            to_file=q.system.fs.joinPaths(backup_folder, created_file[1:])
            try:
                if q.system.fs.isFile(created_file):
                    q.system.fs.copyFile(created_file, to_file)
                else:
                    q.system.fs.createDir(to_file)
            except:
                q.eventhandler.raiseWarning("Error coping file %s"% created_file)
        deleted_file_path=q.system.fs.joinPaths(backup_folder, "%s_deletedFiles.txt"% appname)
        deleted_file_dump= open(deleted_file_path, "a")
        deleted_file_dump.write(str(deleted_files))
        deleted_file_dump.close()
        return backup_folder

    def _getChangedFiles(self, appname):
        """returns lists changed_files, created_files, deleted_files by comapring  the folders

        /opt/qbase5/pyapps/%s
        /opt/qbase5/var/qpackages4/files/pylabs5/%s/0.5/generic/pyapps/%s

        where %s is the appname
        """
        package = q.qp.find(appname)[0]
        packagePath = package.getPathFiles()

        changed_files_command = "diff -r -q  -y --suppress-common-lines /opt/qbase5/pyapps/%s %s/generic/pyapps/%s | grep 'differ' |awk '{print $2}'" %(appname, packagePath, appname)
        created_files_command = "diff -r -q     --suppress-common-lines /opt/qbase5/pyapps/%s %s/generic/pyapps/%s | grep 'Only in /opt/qbase5/pyapps' |grep -v '/portal/static: js'| grep -v ': tmp'| grep -v  'spaces/api:' |grep -v ': cfg' |grep -v ': client'|grep -v ': service'  |grep -v ': __init__.py'| grep -v ': formwizard.md' |grep -v '.pyc'| awk '{sub(\":\",\"/\");print $3$4 }' "  %(appname, packagePath, appname)
        deleted_files_command = "diff -r -q  -y --suppress-common-lines /opt/qbase5/pyapps/%s %s/generic/pyapps/%s  |grep 'Only in /opt/qbase5/var' |awk '{sub(\"%s/generic/pyapps/%s\",\"/opt/qbase5/pyapps/%s\");print $0 }' |     awk '{sub(\":\",\"/\");print $3$4 }'"  %(appname, packagePath, appname, packagePath, appname, appname)

        exitCode, output1 = q.system.process.execute(changed_files_command)
        changed_files=output1.splitlines()

        exitCode, output2 = q.system.process.execute(created_files_command)
        created_files=output2.splitlines()

        exitCode, output3 = q.system.process.execute(deleted_files_command)
        deleted_files = output3.splitlines()

        is_changed =  len(deleted_files) > 0 or len(created_files) > 0 or len(changed_files) > 0

        q.logger.log("changed_files %s"%str(changed_files), 1)
        q.logger.log("created_files %s"%str(created_files), 1)
        q.logger.log("deleted_files %s"%str(deleted_files), 1)

        return changed_files, created_files, deleted_files, is_changed

    def syncPortal(self, appname, space=None, page=None, clean_up=False):
        from alkira.sync_md_to_lfw import sync_to_alkira
        sync_to_alkira(appname, sync_space=space, sync_page=page, clean_up=clean_up)


    def check_application(function):

        def _check_application(self, appname):
            app_dir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname)
            if not q.system.fs.exists(app_dir):
                raise RuntimeError('Application "%s" does not exist'%appname)

            app_cfg_dir = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, 'cfg')
            if not q.system.fs.exists(app_cfg_dir):
                raise RuntimeError('Application "%s" configuration does not exist ... Please install application first'%appname)

            return function(self, appname)

        return _check_application

    @check_application
    def start(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.start()

    @check_application
    def stop(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.stop()

    @check_application
    def restart(self, appname):
        gen = PyAppsConfigGen(appname)
        gen.stop()
        gen.start()


class Events(object):
    def __init__(self, app):
        self._app = app
        self._hostname = p.application.getRabbitMqHost(app.appname)

    def publish(self, rootingKey, tagString):
        p.events.publish(rootingKey, tagString, self._hostname)

class ApplicationAPI(object):

    def __init__(self, appname, host=None, context=None, username=None, password=None):

        # Default to client context
        context = context or q.enumerators.AppContext.CLIENT
        self._app_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname)
        self._host = host
        self._username = username
        self._password = password

        if q.dirs.pyAppsDir not in sys.path:
            sys.path.append(q.dirs.pyAppsDir)
        if self._app_path not in sys.path:
            sys.path.append(self._app_path)

        self.appname = appname
        self.events = Events(self)
        self.action = self._get_actions(appname, context)

        categories = ('model', 'config', 'monitoring')
        from pylabs.baseclasses.BaseEnumeration  import pymodelEnumerators
        if not context == q.enumerators.AppContext.CLIENT:
            for category in categories:
                client = self._get_osis_client(appname, category, context)
                client.enumerators = pymodelEnumerators.get((appname, category))
                setattr(self, category, client)
            #load language localizer if found
            localepath = q.system.fs.joinPaths(self._app_path, "share", "locale")
            if q.system.fs.isDir(localepath):
                self.language = locale.getlocalizer(appname, localepath)
                
            if context == q.enumerators.AppContext.WFE:
                self.actor = self._get_actors(appname, context)

    def _get_actors(self, appname, context):
        from client.actor import actors
        return actors()

    def _get_actions(self, appname, context):

        proxy = None
        if context == q.enumerators.AppContext.CLIENT:
            host = self._host
            if self._username and self._password:
                host = "%s:%s@%s" % (self._username, self._password, host)
            proxy = XmlRpcActionProxy('http://%s/%s/appserver/xmlrpc/' % (host, appname))
        actions = __import__("%s.client" % appname, globals(), locals(), ["action"], -1).action.actions
        return actions(proxy=proxy)

    def _get_osis_client(self, appname, category, context=None):
        import os.path

        import pymodel
        from pymodel import serializers

        from osis.client import connection, xmlrpc, local

        def list_(path_):
            subdirs = ((entry, os.path.join(path_, entry)) for entry in os.listdir(path_)
                if os.path.isdir(os.path.join(path_, entry)))

            for (name, subdir) in subdirs:
                models = pymodel.load_models(subdir)

                for model in models:
                    yield ((category, name, model.__name__), model)

        def load(path_, transport_, serializer_):
            return connection.generate_client(list_(path_), transport_, serializer_)

        path = os.path.join(self._app_path, 'interface', category)
        transport_uri = 'http://%s:80/%s/appserver/xmlrpc/' % (self._host, appname)
        osisservice = 'osissvc'
        transport = None
        #TODO Fix local transport
        if False and self._host in ('localhost', '127.0.0.1') and context != q.enumerators.AppContext.WFE:
            tasklet_path = os.path.join(self._app_path, 'impl', 'osis')
            transport = local.LocalTransport(list_(path))
            transport.tasklet_engine = q.taskletengine.get(tasklet_path)
            orig_execute = transport.tasklet_engine.execute
            def execute(**kwargs):
                params = kwargs.pop('params', None)
                params = params if params is not None else {}
    
                if 'rootobjecttype' in params and len(params['rootobjecttype']) == 3:
                    category, domain, rootobjecttype = params['rootobjecttype']
    
                    params.update({
                        'category': category,
                        'domain': domain,
                        'rootobjecttype': rootobjecttype,
                    })
                if 'rootobjectguid' in params:
                    params['rootobjectguid'] = str(params['rootobjectguid'])
    
                kwargs['params'] = params
    
                result = orig_execute(**kwargs)
                if 'result' in params and isinstance(params['result'], tuple):
                    params['result'] = list(params['result'])
                return result

            transport.tasklet_engine.execute = execute


        elif context == q.enumerators.AppContext.WFE:
            from workflowengine.xmlrpc import ConcurrenceOsisXMLRPCTransport
            transport = ConcurrenceOsisXMLRPCTransport(transport_uri, osisservice)
        else:
            transport = xmlrpc.XMLRPCTransport(transport_uri, osisservice)
        serializer = serializers.ThriftSerializer

        return load(path, transport, serializer)

class XmlRpcActionProxy(object):

    def __init__(self, url):
        self.client = xmlrpclib.ServerProxy(url, allow_none=True)

    def __call__(self, domainname, classname, methodname, *args):

        try:
            m = getattr(self.client, domainname)
            m = getattr(m, classname)
            m = getattr(m, methodname)

            return m(*args)
        except AttributeError:
            raise
        except Exception:
            raise



