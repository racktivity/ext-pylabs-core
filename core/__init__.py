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

__version__ = (3, 1, 0)

__all__ = ['__version__', 'q', 'i', 'p']

def _setup_stacktrace_hook():
    '''Set up SIGUSR2 signal handler which dumps stack traces of all threads'''
    try:
        import signal
    except ImportError:
        # No signal support on current platform, ignore
        return

    sig = signal.SIGUSR2

    def stderr():
        '''Coroutine which writes input to sys.stderr and a dump file,
        /tmp/pm_<PID>.stack'''
        outputs = list()

        try:
            import sys
            outputs.append((sys.stderr.write, sys.stderr.flush, lambda: None, ))
        except Exception:
            pass

        try:
            import os
            name = '/tmp/pm_%d.stack' % os.getpid()
            fd = open(name, 'w')
            outputs.append((fd.write, fd.flush, fd.close, ))
        except Exception:
            pass

        try:
            while True:
                message = yield

                if message is None:
                    break

                for write, flush, _ in outputs:
                    try:
                        write(message)
                        flush()
                    except Exception:
                        pass
        finally:
            for _, _, close in outputs:
                try:
                    close()
                except Exception:
                    pass

    def getframes(output, frame):
        '''Get a list of all current frames

        This function tries to use sys._current_frames to get a list of the
        frames of every running thread and their thread ID. If this function is
        not available, the given frame will be returned using the string
        '<unknown>' as thread ID.
        '''
        import sys

        # Using sys._current_frames for now
        # We could rewrite this using ctypes as well, see the implementation of
        # _PyThread_CurrentFrames at
        # http://svn.python.org/projects/python/trunk/Python/pystate.c
        current_frames = getattr(sys, '_current_frames', None)
        if not current_frames:
            output('Your system has no support to dump stacks of all threads\n')
            output('Only dumping interrupted frame\n')
            return (('<current>', frame, ), )
        else:
            return tuple(current_frames().items())

    def dump_proc_status(output):
        import os
        import os.path

        procfile = '/proc/%d/status' % os.getpid()

        if not os.path.exists(procfile):
            # File doesn't exist, we're not running on Linux or something alike
            return

        try:
            fd = open(procfile, 'r')
        except Exception:
            # No permissions or something alike?
            # Funny if a process would have no permission on its own status proc
            # file, but anyway, better safe than sorry
            return

        try:
            data = fd.read()
        finally:
            fd.close()

        output('Dumping content of %s\n' % procfile)
        output('\n')
        output(data)
        output('\n')

    def handler_impl(output, num, frame):
        '''Implementation of the signal handler

        This will be called inside a try/except clause so the signal handler
        behaves correctly.
        '''
        import traceback

        output('Got signal %s\n' % str(num))
        output('Dumping current stack frame(s)\n')
        frames = getframes(output, frame)
        output('\n')

        try:
            from threading import _active as active_threads
        except ImportError:
            active_threads = dict()

        for threadid, frame in frames:
            title = None
            if threadid in active_threads:
                try:
                    name = active_threads[threadid].getName()
                except Exception:
                    pass
                else:
                    if name:
                        title = 'Thread %s (%s)' % (name, str(threadid))

            if not title:
                title = 'Thread %s' % str(threadid)

            output('%s\n%s\n' % (title, '=' * len(title)))

            try:
                import thread
                get_ident = thread.get_ident
            except (ImportError, AttributeError):
                get_ident = lambda: object()

            ident = get_ident()
            if threadid == get_ident():
                # We want to strip of ourself from the stacktrace
                orig_frame = frame
                while frame:
                    # If we found the frame of this 'handler' function
                    if frame.f_code == handler.func_code:
                        # Go one frame up and return
                        frame = frame.f_back
                        break

                    # Else go up one more frame
                    frame = frame.f_back

                # If we were not able to find the stackframe we were looking
                # for, just use the original one
                if not frame:
                    frame = orig_frame

            # Format and print backtrace
            stack = ''.join(traceback.format_stack(frame))
            output(stack)
            output('\n')

        try:
            dump_proc_status(output)
        except Exception:
            pass

    def handler(num, frame):
        '''Signal handler which dumps Python stacks of all running threads'''
        output = stderr()
        output.next()
        output = output.send
        try:
            handler_impl(output, num, frame)
        except Exception, e:
            output('An exception occurred while handling signal %d\n' % num)
            output('Exception information:\n')
            output('%s\n\n' % str(e))

        try:
            output(None)
        except StopIteration:
            pass

    # Install signal handler, if none set
    # Check whether a handler is set
    orig_handler = signal.getsignal(sig)
    if orig_handler != signal.SIG_DFL:
        return

    # Set up handler
    old = signal.signal(sig, handler)

# Set up our signal handler
try:
    _setup_stacktrace_hook()
except Exception:
    pass
# Remove the no longer needed function
del _setup_stacktrace_hook


from pylabs.Pylabs import Pylabs
from pylabs.interactive.Interactive import Interactive

q = Pylabs()
i = Interactive()

#########
from pylabs.extensions.PMExtensions import PMExtensions
class PylabsNS():

    def _initExtensions(self):
        self._pmExtensions = PMExtensions(self, 'p.')
        self._pmExtensions.init()
        self._pmExtensions.findExtensions()
        
p = PylabsNS()

from pylabs.testing import pylabsTestCase
