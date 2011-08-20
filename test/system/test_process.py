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

import os
import os.path
import sys
import time
import unittest

from pylabs.testing import pylabsTestCase
from pylabs.system.process import run, runScript, runDaemon
from pylabs.system.process import calculateEnvironment, UNSET

#We want the real 'echo' executable somehow, not the shell built-in
#On Solaris shell-echo doesn't like -n and -e, on Ubuntu Linux /bin/sh
#doesn't like -e,...
ECHO = None
for echo in ('/usr/gnu/bin/echo', '/usr/local/bin/echo', '/bin/echo', ):
    if os.path.exists(echo):
        ECHO = echo
        break
if not ECHO:
    #Fallback to shell echo as a last resort
    ECHO = 'echo'

class TestProcessRun(unittest.TestCase):
    def test_simple(self):
        if sys.platform.startswith('win'):
            cmd = 'echo.'
        else:
            cmd = '%s -n' % ECHO
        code, out, err = run(cmd)

        if  sys.platform.startswith('win'):
            #'echo' on win32 outputs at least a newline
            out = out.rstrip()

        self.assertEquals(code, 0)
        self.assertEquals(out, '')
        self.assertEquals(err, '')

    def test_exitcode(self):
        code, out, err = run('exit 123', stopOnError=False)
        self.assertEquals(code, 123)
        self.assertEquals(out, '')
        self.assertEquals(err, '')

    def test_stdout(self):
        if sys.platform.startswith('win'):
            cmd = 'echo Hello world'
        else:
            cmd = '%s -n "Hello world"' % ECHO
        code, out, err = run(cmd)
        self.assertEquals(code, 0)

        if sys.platform.startswith('win'):
            out = out.rstrip()

        self.assertEquals(out, 'Hello world')
        self.assertEquals(err, '')

    def test_stdout_multiline(self):
        if sys.platform.startswith('win'):
            cmd = 'echo Hello world&& echo Beautiful world'
        else:
            cmd = r'%s -e "Hello world\nBeautiful world"' % ECHO

        code, out, err = run(cmd)

        if sys.platform.startswith('win'):
            out = out.replace('\r\n', '\n')

        self.assertEquals(code, 0)
        self.assertEquals(out, 'Hello world\nBeautiful world\n')
        self.assertEquals(err, '')

    def test_stderr(self):
        if sys.platform.startswith('win'):
            cmd = 'echo Hello world >&2'
        else:
            cmd = '%s -n "Hello world" > /dev/stderr' % ECHO
        code, out, err = run(cmd)

        if sys.platform.startswith('win'):
            err = err.rstrip()

        self.assertEquals(code, 0)
        self.assertEquals(out, '')
        self.assertEquals(err, 'Hello world')

    def test_stdout_stderr(self):
        if sys.platform.startswith('win'):
            cmd = 'echo out && echo err >&2'
        else:
            cmd = '%(echo)s -n "out";' \
                  '%(echo)s -n "err" > /dev/stderr' % \
                  {'echo': ECHO}

        code, out, err = run(cmd)

        if sys.platform.startswith('win'):
            out = out.rstrip()
            err = err.rstrip()

        self.assertEquals(code, 0)
        self.assertEquals(out, 'out')
        self.assertEquals(err, 'err')

    def test_show_capture(self):
        self.assertRaises(ValueError, run, 'foobar', showOutput=True,
                captureOutput=True)

    def test_long_running(self):
        if sys.platform.startswith('win'):
            run('ping -w 2000 -n 1 1.0.0.0 > NUL', stopOnError=False)
        else:
            run('sleep 2')

    def test_max_seconds(self):
        if sys.platform.startswith('win'):
            cmd = 'ping -w 5000 -n 1 1.0.0.0 > NUL'
        else:
            cmd = 'sleep 5000'
        code, out, err = run(cmd, maxSeconds=2, stopOnError=False)
        self.assertEquals(code, -2)

    def test_max_seconds_output(self):
        if sys.platform.startswith('win'):
            cmd = 'echo Hello world && ping -w 4000 -n 1 1.0.0.0 > NUL'
        else:
            cmd = '%s -n "Hello world"; sleep 5000' % ECHO
        code, out, err = run(cmd, maxSeconds=2,
                stopOnError=False)

        if sys.platform.startswith('win'):
            out = out.rstrip()

        self.assertEquals(code, -2)
        self.assertEquals(out, 'Hello world')

    def _run_exit_test(self, *args, **kwargs):
        l = list()

        def exit(code):
            l.append(code)

        oldexit = sys.exit
        sys.exit = exit

        code, out, err = run(*args, **kwargs)

        sys.exit = oldexit

        return l[0]


    def test_stop_max_seconds(self):
        if sys.platform.startswith('win'):
            cmd = 'ping -w 5000 -n 1 1.0.0.0 > NUL'
        else:
            cmd = 'sleep 5000'
        code = self._run_exit_test(cmd, maxSeconds=2)
        self.assertEquals(code, 45)

    def test_stop_exitcode(self):
        if sys.platform.startswith('win'):
            cmd = 'echo "Hello world" && exit 1'
        else:
            cmd = '%s "Hello world"; exit 1' % ECHO
        code = self._run_exit_test(cmd)
        self.assertEquals(code, 44)

    def test_run_python_execute_command(self):
        for run_ in xrange(20):
            cmd = '%s -uc "from pylabs.InitBase import q; q.system.process.execute(\'echo %d\', useShell=True)"' \
                % (sys.executable, run_)
            run(cmd)

