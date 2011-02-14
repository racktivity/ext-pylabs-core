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
 
import sys
import imp
import random
import functools

from twisted.python import log

def generateModuleName(orig_name):
    """
    Generate a unique module name

    @param orig_name: original module name
    @type orig_name: string
    @return: unique module name of form _applicationserver_ORIG_NAME_RANDOM_NR
    @rtype: string
    """
    MIN = 0
    MAX = 999999

    def gen(nr):
        return "_applicationserver_%s_%d" % (orig_name, nr)

    def taken(modName):
        return modName in sys.modules

    nr = random.randint(MIN, MAX)
    while taken(gen(nr)):
        nr = (nr + 1) % MAX
    return gen(nr)

def getClass(name, classpath):
    """
    Get a reference to a class object based on a combination of the path of
    its module and the classname, separated by a ':'

    Caller should catch exceptions

    @param name: suggestion for the module name
    @type name: string
    @param classpath: "/path/of/module:ClassName"
    @type classpath: string
    @return: Loaded class
    @rtype: type
    """
    log.msg('[UTILS] Loading class %s for service %s' % (classpath, name))

    if ':' not in classpath:
        raise ValueError("Invalid classpath: no ':' found")
    path, klassname = classpath.rsplit(':', 1)
    log.msg('[UTILS] Loading class %s from file %s' % (klassname, path))
    modname = generateModuleName(name)
    module = imp.load_source(modname, path)
    return getattr(module, klassname)

def attrchecker(name):
    '''Function generator to generate an attribute-checker function

    Functions generated by this function will return the value of a specific
    attribute on their parameter, or return C{False} if not set.

    @param name: Name of the attribute to retrieve
    @type name: string

    @return: Attribute checker function
    @rtype: callable
    '''
    def f(func):
        return getattr(func, name, False)

    f.__doc__ = 'Check whether function attribute %s is set' % name
    return f

def service_method_caller(service_name, func, wraps=True):
    def service_func(*args, **kwargs):
        from applicationserver.dispatcher import EXPOSED_SERVICE_NAME_KWARG
        kwargs = kwargs.copy()
        kwargs[EXPOSED_SERVICE_NAME_KWARG] = service_name
        return func(*args, **kwargs)

    if wraps:
        return functools.wraps(func)(service_func)
    else:
        return service_func


AUTH_FUNC_ATTRNAME = 'APPLICATIONSERVER_XMLRPC_AUTH_FUNC'

def auth_func_attrchecker(func, request):
    checker = getattr(func, AUTH_FUNC_ATTRNAME, lambda r: True)
    return checker(request)

class auth_func(object):
    def __init__(self, auth_func):
        self.auth_func = auth_func

    def __call__(self, func):
        setattr(func, AUTH_FUNC_ATTRNAME, self.auth_func)
        return func


class _authorization_local(auth_func):
    def __init__(self):
        def func(request):
            host = request.getHost().host
            client = request.getClientIP()
            if client.startswith('127.'):
                return True
            elif host == client:
                return True
            return False

        auth_func.__init__(self, func)

authorization_local = _authorization_local()