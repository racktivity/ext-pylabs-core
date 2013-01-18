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

'''Applicationserver service to host wizards following SPEC20/WizardServer

The basics
==========
The service needs to host several wizards at a time. One wizard is written as a
simple script, eg.

>>> def main(q, i, params, tags):
...     name = q.gui.dialog.askString('What\'s your name?')
...     age = q.gui.dialog.askInteger('What\'s your age?')
...     if age < 18:
...         q.gui.dialog.messages('Sorry %s, you\'re not allowed here' % name)
...         return
...
...     registerVisitor(name)
...     q.gui.dialog.message('Welcome to the party, %s' % name)

These scripts are PyMonkey2 C{tasklets}, see the documentation of the tasklet
extension for more information.

There's one issue here since we're working in a web-based context: the HTTP
protocol is stateless and client-server based, and we can't just run the wizard
script in our HTTP server container, since this should be non-blocking. A
potential solution would be to run the wizard script in some thread, but even
then some rather complex inter-thread communication should be required to pass
information between the HTTP server (which handles client request/responses) and
a running wizard thread. The implementation of all q.gui.dialog.* methods would
become complex as well since they should block until a response is available and
handle it to the assignment (return it).

Luckily, Python comes to the rescue thanks to its support for coroutines
(introduced in Python 2.5). This way we are able to run a function (actually
it's a generator) inside our mainloop, but with a separate execution context,
while being able to interact with this generator. Here's some code to
demonstrate the idea (using fake wizard control messages):

>>> def askString(s):
...     return 'askstringaction:%s' % s
...
>>> def askInteger(s):
...     return 'askintegeraction:%s' % s
...
>>> def message(s):
...     return 'messageaction:%s' % s
...
>>> def main():
...     name = yield askString('What\'s your name?')
...     age = yield askInteger('What\'s your age?')
...     if age < 18:
...         yield message('Sorry, you\'re not allowed yet')
...         return
...     yield message('Welcome, %s' % name)
...
>>> runner = main()
>>> action = runner.next()
>>> print action
askstringaction:What's your name?
>>> action = runner.send('Nicolas')
>>> print action
askintegeraction:What's your age?
>>> action = runner.send(23)
>>> print action
messageaction:Welcome, Nicolas
>>> runner.send(None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

This shows how generators/coroutines can help us out to create wizards using
normal methods without the need of threading, complex blocking action functions,
etc. For an overview of coroutines in Python, see PEP342.

The problem
===========
There's one issue with the approach described above: it requires the wizard
author to add _yield_ statements to his code, which renders the wizard useless
in a non-webbased environment, ie. when the wizard is not running inside this
service. This can't be easily solved, unless we create a _runWizard_ method
which takes a wizard function and handles all coroutine interaction.

This approach would require rather strange constructed q.gui.dialog.* functions
though. Here's something which could work (for reference), but it's highly
suboptimal, since the main problem (wizards scripts being less intuitive to
write because of the required _yield_ statements) is not fixed.

>>> def askString(s):
...     def f():
...         return raw_input('%s ' % s).rstrip('\n')
...     return f
...
>>> def message(s):
...     def f():
...         print s
...     return f
...
>>> def main():
...     name = yield askString('What\'s your name?')
...     yield message('Hello, %s' % name)
...
>>> runner = main()
>>> action = runner.next()
>>> value = action()
What's your name? Nicolas
>>> action = runner.send(value)
>>> value = action()
Hello, Nicolas
>>> runner.send(value)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration


Getting rid of yield
====================
So, we want to get rid of the _yield_ statements in our wizard source code, but
still want to use coroutines (which require _yield_-based code).

One approach here would be source code rewriting, putting a _yield_ statement
before every occurrence of _q.gui.dialog_ in the original code, and recompile
the code string.

Rewriting source code in an automated manner can be very error-prone though, and
especially in this case, could easily result in the production of invalid Python
code, since a construct like the following is not legal:

>>> def f():
...     if yield askYesNo('Is this correct?'):
  File "<stdin>", line 2
    if yield askYesNo('Is this correct?'):
           ^
SyntaxError: invalid syntax

So, we need a better solution.

Instead of rewriting source code, we can as well rewrite the CPython Virtual
Machine bytecode of the wizard functions.

This might sound easy at first, but there's one difficulty: where do we need to
insert statements, and which?

At first this might seem easy: we want to make sure a value is yielded after
every call to some function of _q.gui.dialog_, so we figure out how yield works
in bytecode:

>>> import dis
>>> def f():
...     name = askString('What\'s your name?')
...
>>> def g():
...     name = yield askString('What\'s your name?')
...
>>> dis.dis(f)
  2           0 LOAD_GLOBAL              0 (askString)
              3 LOAD_CONST               1 ("What's your name?")
              6 CALL_FUNCTION            1
              9 STORE_FAST               0 (name)
             12 LOAD_CONST               0 (None)
             15 RETURN_VALUE
>>> dis.dis(g)
  2           0 LOAD_GLOBAL              0 (askString)
              3 LOAD_CONST               1 ("What's your name?")
              6 CALL_FUNCTION            1
              9 YIELD_VALUE
             10 STORE_FAST               0 (name)
             13 LOAD_CONST               0 (None)
             16 RETURN_VALUE

So, looks like we need to add a _YIELD_VALUE_ opcode after every call to a
_q.gui.dialog_ function.

Let's see how to figure out these:

>>> def f():
...     name = yield q.gui.dialog.askString('What\'s your name?')
...
>>> dis.dis(f)
  2           0 LOAD_GLOBAL              0 (q)
              3 LOAD_ATTR                1 (gui)
              6 LOAD_ATTR                2 (dialog)
              9 LOAD_ATTR                3 (askString)
             12 LOAD_CONST               1 ("What's your name?")
             15 CALL_FUNCTION            1
             18 YIELD_VALUE
             19 STORE_FAST               0 (name)
             22 LOAD_CONST               0 (None)
             25 RETURN_VALUE

Right, figuring out where to add this _YIELD_VALUE_ opcode becomes less
obvious, but still possible if we keep some state in our opcode walker.

This becomes even more difficult though if the wizard developer starts doing
something like this:

>>> def f():
...     test = q.gui.dialog.askYesNo('Is %d + %d %d?' % (1, 2, sum((1, 2, ))))
...
>>> dis.dis(f)
  2           0 LOAD_GLOBAL              0 (q)
              3 LOAD_ATTR                1 (gui)
              6 LOAD_ATTR                2 (dialog)
              9 LOAD_ATTR                3 (askYesNo)
             12 LOAD_CONST               1 ('Is %d + %d %d?')
             15 LOAD_CONST               2 (1)
             18 LOAD_CONST               3 (2)
             21 LOAD_GLOBAL              4 (sum)
             24 LOAD_CONST               4 ((1, 2))
             27 CALL_FUNCTION            1
             30 BUILD_TUPLE              3
             33 BINARY_MODULO
             34 CALL_FUNCTION            1
             37 STORE_FAST               0 (test)
             40 LOAD_CONST               0 (None)
             43 RETURN_VALUE

We'd need to be able to keep track of which object is actually called for each
_CALL_FUNCTION_ opcode, which is not a trivial task at all.

So, looks like we're not able to figure out reliably where to add _YIELD_VALUE_
opcodes to the wizard function code.

We need to take other opcodes, next to _CALL_FUNCTION_, into account as well,
since _CALL_FUNCTION_ is not the only way to call functions: _CALL_FUNCTION_ is
used to call a function using simple arguments which are all pushed on the
stack. To support positional and keyword arguments (using _*args_ or _**kwargs_
in the caller code), one of _CALL_FUNCTION_VAR_, _CALL_FUNCTION_KW_ or
_CALL_FUNCTION_VAR_KW_ is used. From now on, we'll refer to the family of
function call opcodes as _CALL_FUNCTION*_.

It turns out there's a very simple (although suboptimal time-wise) solution for
this problem: instead of figuring out where to add _YIELD_VALUE_ opcodes, we can
just add one after every single _CALL_FUNCTION*_ opcode, and handle this inside
our wizard runner code: we just walk through the rewritten function (well,
generator produced by the function) and send back every value we got:

>>> def return_something(what):
...     return what
...
>>> def f():
...     a = yield return_something(123)
...     print 'a =', a
...     b = yield return_something(456)
...     print 'b =', b
...
>>> runner = f()
>>> value = runner.next()
>>> while True:
...     value = runner.send(value)
...
a = 123
b = 456
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
StopIteration

Here the _yield_ statements are hard-coded, but if you check the opcodes used,
it's easy to see we can generate this as well:

>>> dis.dis(f)
  2           0 LOAD_GLOBAL              0 (return_something)
              3 LOAD_CONST               1 (123)
              6 CALL_FUNCTION            1
              9 YIELD_VALUE
             10 STORE_FAST               0 (a)

  3          13 LOAD_CONST               2 ('a =')
             16 PRINT_ITEM
             17 LOAD_FAST                0 (a)
             20 PRINT_ITEM
             21 PRINT_NEWLINE

  4          22 LOAD_GLOBAL              0 (return_something)
             25 LOAD_CONST               3 (456)
             28 CALL_FUNCTION            1
             31 YIELD_VALUE
             32 STORE_FAST               1 (b)

  5          35 LOAD_CONST               4 ('b =')
             38 PRINT_ITEM
             39 LOAD_FAST                1 (b)
             42 PRINT_ITEM
             43 PRINT_NEWLINE
             44 LOAD_CONST               0 (None)
             47 RETURN_VALUE

Using this method, we can insert a _YIELD_VALUE_ opcode after every single
occurrence of _CALL_FUNCTION*_. We only need some way to figure out whether we
should yield the value to the final caller or not, since now we're using 2
separate generators:

 * One generator is the rewritten wizard function
 * One generator wraps the rewritten one and only yields values we actually want

These values are everything returned by a _q.gui.dialog_ function, since these
are the ones to be handed over to the HTTP server, and HTTP responses should be
sent to the wizard function. Others can just be returned as-is without
interference by the HTTP server.

This is simply solved by wrapping all values returned by any _q.gui.dialog_
functions in a simple wrapper type and perform some type checking in the outer
generator.

There's one more thing we should check: are we allowed to add these
_YIELD_VALUE_ opcodes after every _CALL_FUNCTION*_ opcode?

Function calling and stacks
===========================
Note: this applies to CPython 2.5. Information provided here might change in
newer versions.

CPython is a stack-based virtual machine, where every execution context got its
own stack. We need to make sure, when inserting this extra opcode after
_CALL_FUNCTION*_, no side-effects are introduced, and the semantics of the
_YIELD_VALUE_ opcode are honoured.

Here's how _CALL_FUNCTION_ works:

1. Pop all arguments from the stack (number of arguments is provided as an
   argument to the opcode)
2. Pop the callable to call from the stack
3. Execute the code object of this callable
4. Push the return value of the callable on the stack

Other _CALL_FUNCTION*_ opcodes work in a similar way.

In the end there can be 2 situations:

* We don't care about the function return value

  >>> def f():
  ...     test(1, 2, 3)
  ...
  >>> dis.dis(f)
    2           0 LOAD_GLOBAL              0 (test)
                3 LOAD_CONST               1 (1)
                6 LOAD_CONST               2 (2)
                9 LOAD_CONST               3 (3)
               12 CALL_FUNCTION            3
               15 POP_TOP
               16 LOAD_CONST               0 (None)
               19 RETURN_VALUE

  Notice the _POP_TOP_ opcode at location 15, which removes the return value of
  the _test_ function (whatever this might be) from the stack, since we didn't
  assign it to any variable.

* We want to store the function return value

  >>> def f():
  ...     t = test(1, 2, 3)
  ...
  >>> dis.dis(f)
    2           0 LOAD_GLOBAL              0 (test)
                3 LOAD_CONST               1 (1)
                6 LOAD_CONST               2 (2)
                9 LOAD_CONST               3 (3)
               12 CALL_FUNCTION            3
               15 STORE_FAST               0 (t)
               18 LOAD_CONST               0 (None)
               21 RETURN_VALUE

  Notice the _STORE_FAST_ opcode at location 15, which pops an item from the
  stack (in this case the return value of the _test_ function), and assigns it
  to a certain name (how names are handled inside functions won't be discussed
  here).

Now, how does _YIELD_VALUE_ work (since CPython 2.5)? Quite similar to
_CALL_FUNCTION*_: when a _YIELD_VALUE_ opcode is encountered by the virtual
machine, it pops a value from the stack, and yields this to the generator
caller. The value sent back by the caller (through the _send_ or _next_ methods,
where in case of the _next_ method this value is _None_) is pushed on top of the
stack.

If the yield statement comes at the right-hand-side (RHS) of an assignment, the
returned value is handled exactly like a function return value: the value is
popped from the stack and assigned to a name. If the yield statement is a
non-assignment statement, the value is discared using _POP_TOP_:

>>> def f():
...     a = yield 123
...     yield 456
...
>>> dis.dis(f)
  2           0 LOAD_CONST               1 (123)
              3 YIELD_VALUE
              4 STORE_FAST               0 (a)

  3           7 LOAD_CONST               2 (456)
             10 YIELD_VALUE
             11 POP_TOP
             12 LOAD_CONST               0 (None)
             15 RETURN_VALUE

This means we can safely insert a _YIELD_VALUE_ opcode after every
_CALL_FUNCTION*_ occurrence: the stack will remain intact.

This also means we can, thanks to this binary rewrite, make our system work in
situations like

>>> if askYesNo('Something'):
...     doSomething()

where a normal _yield_ would be invalid syntax (see before). The runtime handles
the changed opcode stream just fine.

Binary rewriting caveats
========================
When rewriting a normal function, this can be done by changing the _co_code_
attribute of the function code object (_func_code_ attribute). This is a simple
bytestring of opcodes and arguments.

When making big changes to a function (like, turning it into a generator
function) lots of other things need to be changed as well:

* The flags of the code object should be altered so the runtime knows it's a
generator function (need to be OR'ed with 0x0020, see CO_GENERATOR in
Include/code.h in your CPython distribution)

  >>> def f():
  ...     a = 123
  ...
  >>> def g():
  ...     a = yield 123
  ...
  >>> f.func_code.co_flags
  67
  >>> g.func_code.co_flags
  99
  >>> f.func_code.co_flags & 0x0020
  0
  >>> g.func_code.co_flags & 0x0020
  32

* The stacksize should be adjusted if necessary
* ...

Getting this straight is a tedious task and can be error-prone. Making mistakes
here can crash a CPython virtual machine.

This is why the _byteplay_ module is used to rewrite the existing function code.
This module will recalculate stack sizes, set code object flags correctly, etc.

For more information on the _byteplay_ module, see
http://code.google.com/p/byteplay/

Final overview
==============
Here's an overview of the total picture:

1. Given a wizard function, a new function object is generated. This generated
   function has the same opcodes as the original one, except for one thing: a
   _YIELD_VALUE_ opcode is added immediately after every _CALL_FUNCTION*_
   opcode.

2. The generator function is called to create a generator. A helper walks
   through the generator and sends back every value it receives, unless it's a
   value wrapped in a well-known type.

3. If such special value is found, its actual value is extracted and send to the
   caller code (ie. the runner code is a generator itself).

4. Any value the caller code sends into the generator is proxied to the
   rewritten wizard function and assigned accordingly.


That's about it. Using above information you should be able to read the code
yourself and change it if ever necessary. Most hard work is done in the
___call___ and __generate_generator_ methods of _GeneratorGenerator_: the first
one provides the run helpers, the latter performs the bytecode rewriting. The
_step_ method of _RunningWizardManager_ shows the rewritten wizard can be used
as a normal generator, handling nothing but the original _q.gui.dialog_ calls.
'''
#pylint: disable=C0302,R0903,W0142,C0103,E1101

