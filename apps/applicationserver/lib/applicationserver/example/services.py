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
 
from applicationserver import expose, expose_authenticated, cronjob
from applicationserver import CRON_JOB_STOP

class HelloService:
    def __init__(self, greeting):
        self.greeting = greeting
        self.users = set()

    @expose
    def hello(self, name):
        if name == 'invalid':
            raise ValueError('"invalid" is not a valid name')

        try:
            self.users.add(name)
        except Exception, e:
            pass

        return '%s, %s!' % (self.greeting, name), list(self.users)

    def goodbye(self):
        return 'Bye!'


class SecretService:
    def checkAuthentication(self, username, password):
        return username == 'ali' and password == 'baba'

    @expose_authenticated
    def get_password(self):
        return 'Sesame'


class RequestService:
    @expose
    def request(self, applicationserver_request):
        data = {
                'request_hostname': 'Request hostname',
                'client_ip': 'Client IP',
                'user_authenticated': 'User authenticated',
                'username': 'Username',
                'password': 'Password',
        }
        res = dict()
        for key, value in data.iteritems():
            res[value] = getattr(applicationserver_request, key)

        return res

    @expose_authenticated
    def auth_request(self, applicationserver_request):
        return self.request(applicationserver_request)

    def checkAuthentication(self, username, password):
        return True


class CounterService:
    def __init__(self):
        self.counter = self.counter2 = 0

    @cronjob(1)
    def count(self):
        self.counter += 1
        print 'Counter:', self.counter
        return self.counter

    @cronjob(1)
    def count_to_10(self):
        self.counter2 += 1
        if self.counter2 >= 10:
            print 'Stopping count_to_10'
            return CRON_JOB_STOP
        print 'count_to_10 stops in %d' % (10 - self.counter2)

    @cronjob(1)
    def misbehave(self):
        print 'I\'m a long-running cronjob'
        import time
        time.sleep(5)

    @cronjob(5)
    def error(self):
        print 'I error out'
        raise RuntimeError('Some error')