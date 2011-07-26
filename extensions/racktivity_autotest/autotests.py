from pylabs.baseclasses import BaseEnumeration
import simplejson
import os
import time
from pylabs import q

class RacktivityAutoTestPubishFormat(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('FILESYSTEM')
        cls.registerItem('CONSOLE')
        cls.registerItem('SERVICE')
        cls.finishItemRegistration()

SCENARIOS_PATH=q.system.fs.joinPaths(q.dirs.varDir, "scenarios")

class RacktivityTesting():
    CFG_NAME = "racktivity_autotests"
    def configure(self, logformat=RacktivityAutoTestPubishFormat.CONSOLE, loguser="",  logpassword="",logservice="http://racktivity.com:4444", logdir="/opt/racktivity_test_logs",testscenario="racktivity"):
        """
        Write parameters to configuration file which can be used by the other extension functions, check if testscenarios are available.
        """
        ini = q.config.getInifile(self.CFG_NAME)
        ini.addSection("main")
        ini.setParam("main", "logformat", logformat)
        ini.setParam("main", "loguser", loguser)
        ini.setParam("main", "logpassword", logpassword)
        ini.setParam("main", "logservice", logservice)
        ini.setParam("main", "logdir", logdir)
        ini.setParam("main", "testscenario", testscenario)
        
    
    def _getConfig(self, key, default=None):
        config = q.config.getConfig(self.CFG_NAME)
        if "main" in config:
            return config["main"].get(key, default)
        else:
            return default
    
    def _addEmulator(self, cfg):
        name = cfg['name']
        type = cfg.get('type', 'PM0816')
        port = cfg['port']
        model = cfg.get('model', "0.1")
        login = cfg['login']
        password = cfg['password']
        database = cfg['database']
        
        if name in q.manage.rackemulator.listEmulators():
            q.manage.rackemulator.stop(name)
            q.manage.rackemulator.startChanges()
            q.manage.rackemulator.cmdb.removeEmulator(name)
            q.manage.rackemulator.save()
        
        q.manage.rackemulator.startChanges()
        emu = q.manage.rackemulator.cmdb.addEmulator(name, type, int(port), model)
        emu.database = database
        emu.initialize_db = True
        q.manage.rackemulator.save()
        
        code, msg = q.manage.rackemulator.start(name)
        if code != 0:
            raise RuntimeError("Failed to start emulator '%s' error: %s" % (name, msg))
        
        #make sure that the emulator didn't stop unexpectedly and give it a change to setup the database.
        if not q.manage.rackemulator.isRunning(name):
            raise RuntimeError("Emulator '%s' dies unexpectedly" % name)
        
        client = q.clients.racktivitycontroller.connect("localhost", int(port), "root", "rooter")
        for i in range(10):
            #ping until you get a response
            try:
                client.master.getAdminLogin()
                break
            except IOError, e:
                q.logger.log("Connection refused, retyring ...")
                time.sleep(2)
            
        client.master.setAdminLogin(login)
        #reconnect to re-authenticate otherwise the next call will fail
        client = q.clients.racktivitycontroller.connect("localhost", int(port), login, "rooter")
        client.master.setAdminPassword(password)
    
    def _removeEmulator(self, name):
        if name not in q.manage.rackemulator.cmdb.emulators:
            return
        code, msg = q.manage.rackemulator.stop(name)
        if code != 0:
            q.logger.log("Failed to stop emulator '%s'. Deleting anyway" % code)
        q.manage.rackemulator.startChanges()
        q.manage.rackemulator.cmdb.removeEmulator(name)
        q.manage.rackemulator.save()

    def _startScenarion(self, scenario, stage):
        if scenario not in self.list():
            raise RuntimeError("Scenario '%s' doesn't exits" % scenario)
        
        scenariopath = q.system.fs.joinPaths(SCENARIOS_PATH, scenario)
        initdir = q.system.fs.joinPaths(scenariopath, "tasklets")
        te = None
        if q.system.fs.isDir(initdir):
            te = q.taskletengine.get(initdir)
        cfgfile = q.system.fs.joinPaths(scenariopath, "main_config.cfg")
        if not q.system.fs.isFile(cfgfile):
            raise RuntimeError("No main_config.cfg file found for scenario '%s'" % scenario)
        
        cfg = q.tools.inifile.open(cfgfile)
        maincfg = {}
        if 'main' not in cfg.getSections():
            raise RuntimeError("No main secion in '%s/main_confic.cfg'" % scenario)
        maincfg = cfg.getSectionAsDict("main")
        stages = int(maincfg.get("stages", 1))
        testcase = maincfg['testcase']
        
        emulators = list()
        try:
            params = {}
            
            
            
            if "params" in cfg.getSections():
                params.update(cfg.getSectionAsDict('params'))
            
            paramsconfig = q.config.getConfig("scenarioparams")
            if 'main' in paramsconfig:
                params.update(paramsconfig['main'])
            
            params['stage'] = stage
            if te:
                q.logger.log("Starting the setup tasklets for stage '%d'" % params['stage'], 1)
                te.execute(params, tags=("test", "setup"))
            
            #run testcases and configure emulators on the last stage.
            if stage == stages:
                sections = filter(lambda s: s.startswith("emulator_"), cfg.getSections())
                sections.sort()
                keys = ("name", "port", "database", 'login', 'password')
                for section in sections:
                    emulatorCfg = cfg.getSectionAsDict(section)
                    for k in keys:
                        if k not in emulatorCfg:
                            raise RuntimeError("Section '%' misses '%s' (%s)" % (section, k, cfgfile))
                    emulators.append(emulatorCfg['name'])
                    q.logger.log("Starting emulator '%s'" % emulatorCfg['name'], 1)
                    self._addEmulator(emulatorCfg)
                    
                outputFormat = RacktivityAutoTestPubishFormat.getByName(self._getConfig("logformat", "CONSOLE"))
                
                testRunnerFormat = None 
                if outputFormat == RacktivityAutoTestPubishFormat.CONSOLE:
                    testRunnerFormat = q.enumerators.TestRunnerOutputFormat.CONSOLE
                else:
                    testRunnerFormat = q.enumerators.TestRunnerOutputFormat.XML
                    
                q.testrunner.run(testcase, testRunnerFormat, self._getConfig("logdir", None))
        except Exception, e:
            q.logger.log("Error while running stage '%s' : %s" % (stage, e), 1)
            raise e
        finally:
            if stage == stages:
                #tear down on last stage.
                if te:
                    te.execute(params, tags=("test", "teardown"))
                
                #stop/remove emulators.
                for emulator in emulators:
                    self._removeEmulator(emulator)
            
            return stages - stage
    
    def list(self):
        return q.system.fs.listDirsInDir(SCENARIOS_PATH, dirNameOnly=True)
    
    def run(self, testscenario="", stage=1):
        """
        Run the testscenarios listed in the testscenario parameter
        """
        if not testscenario:
            testscenario = self._getConfig("testscenario", '')
        
        if not testscenario:
            raise ValueError("No test scenario to run")
        
        q.logger.log("Starting scenario '%s' stage '%s'" % (testscenario, stage), 1)
        if self._startScenarion(testscenario, int(stage)):
            exit(2)
    
    def publishTestResultsAndLogs(self, publishType=RacktivityAutoTestPubishFormat.FILESYSTEM, summaryType=RacktivityAutoTestPubishFormat.CONSOLE):
        """
        Publish the latest testresults and logs to the filesystem/console or a external service
        """
        pass