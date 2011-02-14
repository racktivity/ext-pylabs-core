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

'''XMLRPC service client generators

The ManagementClassXMLRPCClient class implemented in this module allows you to
auto-generate client classes (including tab-completion support in Q-shell) for
services exposed through XMLRPC as explained in the module documentation of
L{pymonkey.baseclasses.xmlrpc.server}.

Here's a sample, using the server shown in the module documentation of
L{pymonkey.baseclasses.xmlrpc.server}. We assume C{ServiceOne} and
C{ServiceTwo} are the classes used in the server, implemented in a C{service}
module.

>>> from pymonkey.baseclasses.xmlrpc.client import ManagementClassXMLRPCClient
>>>
>>> from service import ServiceOne, ServiceTwo
>>>
>>> class ServiceOneClient(ManagementClassXMLRPCClient):
...     MANAGER_CLASS = ServiceOne
...
>>> class ServiceTwoClient(ManagementClassXMLRPCClient):
...     MANAGER_CLASS = ServiceTwo
...
>>> c1 = ServiceOneClient('localhost', 8000, endpoint='one')
>>> c1.sum(1, 2)
3
>>> c2 = ServiceTwoClient('localhost', 8000, username='user', password='pass', endpoint='two')
>>> c2.get_secret()
'secret'
'''
import inspect
import new
import itertools
import xmlrpclib
import opcode

from pymonkey.baseclasses.xmlrpc.server import XMLRPC_REQUEST_ARG