#This test seems to run fine on Linux32, Solaris and Win32, although most
#likely this is just good luck (since it can fail indeed). Failure is
#reproducible on Linux64.
#Threading and forking don't go well together, at least in Python, since there
#is no support for lock-handling when calling fork (using pthread_atfork etc-)
#See http://mail.python.org/pipermail/python-bugs-list/2004-May/023132.html,
#http://mail.python.org/pipermail/python-dev/2000-August/008558.html or just
#http://www.google.be/search?q=python+pthread_atfork for more info
#    def test_thread(self):
#        import threading
#
#        class WorkerThread(threading.Thread):
#            def __init__(self):
#                threading.Thread.__init__(self)
#                self.running = True
#
#            def run(self):
#                import time
#                while self.running:
#                    run('%s -uc "print \'Hello world\'"' % sys.executable)
#                    time.sleep(0.2)
#
#        t = WorkerThread()
#        t.start()
#
#        import time
#        for i in xrange(10):
#            cmd = 'echo %d' % i
#            run(cmd)
#            time.sleep(0.1)
#
#        t.running = False
#        t.join()


class ProcessRunScriptMixin:
    def _run_script(self, script, *args, **kwargs):
        import tempfile
        #Create a temporary file
        fd, name = tempfile.mkstemp()
        #Make sure we can actually use the fd we got
        fd = os.fdopen(fd, 'w')
        #Dump script content in file
        fd.write(script)
        #Close fd, we don't need it anymore
        fd.close()
        #Run script
        ret = runScript(name, *args, **kwargs)
        #Remove temporary script file
        os.unlink(name)
        return ret


class TestProcessRunScript(unittest.TestCase, ProcessRunScriptMixin):
    def test_basic(self):
        script = r'''
print 'stdout'
import sys
sys.stderr.write('stderr\n')
'''
        code, out, err = self._run_script(script)
        self.assertEquals(code, 0)
        self.assertEquals(out.strip(), 'stdout')
        self.assertEquals(err.strip(), 'stderr')

    def test_unbuffered(self):
        script = r'''
print 'abcdef'
import time
time.sleep(10)
'''
        code, out, err = self._run_script(script, stopOnError=False,
                maxSeconds=2)
        self.assertEquals(code, -2)
        self.assertEquals(out.strip(), 'abcdef')
        self.assertEquals(err, '')

    def test_exitcode(self):
        script = r'''
import sys
sys.exit(123)
'''
        code, _, _ = self._run_script(script, stopOnError=False)
        self.assertEquals(code, 123)


