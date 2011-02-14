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

'''Module providing several decorators used inside PyMonkey.

A decorator is a function 'wrapped around' another function or method: it
allows us to perform actions before or after the decorated method is
executed, including not executing the decorated method at all (eg when we want
deprecated methods decorated with the 'deprecated' decorator not to be
callable at all).

Python provides some syntactic sugar to decorate methods, here are some samples
with the 'deprecated' decorator implemented in this module:

>>> @deprecated
... def deprecated_function(a, b):
...     return a + b

>>> class SomeClass:
...     @deprecated
...     def deprecated_method(self, a, b):
...         return a * b

Decorators 101
==============
Here's a very basic introduction how decorators work:

>>> # We'll use functools.wraps, which is a utility decorator for decorators
>>> # It fixes __name__ and __doc__ for decorated functions
>>> import functools
>>>
>>> def simple_decorator(func):
...     print 'Generating decorated version of', func.__name__
...
...     @functools.wraps(func)
...     def wrapped(*args, **kwargs):
...         print func.__name__, 'called with arguments', args, kwargs
...         result = func(*args, **kwargs)
...         print 'Result is', result
...         # Return the result
...         return result
...
...     print 'Decorated version created'
...     return wrapped
...
>>> # Basic test function
>>> def test1(a, b):
...     print 'Adding', a, 'to', b
...     return a + b
...
>>> print test1(1, 2)
Adding 1 to 2
3
>>>
>>> # Let's use our decorator as if it's a normal function generator
>>> # Do note it actually *is* a function generator
>>> test2 = simple_decorator(test1)
Generating decorated version of test1
Decorated version created
>>> # Now we got a new method, test2, which is a wrapped test1
>>> print test2(1, 2)
test1 called with arguments (1, 2) {}
Adding 1 to 2
Result is 3
3
>>>
>>> # Now use the decorator syntax (new since Python 2.4)
>>> @simple_decorator
... def test3(a, b):
...     print 'Adding', a, 'to', b
...     return a + b
...
Generating decorated version of test3
Decorated version created
>>> # And test...
>>> print test3(1, 2)
test3 called with arguments (1, 2) {}
Adding 1 to 2
Result is 3
3
'''

import os
import warnings
import functools
import inspect

import pymonkey

class Version:
    '''Helper class to perform version calculations'''
    def __init__(self, major=None, minor=None, micro=None, str_=None):
        if not str_:
            self.major = major or 0
            self.minor = minor or 0
            self.micro = micro or 0

        else:
            parts = str_.split('.')
            parts = map(int, parts)
            if len(parts) > 3:
                raise ValueError('Unable to parse version %s' % str_)
            if len(parts) == 3:
                self.major, self.minor, self.micro = parts
            elif len(parts) == 2:
                self.major, self.minor = parts
                self.micro = 0
            elif len(parts) == 1:
                self.major = parts
                self.minor, self.micro = 0, 0
            else:
                raise ValueError('Unable to parse version %s' % str_)

    def __cmp__(self, other):
        return cmp(self.as_tuple(), other.as_tuple())

    def __str__(self):
        return '.'.join(map(str, self.as_tuple()))

    def as_tuple(self):
        return self.major, self.minor, self.micro

    def is_previous(self, other):
        return self.major == other.major and self.minor == other.minor + 1

PYMONKEY_VERSION = Version(str_='.'.join(map(str, pymonkey.__version__)))


class deprecated(object):
    '''Mark a function or method as deprecated

    When running in debug mode, this method will display a warning on stdout
    using the standard Python mechanism when the deprecated method is called.
    When the environment variable PM_DISABLE_DEPRECATED is set, a
    DeprecationWarning will be raised when a deprecated method is called,
    most likely resulting in a crash (eg to be used when running testcases).
    '''
    def __init__(self, name, alternative=None, version=None):
        '''Provide display information for deprecated methods

        @param name: Human-readable name of the function,
                     e.g. q.system.fs.Walk
        @type name: string
        @param alternative: Optional alternative function,
                            e.g. q.system.fs.walk
        @type alternative: string
        @param version: Version in which the function will be removed,
                        e.g. 3.3
        @type version: string
        '''
        self.name = name
        self.alternative = alternative

        self.removed = False
        self.show_warning = False

        if version:
            self.version = Version(str_=version)
            if self.version <= PYMONKEY_VERSION:
                self.removed = True
            if self.version.is_previous(PYMONKEY_VERSION):
                self.show_warning = True
        else:
            self.version = None

    def calculate_message(self, func):
        name = self.name or \
                '%s.%s' % (inspect.getmodule(func).__name__, func.__name__)

        msg = 'Call to %s function %s' % \
                ('deprecated' if not self.removed else 'removed', name)
        if self.version:
            msg = '%s (removed in PyMonkey version %s)' % (msg, self.version)

        if self.alternative:
            msg = '%s, use %s instead' % (msg, self.alternative)

        return msg

    def __call__(self, func):
        if self.removed:
            name = self.name or \
                '%s.%s' % (inspect.getmodule(func).__name__, func.__name__)
            if hasattr(pymonkey, 'q'):
                pymonkey.q.logger.log('[DEPRECATION] Found deprecated method '
                                  '%s.%s, this can be removed' % name, 5)

        @functools.wraps(func)
        def newfunc(*args, **kwargs):
            message = self.calculate_message(func)

            pymonkey.q.logger.log('[DEPRECATION] %s' % message, 4)

            # TODO Display this in non-debug mode as well one day
            if pymonkey.q.vars.getVar('DEBUG') or self.show_warning:
                warnings.warn(message, category=DeprecationWarning)

            if 'PM_DISABLE_DEPRECATED' in os.environ or self.removed:
                raise DeprecationWarning(message)

            return func(*args, **kwargs)

        extra_doc = 'Note: this function is deprecated'
        if self.version:
            extra_doc = '%s and will be removed in PyMonkey version %s' % \
                    (extra_doc, self.version)
        if self.alternative:
            extra_doc = '%s, use %s' % (extra_doc, self.alternative)

        if not newfunc.__doc__:
            newfunc.__doc__ = extra_doc
        else:
            def get_doc_lines():
                lines = newfunc.__doc__.strip().splitlines()

                if not [l for l in lines if l.strip()]:
                    # Docstring is empty
                    yield extra_doc
                    return

                first_line = None
                if lines[0].startswith(' ') and lines[0].strip():
                    first_line = lines[0]
                else:
                    # Find the first line starting from the second which
                    # contains some content
                    first_lines = [l for l in lines[1:] if l.strip()]
                    if first_lines:
                        first_line = first_lines[0]

                if not first_line:
                    # If no 'first line' is found, don't indent
                    indent = 0
                else:
                    # Indent the number of spaces at front of the first
                    # significant line in the docstring
                    indent = len(first_line) - len(first_line.lstrip())

                extra_emitted = False

                for idx, line in enumerate(lines):
                    if not extra_emitted and line.lstrip().startswith('@'):
                        if idx > 0 and lines[idx - 1].strip():
                            # Looks like there's no newline between the last
                            # line in the documentation and the first one
                            # starting with an '@'. Insert one.
                            yield ''

                        # Emit the extra line and one newline
                        yield '%s%s.' % (' ' * indent, extra_doc)
                        yield ''

                        extra_emitted = True

                    yield line

                if not extra_emitted:
                    # We found no '@' line, so extra_doc is not yet emitted. Do
                    # so now.
                    yield ''
                    yield '%s%s.' % (' ' * indent, extra_doc)

            newfunc.__doc__ = '\n'.join(get_doc_lines())

        return newfunc