# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

'''pylabs framework central class (of which the C{q} object is an instance)'''

import sys
import inspect
import os
import imp
import random
if not (sys.platform.startswith("win32") or sys.platform.startswith("linux")  or sys.platform.startswith("darwin") or sys.platform.startswith("sunos")):
    print "pylabs framework is only supported on win32, darwin and linux*. Current platform is [%s]. " % (sys.platform)
    sys.exit(1)

import pylabs

from Dirs import Dirs
from pylabs.base.time.Time import Time
from pylabs.base.idgenerator.IDGenerator import IDGenerator
##from pylabs.enumerators.QPackageQualityLevelType import QPackageQualityLevelType

from pylabs.extensions.PMExtensions import PMExtensions

#We'll only lazy-load all attributes here to save memory and launch time
_DUMMY = object()
class pylabsContainerAttributeDescriptor(object):
    def __init__(self, name, generator):
        self.name = name
        self.generator = generator

    def get_attribute_container(self, obj):
        if not hasattr(obj, '_lazy_attribute_container'):
            obj._lazy_attribute_container = dict()

        return obj._lazy_attribute_container

    def __get__(self, obj, type_=None):
        container = self.get_attribute_container(obj)

        ret = container.get(self.name, _DUMMY)

        if ret is _DUMMY:
            ret = self.generator()
            container[self.name] = ret

        # Overwrite class attribute (this descriptor) in instance dict
        setattr(obj, self.name, ret)
        return ret

    def __set__(self, obj, value):
        self.get_attribute_container(obj)[self.name] = value

    def __delete__(self, obj):
        raise RuntimeError('This attribute can not be deleted')


def _pylabs_system():
    from System import System
    return System()

def _pylabs_logger():
    from pylabs.logging.LogHandler import LogHandler
    return LogHandler()

def _pylabs_eventhandler():
    from pylabs.logging.EventHandler import EventHandler
    return EventHandler()

def _pylabs_messagehandler():
    from pylabs.messages.MessageHandler import MessageHandler
    return MessageHandler()

def _pylabs_application():
    from Application import Application
    return Application()

def _pylabs_vars():
    from pylabs.Vars import Vars
    return Vars

def _pylabs_platform():
    from pylabs.enumerators.PlatformType import PlatformType
    return PlatformType.findPlatformType()

def _pylabs_cmdb():
    from pylabs.cmdb import CMDB
    return CMDB()

def _pylabs_transaction():
    from pylabs.transaction.TransactionController import TransactionController
    return TransactionController()

def _pylabs_action():
    from pylabs.action import ActionController
    return ActionController()

def _pylabs_console():
    from pylabs.console import Console
    return Console()

def _pylabs_extensions():
    import pylabs.extensions.management
    return pylabs.extensions.management

def _pylabs_qshellconfig():
    from pylabs.qshellconfig.QShellConfig import QShellConfig
    return QShellConfig()

def _pylabs_tools():
    from pylabs.Tools import Tools
    return Tools

def _pylabs_clients():
    from pylabs.clients.Clients import Clients
    return Clients()

def _pylabs_enumerators():
    from pylabs.baseclasses.BaseEnumeration import enumerations
    return enumerations

def _pylabs_errorconditionhandler():
    from pylabs.messages.ErrorconditionHandler import ErrorconditionHandler
    return ErrorconditionHandler()

def _pylabs_config():
    from pylabs.config.QConfig import QConfig
    return QConfig()

def _pylabs_gui():
    from pylabs.gui.Gui import Gui
    return Gui()

def _pylabs_debugger():
    from pylabs.debugger import QHook
    return QHook()


def _pylabs_qpackagetools():
    from pylabs.qpackages.client.QPackageTools import QPackageTools
    return QPackageTools()