#This is *only* supported on CPython 2.5. If this ever needs to run on some
#other version, make sure the bytecode rewriting tricks explained above also
#work on this new target.
import sys
#assert (sys.version_info[:2] == (2, 5)), 'This service only runs in CPython 2.5'
assert hasattr(sys, 'subversion'), 'This service only runs in CPython'
assert (sys.subversion[0] == 'CPython'), 'This service only runs in CPython'

import os.path
import uuid
import inspect
import operator
import threading
import copy

import json

import byteplay

# racktivity specific authorization
try:
    from racktivity import authorization
except ImportError:
    authorization = None

# We require this for the tests to run fine
if __name__ == '__main__':
    from pylabs.InitBase import q, i, p #pylint: disable=F0401
else:
    from pylabs import q, i, p #pylint: disable=F0401

class UnknownSessionException(Exception):
    '''Exception raised when an invalid session ID is used'''
    pass

class EndOfWizard(Exception):
    '''The end of the wizard was reached'''


    def __init__(self, result): #pylint: disable=W0231
        self.result = result

    def __str__(self):
        return '{"action": "endofwizard", "result": %s}' % \
            json.dumps(self.result) if self.result else ""


class DialogMessage(object):
    '''Container for dialog messages from q.gui.dialog.*

    Any wizard step response should be marshalled in this type so the wizard
    runner can know it should yield the value.
    '''
    def __init__(self, value):
        '''Wrap a new wizard message

        @param value: Value to wrap
        @type value: object
        '''
        self.value = value