def generate_client_method(original_function):
    '''Generate a callable which can work a proxy for a method on a given type

    This method generates a callable which can be used as a proxy for a method
    on a remote type, whilst retaining the original method definition.

    Warning: this is some really tricky code, make sure you really know what
    you're doing when changing this!
    '''
    args = inspect.getargspec(original_function)
    arguments, defaults = args[0], args[3]
    if arguments[0] == 'self':
        arguments = arguments[1:]

    try:
        arguments.remove(XMLRPC_REQUEST_ARG)
    except ValueError:
        pass

    code_string = list()

    #Code we need:
    #In [2]: def func(self, a, b):
    #   ...:     return self._call('func', a, b)
    #   ...:
    #
    #In [3]: dis.dis(func.func_code)
    #  2           0 LOAD_FAST                0 (self)
    #              3 LOAD_ATTR                1 (_call)
    #              6 LOAD_CONST               1 ('func')
    #              9 LOAD_FAST                1 (a)
    #             12 LOAD_FAST                2 (b)
    #             15 CALL_FUNCTION            3
    #             18 RETURN_VALU
    #
    #In [4]: print [ord(c) for c in func.func_code.co_code]
    #[124, 0, 0, 105, 1, 0, 100, 1, 0, 124, 1, 0, 124, 2, 0, 131, 3, 0, 83]
    #
    #In [5]: print func.func_code.co_varnames
    #('self', 'a', 'b')
    #
    #In [6]: print func.func_code.co_consts
    #(None, 'func')

    LOAD_FAST = chr(opcode.opmap['LOAD_FAST'])
    LOAD_ATTR = chr(opcode.opmap['LOAD_ATTR'])
    LOAD_CONST = chr(opcode.opmap['LOAD_CONST'])
    CALL_FUNCTION = chr(opcode.opmap['CALL_FUNCTION'])
    RETURN_VALUE = chr(opcode.opmap['RETURN_VALUE'])

    #LOAD_FAST('self')
    code_string.append(LOAD_FAST) #LOAD_FAST
    code_string.append(chr(0)) #co_varnames[0], self
    code_string.append(chr(0)) #No second argument

    #LOAD_ATTR('_call')
    code_string.append(LOAD_ATTR) #LOAD_ATTR
    code_string.append(chr(1)) #co_names[1], _call
    code_string.append(chr(0))

    #LOAD_CONST(original_function_name)
    code_string.append(LOAD_CONST) #LOAD_CONST
    code_string.append(chr(1)) #co_consts[1], original_function_name
    code_string.append(chr(0))

    for i in xrange(len(arguments)):
        #LOAD_FAST(varname)
        code_string.append(LOAD_FAST) #LOAD_FAST
        code_string.append(chr(i + 1)) #co_varnames[idx of argument + 1 (self)]
        code_string.append(chr(0))

    #CALL_FUNCTION(len(arguments) + 1)
    code_string.append(CALL_FUNCTION) #CALL_FUNCTION
    code_string.append(chr(len(arguments) + 1)) #Number of frames up
    code_string.append(chr(0))

    #RETURN_VALUE
    code_string.append(RETURN_VALUE)

    new_code = new.code(len(arguments) + 1, #argcount
                        len(arguments) + 1, #nlocals
                        len(arguments) + 2, #stacksize
                        67,                 #flags, this is a magic value
                        ''.join(code_string), #code
                        (None, original_function.func_name, ), #consts
                        tuple(['self', '_call'] + arguments),  #names
                        tuple(['self', ] + arguments), #varnames
                        '<pymonkey xmlrpc.client internal>', #filename
                        original_function.func_name, #name
                        0,                  #firstlineno
                        '',                 #lnotab
                        tuple(),            #freevars,
                        tuple()             #cellvars
                )

    func = new.function(new_code, dict(), original_function.func_name, \
            argdefs=defaults)

    #This is somewhat tricky: we need to parse the original docstring so we
    #can add the proxy information before any epydoc-style declaration, so
    #the parsing inside Q-Shell goes well - STEL-962
    if original_function.__doc__:
        original_doc = original_function.__doc__
        original_lines = original_doc.splitlines()

        #Find offset of first non-epydoc line
        for i in xrange(len(original_lines)):
            if original_lines[i].lstrip().startswith('@'):
                break

        #If i equals 0, the first line the only non-epydoc line. Since the
        #following code splits on i, and lines[:0] returns [], whilst
        #lines[0:] returns [lines[0]], we need to set i to 1, otherwise
        #the first line (which is non-epydoc) would be treated as an epydoc
        #formatted line
        if i == 0 and not original_lines[0].lstrip().startswith('@'):
            i = 1

        non_epydoc_lines, epydoc_lines = original_lines[:i], original_lines[i:]
        non_epydoc = '\n'.join(line.strip() for line in non_epydoc_lines).strip()
        epydoc = '\n'.join(line.strip() for line in epydoc_lines).strip()

        #Add some whitespacing
        if non_epydoc:
            non_epydoc = '%s\n\n' % non_epydoc
        if epydoc:
            epydoc = '\n\n%s' % epydoc

        doc = '%sThis is a proxy to the %s method on the XMLRPC server.%s' % \
                (non_epydoc, original_function.func_name, epydoc)

    else:
        doc = 'Proxy to the %s method on the XMLRPC server''' % \
                original_function.func_name

    func.__doc__ = doc.strip()

    return func


class ManagementClassXMLRPCClientMeta(type):
    '''Metaclass for ManagementClassXMLRPCClient classes

    This adds proxy methods to all exposed methods on the wrapped on the
    client type.
    '''
    def __new__(cls, name, bases, attrs):
        clean_attrs = dict((key, value) for key, value in attrs.iteritems() \
                if key is not 'MANAGER_CLASS')
        t = type.__new__(cls, name, bases, clean_attrs)
        try:
            ManagementClassXMLRPCClient
        except NameError:
            #This is ManagementClassXMLRPCClient
            return t

        if not 'MANAGER_CLASS' in attrs:
            raise RuntimeError('ManagementClassXMLRPCClient subclasses should have a MANAGER_CLASS field')

        manager = attrs['MANAGER_CLASS']
        attrs = dir(manager)

        for attr in attrs:
            a = getattr(manager, attr)
            if hasattr(a, 'XMLRPC_EXPOSE'):
                func = generate_client_method(a)
                setattr(t, attr, func)

        setattr(t, '_MANAGER_CLASS', manager)

        if not t.__doc__:
            doc = 'Proxy class for a %s.%s instance served through XMLRPC' % \
                    (manager.__module__, manager.__name__)
            t.__doc__ = doc

        return t


