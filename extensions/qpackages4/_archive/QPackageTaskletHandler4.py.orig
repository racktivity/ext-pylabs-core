
from pymonkey import q
from pymonkey.baseclasses import BaseType
from pymonkey.enumerators.PlatformType import PlatformType
from pymonkey.baseclasses.dirtyflaggingmixin import DirtyFlaggingMixin
from enumerators4 import QPackageQualityLevelType4
from DependencyDef4 import DependencyDef4
#from enumerators4 import DependencyType4
from pymonkey.Shell import *


class QPackageTaskletHandler4():
    ''' 
    methods to execute tasklets on qpackage
    '''
    def _executeTasklet(self, qpackageObject, tag):
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=(tag,)):
            q.logger.log('No tasklets found with matching tags (\'%s\',)'%tag, 3)
            return
        engine.execute(params={'qpackage':qpackageObject}, tags=(tag,))
        
    def _executeTasklet(self,qpackage):
                engine = self._createTaskletEngine(qpackageObject)

        if i.qpackageLocalConfig.isQPackageInDevMode(qpackageObject.domain, qpackageObject.name, qpackageObject.version):
            self.build(qpackageObject)
            return

        if not engine.find(tags=('install',)):
            raise RuntimeError('No tasklets found with matching tags (\'install\',)')

        q.action.start('Installing QPackage %s'%qpackageObject.name)
        q.qshellconfig.interactive = True #allows interactive questions
        q.action.start('Executing Install Tasklet of QPackage %s'%qpackageObject.name)

        q.logger.log('Executing Install Tasklet of QPackage %s'%qpackageObject.name, 7)
        engine.execute(params={'qpackage':qpackageObject}, tags=('install',))

        q.logger.log('Updating QPackage inifile', 7)
        
        q.extensions.pm_sync()

        q.action.stop()
        q.action.stop()

    def start(self, qpackageObject):
        """
        Calls the start-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'start')

    def stop(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'stop')

    def _executeTasklet(self, qpackageObject, tag):
        engine = self._createTaskletEngine(qpackageObject)
        if not engine.find(tags=(tag,)):
            q.logger.log('No tasklets found with matching tags (\'%s\',)'%tag, 3)
            return
        engine.execute(params={'qpackage':qpackageObject}, tags=(tag,))

    def restart(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'restart')

    def getStatus(self, qpackageObject):
        """
        Calls the stop-tasklet of the qpackage.
        @param qpackageObject: qpackage object
        """
        self._executeTasklet(qpackageObject, 'getStatus')

    def _createTaskletEngine(self, qpackageObject):
        """
        Create tasklet engine for this qpackage object.
        It always prefers the upload_<qualityLevel> dir over the <buildNr> dir
        @param qpackageObject: qpackage object
        """
        taskletsDirs = self._getTaskletsPlatformDirs(qpackageObject.domain, qpackageObject.name, qpackageObject.version, qpackageObject.buildNr)

        q.logger.log("Instantiating tasklet engine", 9)
        engine = TaskletsEngine()
        for taskletDir in taskletsDirs:
            q.logger.log("Adding tasklet dir [%s] to tasklet engine" % taskletDir, 10)
            engine.addFromPath(taskletDir)
        return engine        