class GeneratorGenerator(object):
    '''Create a generator out of a normal funtion

    This class will create a generator, based on a given function, by inserting
    a YIELD_VALUE opcode after every CALL_FUNCTION* opcode. This generator is
    executed in the __call__ method of this class, which is a generator itself:
    it will send any value it receives from the internal generator back to the
    generator, except if this value is of type C{special_value_wrapper}. In that
    case, it will yield the value returned by C{special_value_getter} (providing
    it the original value) to the caller, and forward the reply on this yield
    to the internal generator.

    See the module documentation for more information how this works.
    '''
    def __new__(cls, func, special_value_wrapper, special_value_getter):
        '''Allocator for class instances

        @param func: Function to create generator from
        @type func: callable
        @param special_value_wrapper: Wrapper class for 'special' values
        @type special_value_wrapper: type
        @param special_value_getter: Function to retrieve values from a wrapper
        @type special_value_getter: callable
        '''
        key = (func, special_value_wrapper, special_value_getter)

        if not hasattr(cls, '_generator_cache'):
            cls._generator_cache = dict()

        if key in cls._generator_cache:
            return cls._generator_cache[key]

        inst = object.__new__(cls, func, special_value_wrapper,
                special_value_getter)
        cls._generator_cache[key] = inst

        return inst

    def __init__(self, func, special_value_wrapper, special_value_getter):
        '''Initialize a new GeneratorGenerator

        @see: GeneratorGenerator.__new__
        '''
        #Check whether provided func is a generator. If it is, I'm unable to
        #work with it
        #The 0x0020 comes from Include/code.h in the CPython distribution:
        #    #define CO_GENERATOR    0x0020
        if func.func_code.co_flags & 0x0020:
            raise TypeError(
                'Provided func is already a generator, I can\'t deal with this')

        #Keep _initialized because we're using __new__. Don't re-init
        if getattr(self, '_initialized', False):
            return

        assert callable(func), 'Provided function should be a callable'
        assert callable(special_value_getter), \
            'Provided special value getter should be a callable'

        self._func = func
        self._special_value_wrapper = special_value_wrapper
        self._special_value_getter = special_value_getter
        self._generator = None

        self._initialized = True

    def __call__(self, *args, **kwargs):
        '''Call the generator

        This will construct the generator if necessary, call it to get a
        coroutine, and run it.

        See the module documentation for more information how this works.
        '''
        if not self._generator:
            self._generator = self._generate_generator(self._func)

        runner = self._generator(*args, **kwargs)

        try:
            value = runner.next()

            while True:
                if isinstance(value, self._special_value_wrapper):
                    value = self._special_value_getter(value)
                    try:
                        #If you find this line in a backtrace, you most likely
                        #need to look one frame up, since that's where the
                        #exception went, from the caller of this generator to
                        #the actual generator
                        value = yield value
                    except (StopIteration, GeneratorExit):
                        raise
                    except:
                        #Forward any exception thrown into here into the inner
                        #coroutine
                        runner.throw(*sys.exc_info())

                value = runner.send(value)
        except StopIteration:
            return
        except GeneratorExit:
            runner.close()

    @classmethod
    def _generate_generator(cls, func):
        '''Create a generator out of the given func

        This basicly creates a generator function by adding a YIELD_VALUE opcode
        after every CALL_FUNCTION* opcode it finds in the original code. It also
        rewrites the origin filename of the code object to denote it has been
        modified by this method.

        Do note C{func} should be a function, a general callable will most
        likely not be sufficient.

        @param func: Source function
        @type func: function
        '''
        def insert_yields(opcodes):
            for opcode, arg in opcodes:
                yield (opcode, arg)
                if opcode in (byteplay.CALL_FUNCTION,
                              byteplay.CALL_FUNCTION_VAR,
                              byteplay.CALL_FUNCTION_KW,
                              byteplay.CALL_FUNCTION_VAR_KW, ):
                    yield (byteplay.YIELD_VALUE, None)

        code = byteplay.Code.from_code(func.func_code)

        new_code = list(insert_yields(code.code))

        code.code = new_code
        code.filename = '%s%s(modified by %s:%s.%s)' % \
            (code.filename, ' ' if code.filename else '', cls.__module__,
                    cls.__name__, '_generate_generator')

        return type(func)(code.to_code(), func.func_globals, func.func_name,
                func.func_defaults, func.func_closure)