class ManagementClassXMLRPCClient(object):
    '''Autogenerated client class for a remote management class

    See the module documentation of L{pymonkey.baseclasses.xmlrpc.client} for
    a more extensive example.

    Make sure your subclass has a MANAGER_CLASS attribute.
    '''
    __metaclass__ = ManagementClassXMLRPCClientMeta

    def __init__(self, host, port, username=None, password=None, endpoint=None):
        '''Initialize a new client

        @param host: Hostname or IP address of XMLRPC server
        @type host: string
        @param port: Port number of XMLRPC server
        @type port: number
        @param username: Username to use for authentication
        @type username: string
        @param password: Password to use for authentication
        @type password: string
        @param endpoint: Endpoint/namespace of service at server
        @type endpoint: string
        '''
        uri = self._build_uri(host, port, username, password)
        self._host, self._port, self._username = host, port, username
        self._client = xmlrpclib.Server(uri)
        self._endpoint = endpoint


    @staticmethod
    def _build_uri(host, port, username=None, password=None):
        '''Build a service URI based on host, port, username and password'''
        auth = ''
        if username:
            if password:
                auth = '%s:%s@' % (username, password)
            else:
                auth = '%s@' % username

        uri = 'http://%s%s:%d' % (auth, host, port)

        return uri

    def _call(self, fname, *args):
        '''Call a remote method

        This method is only used by proxy methods generated by
        L{generate_client_method}.
        '''
        if self._endpoint:
            base = getattr(self._client, self._endpoint)
        else:
            base = self._client

        proxy_func = getattr(base, fname)

        try:
            return proxy_func(*args)
        except xmlrpclib.ProtocolError, e:
            from twisted.web import http
            if e.errcode == http.UNAUTHORIZED:
                msg = 'Authorization failed while performing method call. Did you forget to provide credentials or used the wrong ones?'
                raise RuntimeError(msg)
            else:
                raise
        except xmlrpclib.Fault, e:
            fault = e.faultString or e.message

            from pymonkey.baseclasses.xmlrpc.server import \
                    FAILURE_PICKLE_DELIMITER

            if FAILURE_PICKLE_DELIMITER in fault:
                message, exception = fault.split(FAILURE_PICKLE_DELIMITER, 1)
                try:
                    import cPickle as pickle
                except ImportError:
                    try:
                        import pickle
                    except ImportError:
                        raise e

                exception = pickle.loads(exception)

                value = getattr(exception, 'value', None)
                if value:
                    #This is very tricky but it allows us to do cool things
                    #like this:
                    #
                    #In [4]: c = C('localhost', 8000, endpoint='one')
                    #
                    #In [5]: c.do_error()
                    #
                    #*** Error: Server-side exception: Hello there (type
                    #                               ServerSideRuntimeError)
                    #
                    #In [6]: try:
                    #   ...:     c.do_error()
                    #   ...: except RuntimeError:
                    #   ...:     print 'RuntimeError detected'
                    #   ...:
                    #RuntimeError detected

                    exceptionclass = new.classobj('ServerSide%s' % \
                            value.__class__.__name__, (value.__class__, ), \
                            value.__dict__)
                    msg = getattr(value, 'message', None) or \
                            getattr(value, 'msg', None) or str(value)
                    if msg:
                        msg = 'Server-side exception: %s' % msg
                        try:
                            localvalue = exceptionclass(msg)
                        except:
                            localvalue = exceptionclass()
                        localvalue.msg = msg
                    else:
                        localvalue = exceptionclass()
                    raise localvalue

                raise exception

            raise

    def __str__(self):
        return '<proxy to a %s.%s instance on endpoint \'%s\' at %s>' % \
                (self._MANAGER_CLASS.__module__, self._MANAGER_CLASS.__name__,
                        self._endpoint,
                        ManagementClassXMLRPCClient._build_uri(self._host,
                            self._port, self._username))

    def __repr__(self):
        return str(self)