if not sys.platform.startswith('win'):
    class TestProcessRunDaemon(unittest.TestCase):
        # TODO Add tests for the setuid/setgid feature
        def _run_daemon(self, script, extra_args=None):
            import tempfile
            fd, name = tempfile.mkstemp()
            fd = os.fdopen(fd, 'w')

            fd.write(script.lstrip())
            fd.close()

            fd, stdout = tempfile.mkstemp()
            os.close(fd)
            fd, stderr = tempfile.mkstemp()
            os.close(fd)

            cmd = '%s %s' % (sys.executable, name)
            if extra_args:
                cmd = '%s %s' % (cmd, extra_args)

            pid = runDaemon(cmd, stdout=stdout, stderr=stderr)

            running = True
            while running:
                try:
                    os.kill(pid, 0)
                    time.sleep(0.5)
                except OSError:
                    running = False

            fd = open(stdout, 'r')
            so = fd.read()
            fd.close()
            os.unlink(stdout)

            fd = open(stderr, 'r')
            se = fd.read()
            fd.close()
            os.unlink(stderr)

            return so, se

        def test_simple(self):
            script = r'''
import sys
import time

print 'This goes to stdout'
sys.stderr.write('This goes to stderr\n')

time.sleep(2)
'''

            so, se = self._run_daemon(script)

            self.assertEquals(so.strip(), 'This goes to stdout')
            self.assertEquals(se.strip(), 'This goes to stderr')

        def test_args(self):
            script = r'''
import sys
import time

print 'arg1="%s"' % sys.argv[1]
sys.stderr.write('arg2="%s"' % sys.argv[2])

time.sleep(1)
'''

            so, se = self._run_daemon(script, 'arg1 "argument 2"')

            self.assertEquals(so.strip(), 'arg1="arg1"')
            self.assertEquals(se.strip(), 'arg2="argument 2"')


class TestPymonkeyLogging(pylabsTestCase, ProcessRunScriptMixin):
    def test_simple_log(self):
        script = r'''
from pylabs.InitBase import q
q.application.appname = 'test_process'
q.application.start()
q.logger.log('Hello tested world', 5)
q.console.echo('Hello tested world')
q.application.stop()
'''
        code, out, err = self._run_script(script, stopOnError=False)
        self.assertEquals(code, 0)

        #Filter out those readline bytes
        bad_bytes = '\x1b[?1034h'
        if out.startswith(bad_bytes):
            out = out[len(bad_bytes):]

        self.assertEquals(out.rstrip(), 'Hello tested world')

    def test_stress(self):
        for run in xrange(100):
            script = '''
import sys
import time
from pylabs.InitBase import q

run = int(%(run)d)
q.logger.log('Stress test run %%d' %% run)
time.sleep(0.01)
q.logger.log('End run')
''' % {'run': run}
            from pylabs import q
            q.logger.log('Start stress run %d' % run)
            self._run_script(script)
            q.logger.log('Stop stress run %d' % run)


class TestPymonkeyExecuteRun(pylabsTestCase, ProcessRunScriptMixin):
    def test_log_run_execute(self):
        if sys.platform.startswith('win'):
            script = r'''
from pylabs.InitBase import q
q.logger.log('Start execute in run test', 5)
q.system.process.execute('echo 123', useShell=True)
q.system.process.execute('echo 456 && ping -w 1000 -n 1 1.0.0.0 > NUL', \
        useShell=True, dieOnNonZeroExitCode=False)
q.system.process.execute('echo 789 && ping -w 2000 -n 1 1.0.0.0 > NUL', \
        useShell=True, dieOnNonZeroExitCode=False)
q.logger.log('Test script done', 5)
import time
time.sleep(1)
print 'End of script'
'''
        else:
            script = r'''
from pylabs.InitBase import q
q.logger.log('Start execute in run test', 5)
q.system.process.execute('echo 123', useShell=True)
q.system.process.execute('echo 456 && sleep 1')
q.system.process.execute('echo 789 && sleep 2')
q.logger.log('Test script done', 5)
import time
time.sleep(1)
print 'End of script'
'''
        code, out, err = self._run_script(script)
        self.assertEquals(code, 0)