class RunningWizardManager(object):
    '''Manager for all running wizards'''
    def __init__(self):
        #a dict to hold the running wizards.
        self._wizards = dict()
        self._sessionstore = dict()
        #a dict to hold the running wizards locks,
        #they are needed to add thread safety to the service, so calls to
        #start, step, stop are synchronized
        self._locks = dict()

    def register(self, wizard_func, *args, **kwargs):
        '''Register a new wizard

        A session ID will be generated, and the wizard (implemented in the
        callable wizard_func) will be created.

        @param wizard_func: Function implementing the wizard
        @type wizard_func: callable
        @param args: Args sent to the generator constructor
        @type args: tuple
        @param kwargs: Kwargs sent to the generator constructor
        @type kwargs: dict

        @return: Session ID
        @rtype: string
        '''
        if not callable(wizard_func):
            raise TypeError('The wizard_func argument should be callable')

        session = str(uuid.uuid4())
        #This should never happen, but anyway
        while session in self._wizards:
            session = str(uuid.uuid4())

        if not getattr(wizard_func,
                       'APPLICATIONSERVER_WIZARD_NO_YIELD_REWRITE', False):
            wizard_func = GeneratorGenerator(wizard_func, DialogMessage,
                    operator.attrgetter('value'))

        if len(args) == 5:
            params = args[3]
        elif len(args) == 4:
            params = args[2]
        else:
            raise RuntimeError('Unexpected number of arguments')

        params['SESSIONSTATE'] = self._sessionstore[session] = dict()

        wizard = wizard_func(*args, **kwargs)

        self._wizards[session] = { "wizard": wizard, "params": params}

        #creating an RLock is created for the wizard, note that RLock is required since a thread that
        #executing a step() call may try to re acquire the lock while calling stop() causing a deadlock in
        #case of using simple Lock() object.
        self._locks[session] = threading.RLock()

        return session

    def start(self, session):
        '''Start the wizard

        @param session: Session ID
        @type session: string

        @return: First wizard panel
        @rtype: string
        '''
        lock = self._locks[session]
        lock.acquire()

        try:
            wizard = self._get_wizard(session)["wizard"]
            return wizard.next()
        except StopIteration:
            raise EndOfWizard(self.stop(session))
        finally:
            lock.release()


    def stop(self, session):
        '''Stop the wizard

        @param session: Session ID
        @type session: string
        '''
        lock = self._locks[session]
        lock.acquire()

        try:
            try:
                wizard = self._wizards[session]
                result = wizard["params"]["result"] if "result" in wizard["params"] else {}
                wizard["wizard"].close()
            except StopIteration:
                pass
            except RuntimeError, e:
                if e.message == 'generator ignored GeneratorExit':
                    # Log and discard
                    msg = 'A wizard contains a catchall try/except statement around a q.gui.dialog function.' + \
                        'This is considered bad style and might cause memory leaks'
                    if hasattr(q, 'rtlogger'):
                        q.rtlogger.default.warning(msg)
                    else:
                        q.logger.log(msg)
                else:
                    # Try to avoid a memleak
                    # The __del__ method of the generator might still bail out
                    # and send some warning/exception message to stderr. Nothing
                    # we can do about that
                    del self._wizards[session]
                    raise

            del self._wizards[session]
        except KeyError:
            pass
        finally:
            del self._locks[session]
            lock.release()

        return result

    def step(self, session, data):
        '''Execute one step of the wizard

        @param session: Session ID
        @type session: string
        @param data: Data to send to the wizard method
        @type data: object

        @return: Next wizard panel
        @rtype: string
        '''

        lock = self._locks[session]
        lock.acquire()

        try:
            wizard = self._get_wizard(session)["wizard"]
            return wizard.send(data)
        except StopIteration:
            raise EndOfWizard(self.stop(session))
        finally:
            lock.release()

    def _get_wizard(self, session):
        try:
            return self._wizards[session]
        except KeyError:
            raise UnknownSessionException('Session %s is unknown' % session)


