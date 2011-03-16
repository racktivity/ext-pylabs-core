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

'''Code to bind the applicationserver into the pylabs framework

This sets up logging, event handling, configuration reading and others.
'''

import os
import sys
import time
import xmlrpclib
import socket

from twisted.internet import reactor
from twisted.python.threadpool import ThreadPool

from pylabs import q
from pylabs.baseclasses import BaseEnumeration
from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from applicationserver import CRON_JOB_STOP

# Defines
DICT_SEPARATOR = ':'
DEFAULT_NAME = 'application_server__'
SERVICE_ROOT = q.system.fs.joinPaths(q.dirs.baseDir, 'apps',
                                     'applicationserver', 'services')
if not q.system.fs.isDir(SERVICE_ROOT):
    q.system.fs.createDir(SERVICE_ROOT)

# Enums
class ApplicationserverStatus(BaseEnumeration):
    pass
ApplicationserverStatus.registerItem('INITIALIZING')
ApplicationserverStatus.registerItem('RUNNING')
ApplicationserverStatus.registerItem('NOT_RUNNING')
ApplicationserverStatus.registerItem('NOT_CONFIGURED')
ApplicationserverStatus.registerItem('INCONSISTENT')
ApplicationserverStatus.registerItem('UNKNOWN')
ApplicationserverStatus.registerItem('STOPPING')
ApplicationserverStatus.finishItemRegistration()

class ApplicationserverMailProtocol(BaseEnumeration):
    pass
ApplicationserverMailProtocol.registerItem('POP3')
#PmdMailProtocol.registerItem('IMAP')
ApplicationserverMailProtocol.finishItemRegistration()

# Exceptions
class ApplicationserverException(Exception):
    pass

class AlreadyObserving(ApplicationserverException):
    def __init__(self, subject):
        ApplicationserverException.__init__(self,
            "Trying to subscribe to already subscribed subject '%s'" % \
            subject)

# Config
class EventServer(object):
    """Event sending server mixin"""

    def __init__(self, subject):
        self._observers = list()
        self._subject = subject

    def subscribe(self, callback):
        """Subscribe to an event"""
        if callback in self._observers:
            raise AlreadyObserving(self)
        self._observers.append(callback)

    def fire(self, value):
        for observer in self._observers:
            result = observer(self._subject, value)
            if result:
                break

    @staticmethod
    def passThrough(fromEvent, toEvent):
        def func(subject, value):
            toEvent.fire(value)
        fromEvent.subscribe(func)

class SubscriberException(Exception):
    pass



class ApplicationserverConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = "applicationserver"
    DESCRIPTION = "Application server"

    def ask(self):
        self.dialogMessage("Applicationserver configuration")
        if (not q.manage.applicationserver.isRunning()) \
           or (self.state == self.ConfigMode.CHECKCONFIG):
            self.dialogAskString('xmlrpc_ip',
                                 'XMLRPC server listening IP address',
                                 default='127.0.0.1')
            self.dialogAskString('xmlrpc_port',
                                 'XMLRPC server listening IP port',
                                 default=8888)

            if not 'allow_none' in self.params:
                self.params['allow_none']=False

            self.dialogAskYesNo('allow_none', 'Allow None values in xmlrpc',default=False)

            self.dialogAskString('rest_ip',
                                 'IP address of the REST transport',
                                default=self.params['xmlrpc_ip'])
            self.dialogAskString('rest_port',
                                 'REST server listening IP port',
                                default=8889)
            if not 'amf_ip' in self.params:
                self.params['amf_ip'] = self.params['xmlrpc_ip']
            if not 'amf_port' in self.params:
                self.params['amf_port'] = 8899
            self.dialogAskString('amf_ip', 'IP address of the AMF transport',default=self.params['xmlrpc_ip'])
            self.dialogAskString('amf_port', 'AMF server listening IP port', default=8899)

        self.dialogAskString('mail_incoming_server', 'Incoming mail server')

        if self.params['mail_incoming_server']:
            # POP3 is hardcoded for now, until we support something else
            # as well
            self.params['mail_incoming_protocol'] = 'POP3'

            self.dialogAskString('mail_incoming_username',
                                 'Incoming mail username')
            self.dialogAskString('mail_incoming_password',
                                 'Incoming mail password')
            self.dialogAskYesNo('mail_incoming_ssl',
                                'Incoming mail server uses SSL')
            self.dialogAskInteger('mail_check_interval',
                                  'Mail poll interval (in seconds)', 60)

            self.dialogAskString('mail_outgoing_server',
                                 'Outgoing mail server')
            self.dialogAskString('mail_outgoing_username',
                                 'Outgoing mail username')
            self.dialogAskString('mail_outgoing_password',
                                 'Outgoing mail password')
            self.dialogAskYesNo('mail_outgoing_ssl',
                                'Outgoing mail server uses SSL')
            self.dialogAskString('mail_from_address',
                                 'Outgoing mail \'from\' address')

    def commit(self):
        q.manage.applicationserver.reload(printWarningIfNotRunning=False)

    def show(self):
        msg = ["XML-RPC: %(xmlrpc_ip)s:%(xmlrpc_port)s"]
        msg.append("REST: %(rest_ip)s:%(rest_port)s")
        if 'mail_incoming_username' in self.params:
            msg.append("Incoming Mail: %(mail_incoming_username)s @ %(mail_incoming_server)s, checked every %(mail_check_interval)s seconds, SSL: %(mail_incoming_ssl)s")
        if 'mail_outgoing_server' in self.params:
            msg.append("Outgoing Mail: %(mail_outgoing_username)s @ %(mail_outgoing_server)s as %(mail_from_address)s, SSL: %(mail_outgoing_ssl)s")
        q.gui.dialog.message("\n".join(msg) % self.params)