if not sys.platform.startswith('win'):
    import signal
    import subprocess
    from pylabs.system.process import SafePopen

    class TestSubprocessEINTR(unittest.TestCase):
        '''Test whether our SafePopen doesn't fail on EINTR'''
        #These are testcases as provided by
        #http://patches.ubuntu.com/p/python2.5/extracted/
        #   subprocess-eintr-safety.dpatch
        def test_eintr(self):
            # retries on EINTR for an argv

            # send ourselves a signal that causes EINTR
            prev_handler = signal.signal(signal.SIGALRM, lambda x,y: 1)
            signal.alarm(1)
            time.sleep(0.5)

            rc = SafePopen(['sleep', '1'])
            self.assertEqual(rc.wait(), 0)

            signal.signal(signal.SIGALRM, prev_handler)

        def test_eintr_out(self):
            # retries on EINTR for a shell call and pipelining

            # send ourselves a signal that causes EINTR
            prev_handler = signal.signal(signal.SIGALRM, lambda x,y: 1)
            signal.alarm(1)
            time.sleep(0.5)

            rc = SafePopen("sleep 1; echo hello",
                shell=True, stdout=subprocess.PIPE)
            out = rc.communicate()[0]
            self.assertEqual(rc.returncode, 0)
            self.assertEqual(out, "hello\n")

            signal.signal(signal.SIGALRM, prev_handler)


class TestOldExecute(unittest.TestCase):
    def test_pylabs_log(self):
        script = r'''
from pylabs.InitBase import q
q.application.appname = 'test_old_execute'
q.application.start()
q.logger.log('Hello old tested world', 5)
q.console.echo('Hello old execute')
q.application.stop()
'''
        import tempfile
        fd, name = tempfile.mkstemp()
        fd = os.fdopen(fd, 'w')
        fd.write(script)
        fd.close()
        cmd = '%s %s' % (sys.executable, name)
        try:
            from pylabs import q
            code, output = q.system.process.execute(cmd,
                    dieOnNonZeroExitCode=False, outputToStdout=False)
        finally:
            os.unlink(name)

        if output.startswith('\x1b[?1034h'):
            output = output[len('\x1b[?1034h'):]

        self.assertEquals(code, 0)
        self.assertEquals(output.rstrip(), 'Hello old execute')


class TestUidGid(unittest.TestCase):
    # Is  there any 'better' user/group?
    USER = 'nobody'
    GROUP = 'nogroup'

    def setUp(self):
        # Check whether this is a POSIX platform
        try:
            import posix
        except ImportError:
            import nose
            raise nose.SkipTest(
                'Setuid/setgid only supported on POSIX systems')

        # Check whether we're running as root
        if os.getuid() != 0:
            import nose
            raise nose.SkipTest(
                'Setuid/setgid only supported when running as root')

        # Check whether 'whoami' is available
        path = os.environ.get('PATH', '')
        parts = path.split(os.pathsep)
        id_ = None
        for part in parts:
            test = os.path.join(part, 'id')
            if os.path.exists(test):
                id_ = test
                break

        if not id_:
            import nose
            raise nose.SkipTest('Unable to find \'id\' executable')

    def _check_user(self):
        import pwd
        try:
            return pwd.getpwnam(self.USER).pw_uid
        except KeyError:
            import nose
            raise nose.SkipTest('User %s not found on the system' % self.USER)

    def _check_group(self):
        import grp
        try:
            return grp.getgrnam(self.GROUP).gr_gid
        except KeyError:
            import nose
            raise nose.SkipTest('Group %s not found on the system' % \
                                self.GROUP)

    def _execute_test(self, user=None, group=None):
        code, out, _ = run('id', stopOnError=False, user=user, group=group)

        self.assertEquals(code, 0)

        def get_name(s):
            return s.split('(')[1].rstrip(')')

        if user:
            name = get_name(out.split()[0])
            self.assertEquals(name, self.USER)

        if group:
            name = get_name(out.split()[1])
            self.assertEquals(name, self.GROUP)

    def test_simple_uid(self):
        uid = self._check_user()
        self._execute_test(user=uid)

    def test_simple_username(self):
        self._check_user()
        self._execute_test(user=self.USER)

    def test_simple_gid(self):
        gid = self._check_group()
        self._execute_test(group=gid)

    def test_simple_groupname(self):
        self._check_group()
        self._execute_test(group=self.GROUP)

    def test_user_and_group(self):
        self._check_user()
        self._check_group()

        self._execute_test(user=self.USER, group=self.GROUP)

    def test_daemon(self):
        uid = self._check_user()
        gid = self._check_group()

        import tempfile
        fd, name = tempfile.mkstemp()
        os.close(fd)

        os.chown(name, uid, gid)

        pid = runDaemon('id', stdout=name, user=self.USER, group=self.GROUP)
        running = True
        while running:
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except OSError, e:
                import errno
                if e.errno == errno.ESRCH:
                    running = False

        fd = open(name, 'r')
        data = fd.read()
        fd.close()
        os.unlink(name)

        user, group = data.split()[:2]

        self.assertEquals(user.split('(')[1].rstrip(')'), self.USER)
        self.assertEquals(group.split('(')[1].rstrip(')'), self.GROUP)