class ApplicationserverWizardService(object):
    '''Wizard applicationserver service'''
    def __init__(self, taskletPaths=None):
        self._manager = RunningWizardManager()

        q.gui.dialog.chooseDialogType(q.enumerators.DialogType.WIZARDSERVER)
        q.gui.dialog.MessageType = DialogMessage

        if not taskletPaths:
            # If no specific tasklets path was specified
            # Tasklets go into (folder containing this service file)/tasklets
            taskletPaths = (q.system.fs.joinPaths(
                os.path.dirname(__file__), 'tasklets'), )

        self.taskletengine = q.taskletengine.get(taskletPaths[0])
        for dir_ in taskletPaths[1:]:
            self.taskletengine.addFromPath(dir_)

        # needed for dcpm specific authorization
        basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)
        self._authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
        self._authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))
        if authorization is not None:
            self._localAuthorize = authorization.RacktivityAuthorizationCrossChecker()
        else:
            self._localAuthorize = None

    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        self._authenticate.execute(params, tags=tags)
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        params['localAuthorize'] = self._localAuthorize
        self._authorize.execute(params, tags=tags)
        return params.get('result', False)

    @q.manage.applicationserver.expose_authorized(defaultGroups=["admin"], authorizeParams={"wizard": "wizardName", "extra":"extra", "alarmGuid":""}, authorizeRule="start wizard")
    def start(self, domainName, wizardName, extra=None,
        applicationserver_request=None):
        _p = copy.copy(p)
        _p.api = p.application.getAPI(p.api.appname, context=q.enumerators.AppContext.CLIENT)

        login = applicationserver_request.username
        passwd = applicationserver_request.password

        extra = extra or dict()

        tasklets = self.taskletengine.find(name='*',
            tags=(domainName, wizardName))

        if not tasklets:
            raise RuntimeError(
                'No matching wizard ("%s") found for domain "%s"' % \
                (wizardName, domainName) )

        params = {
            'domain': domainName,
            'extra': extra,
            'login':login,
            'password': passwd,
        }
        params.update( extra )
        tags = (domainName, wizardName)

        def call_tasklet_procedure(proc_, params_, tags_):
            argcount_ = len(inspect.getargspec(proc_)[0])

            # 0 case is 'default match': lambda *_1, lambda **_2: True
            if argcount_ == 5 or argcount_ == 0:
                return proc_(q, i, _p, params_, tags_)
            elif argcount_ == 4:
                return proc_(q, i, params_, tags_)

            raise ValueError('Invalid procedure argument count')

        for tasklet in tasklets:
            if call_tasklet_procedure(tasklet.match, params, tags):
                proc = tasklet.methods['main']
                argcount = len(inspect.getargspec(proc)[0])

                args = ()
                if argcount == 5:
                    args = (q, i, _p, params, tags)
                elif argcount == 4:
                    args = (q, i, params, tags)
                else:
                    raise ValueError('Invalid procedure argument count')

                session = self._manager.register(tasklet.methods['main'], *args)

                try:
                    step = self._manager.start(session)
                except EndOfWizard, e:
                    return session, str(e)

                return session, step

        raise RuntimeError(
            'No matching wizard ("%s") found for domain "%s"' % \
            (wizardName, domainName))

    @q.manage.applicationserver.expose_authenticated
    def callback(self, domainName, wizardName='', methodName='', formData='',
        extra=None, SessionId=None, applicationserver_request=None):

        methodName = 'callback_%s'% methodName
        extra = extra or dict()
        extra['formData'] = formData

        extra['login'] = applicationserver_request.username
        extra['password'] = applicationserver_request.password

        if SessionId:
            extra['SESSIONSTATE'] = self._manager._sessionstore[SessionId] #pylint: disable=W0212
        else:
            extra['SESSIONSTATE'] = None

        callback_method = self._getWizardMethod(domainName, wizardName, methodName)

        updatedForm = callback_method(q, i, extra, (domainName, ))
        action = updatedForm.convertToWizardAction()

        return json.dumps(action)

    @q.manage.applicationserver.expose_authenticated
    def stop(self, sessionId):
        self._manager.stop(sessionId)
        return str(EndOfWizard(""))

    @q.manage.applicationserver.expose_authenticated
    def result(self, sessionId, result):
        try:
            step = self._manager.step(sessionId, result)
        except EndOfWizard, e:
            step = str(e)

        return step

    def _getWizardMethod(self, domainName, wizardName, method):
        wizard_methods = self.taskletengine.find(name='*',
            tags=(domainName,wizardName))

        if not wizard_methods:
            raise RuntimeError('No matching wizard ("%s")found for domain "%s"' % (wizardName, domainName) )
        if len(wizard_methods) > 1:
            raise RuntimeError('Multiple matching wizards found')

        wizard_method = wizard_methods[0].methods[method]
        return wizard_method