ApplicationserverConfigManagement = ItemSingleClass(ApplicationserverConfigManagementItem)

class ApplicationserverServiceConfigManagementItem(ConfigManagementItem):
    CONFIGTYPE = 'applicationserverservice'
    DESCRIPTION = 'Application server service'

    def ask(self):
        self.dialogAskString('classspec', 'Service implementation class spec')

    def commit(self):
        q.manage.applicationserver.reload(printWarningIfNotRunning=False)

    def show(self):
        q.gui.dialog.message("Service '%s' is served by '%s'" % (self.itemname, self.params["classspec"]))

ApplicationserverServiceConfigManagement = ItemGroupClass(ApplicationserverServiceConfigManagementItem)

ApplicationserverConfigManagement.services = ApplicationserverServiceConfigManagement()


import threading
import functools

from pydispatch import dispatcher as pydispatcher

from twisted.python.log import addObserver, removeObserver

from applicationserver import dispatcher, signals, crond

from pylabs.Application import Application

try:
    from twisted.python.log import textFromEventDict
except ImportError:
    from twisted.python import reflect
    #This comes from Twisted SVN r24858
    def textFromEventDict(eventDict):
        """
        Extract text from an event dict passed to a log observer. If it cannot
        handle the dict, it returns None.

        The possible keys of eventDict are:
         - C{message}: by default, it holds the final text. It's required, but
           can be empty if either C{isError} or C{format} is provided (the
           first having the priority).
         - C{isError}: boolean indicating the nature of the event.
         - C{failure}: L{failure.Failure} instance, required if the event is an
           error.
         - C{why}: if defined, used as header of the traceback in case of
           errors.
         - C{format}: string format used in place of C{message} to customize
           the event. It uses all keys present in C{eventDict} to format
           the text.
        Other keys will be used when applying the C{format}, or ignored.
        """
        edm = eventDict['message']
        if not edm:
            if eventDict['isError'] and 'failure' in eventDict:
                text = ((eventDict.get('why') or 'Unhandled Error')
                        + '\n' + eventDict['failure'].getTraceback())
            elif 'format' in eventDict:
                text = _safeFormat(eventDict['format'], eventDict)
            else:
                # we don't know how to log this
                return
        else:
            text = ' '.join(map(reflect.safe_str, edm))
        return text

class ThreadLocalApplication(object, Application):
    '''pylabs application type which keeps the application name per-thread

    Since the C{q} object is normally shared between threads per process, but
    services running in the applicationserver should have service-local
    logging names, we need to be able to store the C{q.application.appname}
    value per thread.

    This type stores this value in a thread-local store. It is hooked on the
    q object by the L{setup} function.
    '''
    def __init__(self):
        '''Initialize a new ThreadLocalApplication object'''
        self._store = threading.local()
        Application.__init__(self)
        self.default_appname = "Unknown"

    def _getAppname(self):
        '''Application name'''
        name = getattr(self._store, 'appname', self.default_appname)
        return name

    def _setAppname(self, name):
        self._store.appname = name

    appname = property(fget=_getAppname, fset=_setAppname)

    def _exithandler(self):
        # We want to shutdown nicely without yelling at the user, even though
        # q.application.stop didn't kill our process
        q.logger.close()

    def stop(self, *args, **kwargs):
        # We don't want q.application.stop to kill our process
        oldexit = os._exit
        # Monkey-patch os._exit with some harmless function
        os._exit = lambda *args, **kwargs: None
        Application.stop(self, *args, **kwargs)
        os._exit = oldexit