class TestTrac187(unittest.TestCase):
    def setUp(self):
        if sys.platform.startswith('win'):
            import nose
            raise nose.SkipTest('Test not supported on Windows')

        import tempfile
        fd, self.stdout = tempfile.mkstemp()
        os.close(fd)

    def test_environment_passing(self):
        value = 'value_of_the_environment_variable'
        env = {
            'TESTXYZ': value,
        }

        cmd = '%s $TESTXYZ' % ECHO

        pid = runDaemon(cmd, stdout=self.stdout, env=env)

        running = True
        while running:
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except OSError:
                running = False

        fd = open(self.stdout, 'r')
        data = fd.read()
        fd.close()

        data = data.strip()

        self.assertEquals(data, value)

    def tearDown(self):
        try:
            os.unlink(self.stdout)
        except OSError, e:
            import errno
            if e.errno != errno.ENOENT:
                raise


class TestEnvironmentCalculation(unittest.TestCase):
    def test_merge(self):
        myenv = {
            'TEST1': 'value1',
            'TEST2': 'value2',
        }

        res = calculateEnvironment(myenv)

        self.assertEquals(res['TEST1'], 'value1')
        self.assertEquals(res['TEST2'], 'value2')

        self.assert_(
            set(os.environ.iteritems()).issubset(set(res.iteritems())))

    def test_identical(self):
        self.assertEquals(calculateEnvironment(dict()), os.environ)

    def test_unset(self):
        myenv = {
            'TEST1': 'value1',
            'PATH': UNSET,
        }

        res = calculateEnvironment(myenv)

        self.assertEquals(res['TEST1'], 'value1')
        self.assert_('PATH' not in res)

        env = os.environ.copy()
        env.pop('PATH')
        self.assert_(set(env.iteritems()).issubset(set(res.iteritems())))

    def test_replace(self):
        env = {
            'TEST': 'value1',
        }

        myenv = {
            'TEST': 'value2',
        }

        res = calculateEnvironment(myenv, env)

        self.assertEquals(res['TEST'], 'value2')

    def test_combined(self):
        env = {
            'PATH': '/bin:/usr/bin',
            'USER': 'root',
            'PWD': '/root',
        }

        myenv = {
            'USER': UNSET,
            'PWD': '/tmp',
            'ID': '123',
        }

        res = calculateEnvironment(myenv, env)

        self.assertEquals(res, {
            'PATH': '/bin:/usr/bin',
            'PWD': '/tmp',
            'ID': '123',
        })


class TestTrac189(unittest.TestCase):
    def setUp(self):
        import subprocess
        if subprocess.mswindows:
            import nose
            raise nose.SkipTest('Test not available on Windows')

        import tempfile
        fd, self.stdout = tempfile.mkstemp()
        os.close(fd)
        fd, self.stderr = tempfile.mkstemp()
        os.close(fd)

    def tearDown(self):
        os.unlink(self.stdout)
        os.unlink(self.stderr)

    def test_run(self):
        cmd = 'yes | head -n2'
        output = run(cmd)
        self.assertEquals(output, (0, 'y\ny\n', ''))

    def test_runDaemon(self):
        cmd = 'bash -c "yes | head -n10"'

        pid = runDaemon(cmd, stdout=self.stdout, stderr=self.stderr)

        running = True
        while running:
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except OSError:
                running = False

        fd = open(self.stdout, 'r')
        stdout = fd.read()
        fd.close()
        fd = open(self.stderr, 'r')
        stderr = fd.read()
        fd.close()

        self.assertEquals(stdout, 'y\n' * 10)
        self.assertEquals(stderr, '')