# Some testcases testing our function rewriting, static analysis
if __name__ == '__main__':
    #pylint: disable=C0111,C0103,E0602,W0142,W0612,W0212,W0613,R0911,E1101
    import unittest

    # This is the function we will rewrite in the yield insert test
    def _yield_test_original(arg1, arg2, *args, **kwargs):
        a = 123
        b = 456

        c = func1()

        a = 789

        d = func2(a, b, c)

        a = 987

        func3()

        a = 654

        e = func4(*abc)

        a = 321

        f = func5(a, b, c, 'abc', *abc, **{'a': 'b', 'c': 1})

        a = 123

        g = func6(**{'a': 123})

        a = 456

        #h = q.some.function('abc')

        a = 789

    # This is the result we expect after rewriting _yield_test_original
    def _yield_test_result(arg1, arg2, *args, **kwargs):
        a = 123
        b = 456

        c = (yield func1())

        a = 789

        d = (yield func2(a, b, c))

        a = 987

        yield func3()

        a = 654

        e = (yield func4(*abc))

        a = 321

        f = (yield func5(a, b, c, 'abc', *abc, **{'a': 'b', 'c': 1}))

        a = 123

        g = (yield func6(**{'a': 123}))

        a = 456

        #h = (yield q.some.function('abc'))

        a = 789

    class TestFunctionRewriting(unittest.TestCase):
        def _compare_funcs(self, target, func):
            '''Check whether 2 functions are code-wise equivalent'''
            target_code = byteplay.Code.from_code(target.func_code).code
            func_code = byteplay.Code.from_code(func.func_code).code

            self.assertEqual(len(target_code), len(func_code))

            # Make sure code and func attributes are equal
            # Don't compare func_code and func_name, the first one will
            # obviously not be the same, the second one neither but we don't
            # care
            for attr in ('func_closure', 'func_defaults', 'func_dict',
                         'func_doc', 'func_globals', ):
                self.assertEqual(getattr(target, attr), getattr(func, attr),
                                'Function attribute %s is different' % attr)

            # Don't compare co_code, which will obviously be different, nor
            # co_filename since we rewrite it, nor co_firstlineno since it is
            # indeed not the same (we're comparing 2 different functions), nor
            # co_lnotab since it will just like co_firstlineno be different, nor
            # co_name, since it will be different as well
            for attr in ('co_argcount', 'co_cellvars', 'co_consts', 'co_flags',
                         'co_freevars', 'co_names', 'co_nlocals',
                         'co_stacksize', 'co_varnames', ):
                self.assertEqual(getattr(target.func_code, attr),
                                 getattr(func.func_code, attr),
                                 'Code attribute %s is different' % attr)

            known_labels = dict()

            for op1, op2 in zip(target_code, func_code):
                if op1[0] == byteplay.SetLineno:
                    self.assertEqual(op1[0], op2[0])
                    continue

                if isinstance(op1[1], byteplay.Label):
                    self.assert_(isinstance(op2[1], byteplay.Label))

                    if op1[1] in known_labels:
                        self.assert_(op2[1] is known_labels[op1[1]])
                    else:
                        known_labels[op1[1]] = op2[1]

                    continue

                if isinstance(op1[0], byteplay.Label):
                    self.assert_(isinstance(op2[0], byteplay.Label))

                    if op1[0] in known_labels:
                        self.assert_(op2[0] is known_labels[op1[0]])
                    else:
                        known_labels[op1[0]] = op2[0]

                    continue

                self.assertEqual(op1, op2)

        def test_yield_insert(self):
            '''Test yield insertion rewriting'''
            result = GeneratorGenerator._generate_generator(
                                                        _yield_test_original)
            self._compare_funcs(_yield_test_result, result)


    unittest.main()