# Link Twisted logging to pylabs logging
class pylabsLogObserver:
    '''Observer for Twisted logs to hook in the pylabs log subsystem'''
    def emit(self, eventDict):
        from pylabs import q
        if eventDict['isError']:
            level = 3
        else:
            level = 6

        text = textFromEventDict(eventDict)
        if text is None:
            return

        q.logger.log(text, level)

    def start(self):
        addObserver(self.emit)

    def stop(self):
        removeObserver(self.emit)

# Dispatch method execution failures. Log them.
def log_method_failure(failure, request, service, method, args, kwargs):
    '''Log failure of a service method call'''
    parts = list()

    parts.append('Exception while calling service method %s.%s' %
        (service, method))
    parts.append('Args: %s' % (args if args else '()', ))
    parts.append('Kwargs: %r' % (kwargs, ))
    parts.append('Client IP: %s' % request.client_ip)
    parts.append('Exception:')
    parts.append(str(failure))

    msg = '\n'.join(parts)

    q.logger.log(msg, 4)

def handle_failure_event(failure):
    '''Handle a cron or method call failure as a pylabs event'''
    import traceback

    # Commented out for pylabs_core 4 compliance
    #from pylabs.enumerators import SeverityType

    type_, value, tb = failure.type, failure.value, failure.tb

    backtrace = '~ '.join(line for line in
            traceback.format_exception(type_, value, tb))

    q.eventhandler.raiseInfo(backtrace)


def log_cronjob_failure(service, func, failure):
    '''Log failure of a cron job execution'''
    parts = list()
    parts.append('Exception while running cronjob method %s.%s' % \
            (service, func.__name__))
    parts.append('Exception:')
    parts.append(str(failure))

    msg = '\n'.join(parts)

    q.logger.log(msg, 4)


# Set up pylabs stuff in applicationserver
def setup():
    '''Set up pylabs hooks in the applicationserver'''

    def _load_init():
        # Try to import init.py
        # This module can be provided by third parties
        # If it exists but fails to be imported, we die
        # If it doesn't exist, we don't care
        import inspect
        import os.path

        import applicationserver

        base = inspect.getfile(applicationserver)
        base = os.path.abspath(os.path.join(os.path.dirname(base), '..', '..'))
        initpath = os.path.join(base, 'init.py')

        if os.path.exists(initpath):
            q.logger.log('[PMBINDINGS] Trying to load custom init module', 4)
            import imp
            imp.load_source('_applicationserver_init', initpath)
        else:
            q.logger.log('No init module found', 6)

    # setup is called before forking. Load the custom init module after forking
    # so we prevent the user from having hard-to-debug threading issues and
    # alike
    reactor.addSystemEventTrigger('after', 'startup', _load_init)

    q.logger.log('Setting up pylabs bindings in the applicationserver', 6)

    q.application = ThreadLocalApplication()

    #reactor.addSystemEventTrigger('after', 'shutdown', q.application.stop)

    observer = pylabsLogObserver()
    observer.start()

    pydispatcher.connect(log_method_failure, sender=dispatcher,
            signal=signals.SERVICE_METHOD_EXCEPTION)
    pydispatcher.connect(handle_failure_event, sender=dispatcher,
            signal=signals.SERVICE_METHOD_EXCEPTION)

    pydispatcher.connect(log_cronjob_failure, sender=crond,
            signal=signals.CRONJOB_EXCEPTION)
    pydispatcher.connect(handle_failure_event, sender=crond,
            signal=signals.CRONJOB_EXCEPTION)

    q.application.default_appname = 'applicationserver'
    q.application.appname = 'applicationserver'

    # Add the applicationserver libexec folder
    sys.path.append(q.system.fs.joinPaths(
                        q.dirs.appDir, 'applicationserver', 'services'))
    #q.application.start()

    # Install pylabs2 tasklet runner
    pylabsTaskletRunner.install()

    # Setup pylabs at an appropriate time
    setup_pylabs_start_and_stop()