class Pylabs:
    '''Central pylabs framework class, of which C{q} is an instance'''
    # Construct the singleton objects
    system = pylabsContainerAttributeDescriptor('system',_pylabs_system)
    '''Accessor to system methods'''

    logger = pylabsContainerAttributeDescriptor('logger',_pylabs_logger)
    '''Accessor to logging methods'''

    eventhandler = pylabsContainerAttributeDescriptor('eventhandler',_pylabs_eventhandler)
    '''Accessor to event handling methods'''

    application = pylabsContainerAttributeDescriptor('application',_pylabs_application)
    '''Accessor to application methods'''

    #TODO Somehow the pylabsContainerAttributeDescriptor trick can't be used
    #on the dirs attribute (test.system.test_fs.TestDirs.test_dir fails).
    dirs = Dirs()
    '''Accessor to directory configuration'''

    vars = pylabsContainerAttributeDescriptor('vars',_pylabs_vars)
    '''Accessor to shared variables'''

    platform = pylabsContainerAttributeDescriptor('platform',_pylabs_platform)
    '''Accessor to current platform information'''

    cmdb = pylabsContainerAttributeDescriptor('cmdb', _pylabs_cmdb)
    '''Accessor to the pylabs CMDB subsystem'''


    transaction = pylabsContainerAttributeDescriptor('transaction',_pylabs_transaction)
    '''Accessor to the pylabs transaction methods'''

    action = pylabsContainerAttributeDescriptor('action',_pylabs_action)
    '''Accessor to the pylabs action methods'''

    console = pylabsContainerAttributeDescriptor('console',_pylabs_console)
    ''' Accessor to the pylabs console methods'''

    extensions = pylabsContainerAttributeDescriptor('extensions',
            _pylabs_extensions)
    '''Extension management methods'''

    qshellconfig = pylabsContainerAttributeDescriptor('qshellconfig',_pylabs_qshellconfig)

    _extensionsInited = False
    '''Whether extensions are initialized'''
    _pmExtensions = None
    '''List of discovered extensions'''

    tools = pylabsContainerAttributeDescriptor('tools', _pylabs_tools)
    '''Accessor to pylabs tools'''

    clients = pylabsContainerAttributeDescriptor('clients',_pylabs_clients)
    ''' Accessor to client applications '''

    enumerators = pylabsContainerAttributeDescriptor('enumerators',_pylabs_enumerators)
    '''Accessor to all registered enumeration types'''

    config = pylabsContainerAttributeDescriptor('config',_pylabs_config)

    gui = pylabsContainerAttributeDescriptor('gui',_pylabs_gui)

    debugger = pylabsContainerAttributeDescriptor('debugger',_pylabs_debugger)

    qpackagetools = pylabsContainerAttributeDescriptor('qpackagetools',_pylabs_qpackagetools)
    
    messagehandler = pylabsContainerAttributeDescriptor('messagehandler',_pylabs_messagehandler)

    errorconditionhandler = pylabsContainerAttributeDescriptor('errorconditionhandler',_pylabs_errorconditionhandler)



    def __init__(self):
        q = getattr(pylabs, 'q', None)
        if q and q is not self:
            raise RuntimeError('Creating a second pylabs instance')
        self._init_called = False
        self._init_final_called = False
        self.agentid="@"

    @staticmethod
    def getTaskletEngine(path=None):
        '''Get a tasklet engine instance

        If a C{path} is provided, this is passed to the C{addFromPath} method of
        the new tasklet engine.

        @param path: Path passed to addFromPath
        @type path: string

        @return: A tasklet engine
        @rtype: L{pylabs.tasklets.TaskletsEngine}
        '''
        from pylabs.taskletengine.TaskletEngine4 import TaskletEngine4

        engine = TaskletEngine4(path)

        return engine


    def init(self):
        """
        Core pylabs functionality.
        You cannot use q.dirs in here since it is not yet configured
        """
        if self._init_called:
            raise RuntimeError('q.init already called. Are you re-importing '
                                'pylabs.InitBase*?')

        #We want to do this asap
        self.basetype = pylabs.pmtypes.register_types()
        class _dummy: pass
        d = _dummy()
        setattr(d, 'time', Time())
        setattr(d, 'idgenerator', IDGenerator())
        self.base = d
        self.eventhandler.__init__()
        self.errorconditionhandler.__init__()
        self._init_called = True

    def init_final(self): #@remark not lin line with pylabs code conventions
        '''Initializations which depend on other initializations should go here'''
        agentconfig=pylabs.q.config.getInifile("main")
        agentconfig.addSection("main")
        if agentconfig.checkParam("main","nodename")==False:
            agentconfig.setParam("main","nodename","unknown")
        if agentconfig.checkParam("main","domain")==False:
            agentconfig.setParam("main","domain","somewhere.com")

        self.agentid="%s.%s" % (agentconfig.getValue("main","nodename"),agentconfig.getValue("main","domain"))
        pylabs.q.application.agentid = self.agentid

        
        if len(pylabs.q.application.agentid)<5:
            raise RuntimeError("nodename and domain in $qbase/cfg/qconfig/main.cfg is not properly filled in, current id %s" % pylabs.q.application.agentid)

        if self._init_final_called:
            raise RuntimeError('q.init_final already called. Are you '
                               're-importing pylabs.InitBase*?')

        self.vars.pm_setSystemVars()

        self._initExtensionsIfNotDoneYet()
        self.qshellconfig.refresh()
        self.gui.dialog.pm_setDialogHandler()
        pylabs.q.logger._init()
        self._init_final_called = True


    def enablepylabsTrace(self):
        '''Enable tracing in pylabs methods'''
        file = inspect.getfile(System)
        folder = os.path.dirname(file)
        files = os.listdir(folder)
        for f in files:
            if not f.endswith(".py"):
                continue
            if f.endswith("Logger.py"):
                continue
            if f.endswith("LogHandler.py"):
                continue
            if f.endswith("LogServer.py"):
                continue
            mod = __import__(os.path.splitext(os.path.basename(f))[0], globals(), locals(), "*")
            self.logger.logModuleUsage(mod, 10)

    def _initExtensionsIfNotDoneYet(self):
        '''Initialize pylabs extensions if they are not initialized yet'''
        if not self._extensionsInited:
            self._initDynamicExtensions()
            self._extensionsInited = True

    def _initDynamicExtensions(self):
        '''Initialize all extensions in self.dirs.extensionDir'''
        self.logger.log('Loading pylabs extensions from %s' % self.dirs.extensionsDir, 7)

        if not self.dirs.extensionsDir or not os.path.exists(self.dirs.extensionsDir):
            self.logger.log('Extension path %s does not exist, unable to load extensions' % self.dirs.extensionsDir, 6)
            return
        self._pmExtensions = PMExtensions(pylabs.q, 'q.')
        self._pmExtensions.init()
        self._pmExtensions.findExtensions()
