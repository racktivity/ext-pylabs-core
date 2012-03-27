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

'''Implementation of the applicationserver cron job manager/scheduler'''

import threading
import functools
import time

from pydispatch import dispatcher as pydispatcher

from twisted.internet import threads, reactor
from twisted.python import log

from applicationserver.utils import attrchecker, service_method_caller
from applicationserver.dispatcher import EXPOSED_SERVICE_NAME_KWARG
from applicationserver import signals

CRON_ATTRIBUTE = 'applicationserver_cron'

class _dummy: pass

'''Variable returned by a cron job if it doesn't need to be rescheduled'''
CRON_JOB_STOP = _dummy()

class Job:
    '''Implementation of a single cron job'''
    def __init__(self, func, timeout):
        '''Initialize a new job

        @param func: Function to execute
        @type func: callable
        @param timeout: Timeout (in seconds) between job invocations
        @type timeout: number
        '''
        self.timeout = timeout
        self.calibrate_time = None
        # Simple threadlock used to make sure the cronjob won't be started
        # more than once concurrently
        self.lock = threading.Lock()
        # Some state information
        self.disabled = False
        # Store the return value of Twisted's callLater so we can cancel a
        # pending call when the job needs to be stopped/disabled. This variable
        # will hold a Twisted object we can use to disable a future function
        # call, installed in Job.register.
        self.delayed_call = None
        self.service_name = '<unknown>'
        self.func = func

    def __call__(self, *args, **kwargs):
        '''Execute the job function'''
        #We need this because otherwise the decorated method would not be
        #callable anymore at all, not even by 'external' callers (outside the
        #applicationserver).
        #We pop out the EXPOSED_SERVICE_NAME kwarg (hoping it is never used by
        #a consumer) since we don't need it here (logging should be set up
        #correctly already).
        kwargs = kwargs.copy()
        try:
            kwargs.pop(EXPOSED_SERVICE_NAME_KWARG)
        except KeyError:
            pass

        return self.func(*args, **kwargs)

    def run(self, object_):
        '''Run the job once, reschedule after completion'''
        #Don't run if currently disabled
        if self.disabled:
            return

        log.msg('[CRONJOB] About to run job %s:%s' % (self.service_name,
                                                      self.func.__name__))

        #Don't run if currently locked
        if self.lock.locked():
            log.err('[CRONJOB] Job %s:%s is locked, not restarting' % \
                    (self.service_name, self.func.__name__))
            return

        self.lock.acquire()

        #Set up logging source stuff
        func = service_method_caller(self.service_name, self,
                wraps=False)
        log.msg('[CRONJOB] Running %s:%s in thread' % (self.service_name,
                                                       self.func.__name__))
        dt = threads.deferToThread(func, object_)

        def callback(data):
            log.msg('[CRONJOB] Job %s:%s returned \'%r\'' % \
                    (self.service_name, self.func.__name__, data))

            if data is not CRON_JOB_STOP:
                self.register(self.service_name, object_)
            else:
                log.msg('[CRONJON] Stop job %s:%s' % (self.service_name,
                                                 self.func.__name__))

            self.lock.release()

        def errback(failure):
            log.err('[CRONJOB] Job %s:%s execution failed: %s' % \
                    (self.service_name, self.func.__name__, failure))

            dispatchkwargs = {
                    'service': self.service_name,
                    'func': self.func,
                    'failure': failure,
            }

            import applicationserver
            pydispatcher.send(signal=signals.CRONJOB_EXCEPTION,
                    sender=applicationserver.crond, **dispatchkwargs)

            self.register(self.service_name, object_)

            self.lock.release()

            #Don't propagate exception
            return None

        dt.addCallback(callback)
        dt.addErrback(errback)

    def register(self, name, object_):
        '''Register the job on the system, schedule it for execution'''

        now = time.time()
        if not self.calibrate_time:
            self.calibrate_time = now
            timeout = self.timeout
        else:
            timeout = self.timeout - ((now - self.calibrate_time) % self.timeout)
        self.service_name = name
        self.delayed_call = reactor.callLater(timeout, self.run, object_)

    def disable(self):
        '''Disable/cancel the job'''
        log.msg('[CRONJOB] Disabling job %s:%s' % (self.service_name,
                                                   self.func.__name__))
        self.disabled = True
        if self.delayed_call and self.delayed_call.active():
            self.delayed_call.cancel()


class CronJob:
    '''Decorator to mark a method as a cronjob'''
    JOBCLASS = Job

    def __init__(self, timeout):
        '''Set up the decorator

        @param timeout: Timeout between job invocation (in seconds)
        @type timeout: number
        '''
        self.timeout = timeout

    def __call__(self, func):
        '''Decorator method'''
        func_ = self.JOBCLASS(func, self.timeout)
        return functools.wraps(func)(self.tag(func_))

    def tag(self, func):
        '''Set cron attribute on the decorated method

        This is only for internal usage.
        '''
        setattr(func, CRON_ATTRIBUTE, True)
        return func


class Crond:
    '''Cron daemon implementation'''
    def __init__(self):
        '''Initialize a new cron daemon'''
        log.msg('[CROND] Initializing')
        self.services = dict()

    def addService(self, name, service):
        '''Add a service class to the cron daemon

        @param name: Service name
        @type name: string
        @param service: Service instance to add
        @type service: object
        '''
        log.msg('[CROND] Adding service %s' % name)
        jobs = self.findJobs(service)
        for job in jobs:
            self.addJob(name, service, job)

    def findJobs(self, service):
        '''Find all cron jobs on a service

        @param service: Service for which jobs should be scheduled
        @type service: object
        '''
        log.msg('[CROND] Looking up all jobs on service %s' % \
                service.__class__.__name__)
        return (getattr(service, name) for name in dir(service) \
                if is_cronjob(getattr(service, name)))

    def addJob(self, name, service, func):
        '''Add a job to crond

        @param name: Service name
        @type name: string
        @param service: Service on which the job is defined
        @type service: object
        @param func: CronJob to add
        @type func: L{CronJob}
        '''
        if service not in self.services:
            self.services[service] = set()

        log.msg('[CROND] Registering job %s of service %s' % (func.__name__,
                                                              name))
        self.services[service].add(func)
        func.register(name, service)

    def removeService(self, name, service):
        '''Remove a service from the cron daemon

        All cron jobs defined on the service will be disabled

        @param name: Name of service to disable
        @type name: string
        @param service: Service instance to disable
        @type service: object
        '''
        if service not in self.services:
            return

        log.msg('[CROND] Removing service %s' % name)
        for job in self.services.pop(service):
            job.disable()


'''Method to check whether something is a L{CronJob}'''
is_cronjob = attrchecker(CRON_ATTRIBUTE)

#Expose the CronJob decorator using lowercase
cronjob = CronJob