def setup_pylabs_start_and_stop():
    '''Hook into the Twisted reactor to start and stop pylabs

    We only want to start the pylabs application after reactor startup, and
    stop it before the reactor shuts down. This method registers some callables
    to achieve this.
    '''
    def _start():
        q.logger.log('[PMBINDINGS] Starting pylabs stuff', 3)
        q.application.start()

    def _stop():
        q.logger.log('[PMBINDINGS] Stopping pylabs stuff', 3)
        q.application.stop()

    reactor.addSystemEventTrigger('after', 'startup', _start)
    reactor.addSystemEventTrigger('before', 'shutdown', _stop)


def _run_with_logger(func, *args, **kwargs):
    '''Decorator to change a callable to set up pylabs logging names'''
    from pylabs import q

    oldname = q.application.appname
    kwargs = kwargs.copy()
    try:
        service_name = '%s:%s' % (oldname,
                kwargs.pop(EXPOSED_SERVICE_NAME_KWARG))
    except KeyError:
        service_name = oldname

    q.application.appname = service_name

    try:
        res = func(*args, **kwargs)
    finally:
        q.application.appname = oldname

    return res


from applicationserver.dispatcher import tag_exposed, tag_expose_authenticated, tag_expose_authorized, not_threaded
from applicationserver.dispatcher import EXPOSED_SERVICE_NAME_KWARG

def expose(func):
    func = tag_exposed(func)

    @functools.wraps(func)
    def exposed_func(*args, **kwargs):
        return _run_with_logger(func, *args, **kwargs)

    return exposed_func

from applicationserver.dispatcher import expose as _expose
expose.__doc__ = _expose.__doc__

def expose_authenticated(func):
    return tag_expose_authenticated(expose(func))

from applicationserver.dispatcher import expose_authorized

from applicationserver.dispatcher import expose_authenticated as \
        _expose_authenticated
expose_authenticated.__doc__ = _expose_authenticated.__doc__

from applicationserver.cron import Job, CronJob

class pylabsJob(Job):
    def __call__(self, *args, **kwargs):
        return _run_with_logger(self.func, *args, **kwargs)

class pylabsCronJob(CronJob):
    JOBCLASS = pylabsJob

cronjob = pylabsCronJob

from applicationserver.services import service_close_handler \
        as _service_close_handler

def service_close_handler(func):
    func = _service_close_handler(func)
    
    @functools.wraps(func)
    def logged_func(*args, **kwargs):
        return _run_with_logger(func, *args, **kwargs)
    
    return logged_func
        
#TaskletRunner implementation for pylabs2 tasklets
import Queue

from twisted.python import log

from .taskletrunner import TaskletRunner

class _FakeFailure:
    def __init__(self, type_, value, tb):
        self.type = type_
        self.value = value
        self.tb = tb

class TaskletRunnerThread(object):
    def __init__(self, queue):
        self.queue = queue
        self.keep_running = True

    def run(self):
        #As long as we should be running...
        while self.keep_running:
            try:
                #Fetch an item from the queue, timeout on 0.5s
                engine, execute_args = self.queue.get(timeout=0.5)
            except Queue.Empty:
                #Queue.Empty is raised if the timeout is passed
                #Catch it, and restart our loop
                continue

            #Call all functions, handle any exception they throw
            q.logger.log(
                'Got tasklet execution call from queue, starting execution', 6)

            # If tasklet execution fails, raising some exception, the
            # current thread will be stopped. This is, obviously, not the
            # desired behavior.
            # The handling of the 'tb' variable might seem strange, we need this
            # to help the Python garbage collector somewhat though. See the
            # documentation of sys.exc_info for more information.
            tb = None
            try:
                engine.execute(**execute_args)
            except:
                q.logger.log('Tasklet execution failed', 1)
                type_, exc, tb = sys.exc_info()
                if (type_, exc, tb) is not (None, None, None):
                    # We want to reuse handle_failure_event which expects a
                    # failure object from somewhere inside Twisted.
                    # Using a fake failure object providing the same interface
                    # (well, the interface used inside handle_failure_event)
                    # should allow us to do this.
                    failure = _FakeFailure(type_, exc, tb)
                    try:
                        handle_failure_event(failure)
                    except:
                        q.logger.log(
                            'Exception during exception handling', 1)
                        # If this is reached, the current thread will stop
                        # running, which might not exactly be desired, but if we
                        # arrive here things are going very very wrong already,
                        # so we don't really care.
                        raise
            finally:
                if tb:
                    del tb
            # This is intentional
            tb = None


