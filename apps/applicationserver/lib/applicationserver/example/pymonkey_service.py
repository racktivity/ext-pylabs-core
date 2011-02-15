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
 
'''A demo Applicationserver service'''

import time
import os.path

from pylabs import q, i
from applicationserver import TaskletRunner

class PMService:
    def __init__(self):
        '''Initialize the service'''
        # Keep track of cronjob runs
        self.cron_counter = 0

        # We need one tasklet runner for synchronous execution
        tasklet_path = q.system.fs.joinPaths(
            os.path.dirname(__file__), 'tasklets')
        self.taskletengine = q.getTaskletEngine(tasklet_path)

        # And one for async execution
        self.asynctaskletrunner = TaskletRunner(self.taskletengine)

    @q.manage.applicationserver.expose
    def getPlatformName(self):
        '''Retrieve the platform type the server is running on

        @return: Platform type
        @rtype: string
        '''
        q.logger.log('Platform request received', 4)
        return str(q.platform)

    @q.manage.applicationserver.cronjob(5)
    def cron(self):
        '''Execute a given task every 5 seconds

        Job execution is stopped when 10 jobs have been executed.
        '''
        q.logger.log('Cron test %d' % self.cron_counter, 3)

        self.cron_counter += 1
        if self.cron_counter > 9:
            return q.manage.applicationserver.CRON_JOB_STOP

    @q.manage.applicationserver.expose_authenticated
    def getApplicationserverServiceNames(self):
        '''Retrieve the names of all services running in the applicationserver

        @return: List of service names
        @rtype: list<string>
        '''
        return i.servers.applicationserver.services.list()

    def checkAuthentication(self, username, password):
        '''Check user authentication credentials

        This method does no real authentication lookup, it just checks whether
        the username is 'me' and the password is 'mypass'.

        @return: Authentication success
        @rtype: bool
        '''
        return username == 'me' and password == 'mypass'

    @q.manage.applicationserver.expose_authenticated
    def executeSomeTasklets(self, params, tags):
        '''Execute some tasklets using given params and tags

        One tag ('demo') is added, and the current timestamp is added in params
        if not given.

        @param params: Parameters to pass to the tasklet
        @type params: dict
        @param tags: List of base tags
        @type tags: list<string>
        '''
        # Make sure we got correct input
        params = dict(params)
        tags = list(tags)

        tags.append('demo')
        if not 'timestamp' in params:
            params['timestamp'] = time.time()

        self.taskletengine.execute(params, tags=tags)

        # A method exposed over XMLRPC should always return some value
        return True

    @q.manage.applicationserver.expose_authenticated
    def executeSomeTaskletsAsync(self, params, tags):
        '''Execute some tasklets using given params and tags, asynchronous

        This method will add an execution request to the tasklet runner and
        return immediately. The selected tasklets will be executed at a later
        point in time.

        @param params: Parameters to pass to the tasklet
        @type params: dict
        @param tags: List of base tags
        @type tags: list<string>
        '''
        self.asynctaskletrunner.queue(params, tags=tags, logname='demo')

        return True