class pylabsTaskletRunner(TaskletRunner):
    def __init__(self, engine, threadpoolsize=10):
        self.engine = engine
        # Job queue
        self._queue = Queue.Queue()
        # Threadpool
        self._runners = list()
        self._threadpool = None

        reactor.addSystemEventTrigger('after', 'startup', self.start,
                                      threadpoolsize)
        reactor.addSystemEventTrigger('before', 'shutdown',
                                      self.shutdown)

    def start(self, threadpoolsize):
        self._threadpool = ThreadPool(minthreads=threadpoolsize,
                                      maxthreads=threadpoolsize + 1)

        # Set up threadpool
        q.logger.log('[PMTASKLETS] Constructing taskletserver threadpool', 6)
        self._threadpool.start()
        for i in xrange(threadpoolsize):
            runner = TaskletRunnerThread(self._queue)
            self._runners.append(runner)
            self._threadpool.callInThread(runner.run)

        self._running = True


    def queue(self, params, author=None, name=None, tags=None, priority=-1,
              logname=None):
        author = author or '*'
        name = name or '*'
        tags = tags or list()
        priority = priority if priority > -1 else -1

        q.logger.log('[PMTASKLETS] Queue: params=%s, author=%s, name=%s, '
                     'tags=%s, priority=%d' % \
                     (params, author, name, tags, priority), 4)

        # Wrap the tasklet executor methods so the appname (for logging) is set
        # correctly
        def logwrapper(func):
            @functools.wraps(func)
            def _wrapped(*args, **kwargs):
                import pylabs

                oldappname = pylabs.q.application.appname
                if logname:
                    pylabs.q.application.appname = \
                            'applicationserver:pmtasklets:%s' % logname
                else:
                    pylabs.q.application.appname = \
                            'applicationserver:pmtasklets'

                try:
                    ret = func(*args, **kwargs)
                finally:
                    pylabs.q.application.appname = oldappname

                return ret

            return _wrapped

        execute_args = {
            'author': author,
            'name': name,
            'tags': tags,
            'priority': priority,
            'params': params,
            'wrapper': logwrapper,
        }

        #Append list of tasklet methods to run to the queue
        self._queue.put((self.engine, execute_args, ))

    def shutdown(self):
        q.logger.log('Shutting down tasklet runner', 5)
        self._running = False

        #Tell all threads to stop running
        for runner in self._runners:
            runner.keep_running = False

        self._threadpool.stop()

    @classmethod
    def install(cls):
        log.msg('Installing pylabs tasklet runner')
        import applicationserver

        applicationserver.TaskletRunner = cls


def getConfig(name, configtype):
    items = name.split(".", 1)
    if len(items) > 1:
        path = q.system.fs.joinPaths(q.dirs.baseDir, items[1], 'cfg', '%s.cfg' % configtype)
        ini = q.tools.inifile.open(path)
        return ini.getFileAsDict()
    else:
        return q.config.getConfig(configtype)

class Server:
    """
    Management functionality for an applicationserver
    """

    #decorators
    expose = staticmethod(expose)
    expose_authenticated = staticmethod(expose_authenticated)
    expose_authorized    = staticmethod(expose_authorized)
    not_threaded = staticmethod(not_threaded)
    cronjob = staticmethod(cronjob)
    CRON_JOB_STOP = CRON_JOB_STOP
    service_close_handler = staticmethod(service_close_handler)

    def _checkName(self, name):
        if not name:
            name = "applicationserver"
        else:
            if not name.startswith("applicationserver"):
                name = "applicationserver.%s" % name
        return name

    def start(self, name=None):
        """
        Start this applicationserver

        @param atreboot: Check the main.startatreboot setting before starting
        @type atreboot: bool
        """
        name = self._checkName(name)
        if self.isRunning(name):
            q.console.echo("Server %s is already running" % name)
            return

        # xmlrpc_port must be > 0
        if int(getConfig(name, 'applicationserver')['main'] \
               ['xmlrpc_port']) <= 0:
            raise ApplicationserverException(
                "xmlrpc.port must be set before starting the server")

        q.console.echo("Starting %s..." % name)

        # Needed to put the folder with twisted/plugins/ in it into the pythonpath
        applicationserver_dir = q.system.fs.joinPaths(q.dirs.baseDir, 'apps',
                                                      'applicationserver', 'lib')
        # pid, log
        pidfile = self._getPIDFilename(name)
        logfile = q.system.fs.joinPaths(q.dirs.logDir, '%s.log' % name)

        # If twisted was killed by eg power failure, stale pidfile should be removed
        if q.system.fs.exists(pidfile):
            pid = q.system.fs.fileGetContents(pidfile)

            if pid and pid.isdigit() and q.system.process.isPidAlive(int(pid)):
                raise 'Pid found in (old) pidfile "%s" is still running.' % pidfile
            else:
                q.system.fs.remove(pidfile)


        # Start a twistd
        os.environ['TWISTED_NAME'] = name
        if not q.platform.isWindows():
            # This code is suboptimal since it overrules previously-set values
            # of PYTHONPATH, which might not be the intention
            tacfile = q.system.fs.joinPaths(applicationserver_dir, 'applicationserver.tac')
            code, stdout, stderr = q.system.process.run(
                "PYTHONPATH=\"%s\" %s "
                "--pidfile=%s -y %s --savestats"% (
                    applicationserver_dir,
                    q.system.fs.joinPaths(q.dirs.binDir, 'twistd'),
                    pidfile,
                    tacfile,
                ),
                showOutput=False,
                captureOutput=True,
                stopOnError=False,
            )
        else:
            # Windows hack
            cmd = q.system.fs.joinPaths(
                os.environ['PYTHONHOME'], 'pythonw.exe')
            args = (
                cmd,
                q.system.fs.joinPaths(q.dirs.binDir, 'twistd'),
                '-l', logfile,
                'applicationserver',
                '--config=applicationserver',
            )

            # This code is suboptimal since it overrules previously-set values
            # of PYTHONPATH, which might not be the intention
            twistd_env = os.environ.copy()
            twistd_env['PYTHONPATH'] = applicationserver_dir
            args = list(args) + [twistd_env]

            pid = os.spawnle(os.P_NOWAIT, cmd, *args)
            # TODO Figure out how to test sucess etc, This doesn't work:
            # Give the process the time to start
            #time.sleep(0.5)
            # Check PID
            #code = q.system.windows.checkProcessForPid('pythonw.exe', pid)
            #stdout = stderr = '(unknown)'
            code = 0


        if code != 0:
            raise ApplicationserverException(
                "Server exited with code %d\nStdout:%s\nStderr:%s" % \
                (code, stdout, stderr)
            )

    def stop(self, name=None):
        """
        Stop this applicationserver
        """
        name = self._checkName(name)
        q.console.echo("Stopping %s..." % name)
        self._callWithStatusCheck('stop', self._getProxy(name).stopServer)

        # same way as the restart() function
        countdown = 5
        pidfile = self._getPIDFilename(name)
        pid = int(q.system.fs.fileGetContents(pidfile)) if q.system.fs.isFile(pidfile) else None
        while countdown and (self.isRunning(name) or (pid and q.system.process.isPidAlive(pid))):
            q.console.echo("%s is still running, waiting for %d more seconds" % (name, countdown))
            time.sleep(1)
            countdown -= 1

        if countdown == 0:
            if pid:
                q.console.echo("%s with pid [%s] is still alive, killing it..." % (name,pid))
                q.system.process.kill(pid)

    def restart(self, name=None):
        """
        Restart this applicationserver
        """
        name = self._checkName(name)
        q.console.echo("Restarting %s..." % name)
        self.stop()

        pidfile = self._getPIDFilename(name)
        countdown = 5
        # Check both using XMLRPC (isRunning()) and the PID file. If the PID
        # file is present, the server is still shutting down.
        pid = int(q.system.fs.fileGetContents(pidfile)) if q.system.fs.isFile(pidfile) else None
        while countdown and \
              (self.isRunning() or (pid and q.system.process.isPidAlive(pid))):
            q.console.echo("%s is still running, waiting for %d more seconds" % (name, countdown))
            time.sleep(1)
            countdown -= 1

        if countdown == 0:
            if not pid:
                q.gui.dialog.message("Failed to stop %s" % name)
                return
            q.gui.dialog.message('Killing process %s'%pid)
            q.system.process.kill(pid)

        self.start()

    def reload(self, printWarningIfNotRunning=True, name=None):
        """
        Reload the services of this applicationserver. Enabled services will
        be loaded. Disabled services will be unloaded. Transport settings
        will _NOT_ be applied.

        A change in transport settings (xmlrpc, rest, mail) requires a server
        restart.
        """
        name = self._checkName(name)
        self._callWithStatusCheck('reload', self._getProxy(name).reloadConfig, printWarningIfNotRunning)
         

    def _callWithStatusCheck(self, commandname, func, printWarning=True):
        status = self.checkStatus()
        if status == ApplicationserverStatus.RUNNING:
            func()
        elif status == ApplicationserverStatus.UNKNOWN:
            if printWarning:
                q.console.echo("Status is unknown for server %s. Trying to %s server anyway" % (self, commandname))
            func()
        elif status == ApplicationserverStatus.NOT_RUNNING:
            if printWarning:
                q.console.echo("Server %s is not running. Cannot %s server" % (self, commandname))
        elif status == ApplicationserverStatus.NOT_CONFIGURED:
            if printWarning:
                q.console.echo("Server %s is not configured. Cannot %s server. Please call i.servers.applicationserver.review()." % (self, commandname))
        else:
            if printWarning:
                q.console.echo("Cannot %s server %s in status %s" % (commandname, self, status))

    def checkStatus(self, name=None):
        """
        Check the status of this applicationserver

        @return: The status of this applicationserver
        @rtype: L{applicationserver.pylabs_bindings.ApplicationserverStatus}
        """
        name = self._checkName(name)
        config = getConfig(name, 'applicationserver')
        if 'main' not in config:  # INI-file is empty, applicationserver isn't configured yet.
            return ApplicationserverStatus.NOT_CONFIGURED
        proxy = self._getProxy(name)
        try:
            status_string = proxy.getStatus()
            status = ApplicationserverStatus.getByName(status_string)
        except socket.error, e:
            # Server is propably not running
            # TODO: check pid?
            return ApplicationserverStatus.NOT_RUNNING
        except (xmlrpclib.Fault, xmlrpclib.ProtocolError), e:
            # Server exists, but method not found?
            # Or some other server is running on that port
            q.eventhandler.raiseWarning(
                "%s is in UNKNOWN status" % name)
            return ApplicationserverStatus.UNKNOWN
        except KeyError, e:
            q.eventhandler.raiseWarning(
                "%s is in UNKNOWN status: %s" % (name, e))
            return ApplicationserverStatus.UNKNOWN
        return status

    def isRunning(self, name=None):
        """
        Check whether or not this applicationserver is running
        """
        name = self._checkName(name)
        running = bool(self.checkStatus(name) == ApplicationserverStatus.RUNNING)
        return running

    def listServices(self, name):
        """
        List of deployed applications
        """
        name = self._checkName(name)
        q.console.echo("List of deployed services")
        proxy = self._getProxy(name)
        try:
            status_string = proxy.getStatus()
            ApplicationserverStatus.getByName(status_string)
        except socket.error:
            # Server is propably not running
            # TODO: check pid?
            return ApplicationserverStatus.NOT_RUNNING
        return proxy.listServices()

    def reloadService(self, appName,targetRole='restart', name=None):
        """
        Reload the specificied service on the application server

        @param appName: The appName can be retrieved via q.manage.applicationserver.listServices()
        @param targetRole: restart,stop,start
        """
        name = self._checkName(name)
        q.console.echo("Reloading service %s" % appName)
        proxy = self._getProxy(name)
        try:
            status_string = proxy.getStatus()
            ApplicationserverStatus.getByName(status_string)
        except socket.error:
            # Server is propably not running
            # TODO: check pid?
            return ApplicationserverStatus.NOT_RUNNING
        return proxy.reloadService(appName,targetRole)

    def _getProxy(self, name=None):
        name = self._checkName(name)
        config = getConfig(name, 'applicationserver')
        ip = config['main'] \
                ['xmlrpc_ip']
        portAsString = config['main']['xmlrpc_port']
        port = int(portAsString) if portAsString else 0
        return xmlrpclib.Server('http://%s:%d/' % (ip, port))._controller

    def _getPIDFilename(self, name=None):
        name = self._checkName(name)
        return q.system.fs.joinPaths(q.dirs.pidDir, '%s.pid' % name)

    def __str__(self):
        return "Applicationserver"

    def __repr__(self):
        return str(self)
