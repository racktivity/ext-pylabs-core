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

import unittest
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import nose

from pylabs.action import ActionController, StartStopOutputCountException

class TestActions(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        self.action = ActionController(_output=self.output, _width=40)

    def tearDown(self):
        self.output.close()

    def _check(self, expected_result):
        self.assertEqual(expected_result, self.output.getvalue())

    def test_start(self):
        expected_result = ' * Testing action start output'
        self.action.start('Testing action start output')
        self._check(expected_result)

    def test_simple_start_stop(self):
        expected_result = ' * Testing action DONE output  DONE\n'
        self.action.start('Testing action DONE output')
        self.action.stop()
        self._check(expected_result)

    def test_simple_start_stop_failure(self):
        expected_result = ' * Testing action FAILED output FAILED\n'
        self.action.start('Testing action FAILED output')
        self.action.stop(True)
        self._check(expected_result)

    def test_simple_nested_actions(self):
        expected_result = '''
 * Outer                       RUNNING
 *  Inner                      DONE
 * Outer                       FINISHED
'''.lstrip('\n')
        self.action.start('Outer')
        self.action.start('Inner')
        self.action.stop()
        self.action.stop()
        self._check(expected_result)

    def test_failing_nested_actions(self):
        expected_result = '''
 * Outer                       RUNNING
 *  Inner                      FAILED
 *  Inner                      DONE
 * Outer                       FAILED
'''.lstrip('\n')
        self.action.start('Outer')
        self.action.start('Inner')
        self.action.stop(True)
        self.action.start('Inner')
        self.action.stop()
        self.action.stop(True)

        self._check(expected_result)

    def test_complex_nested_actions(self):
        expected_result = '''
 * Outer1                      RUNNING
 *  Inner1                     RUNNING
 *   Inner2                    RUNNING
 *    Inner3                   FAILED
 *   Inner2                    DONE
 *  Inner1                     FAILED
 *  Inner4                     DONE
 *  Inner5                     RUNNING
 *   Inner6                    DONE
 *  Inner5                     DONE
 * Outer1                      FINISHED
 * Outer2                      DONE
'''.lstrip('\n')
        self.action.start('Outer1')
        self.action.start('Inner1')
        self.action.start('Inner2')
        self.action.start('Inner3')
        self.action.stop(True)
        self.action.stop()
        self.action.stop(True)
        self.action.start('Inner4')
        self.action.stop()
        self.action.start('Inner5')
        self.action.start('Inner6')
        self.action.stop()
        self.action.stop()
        self.action.stop()
        self.action.start('Outer2')
        self.action.stop()

        self._check(expected_result)

    def test_long_descriptions(self):
        expected_result = '''
 * This is a rather long
 *  message which doesn't fit
 *  on one line                DONE
'''.lstrip('\n')
        self.action.start('This is a rather long message which doesn\'t fit '
                          'on one line')
        self.action.stop()

        self._check(expected_result)

    def test_nested_long_descriptions(self):
        expected_result = '''
 * This is a rather long
 *  message                    RUNNING
 *  This is another rather
 *   long message              RUNNING
 *   This is a very deep but
 *    still very long message  FAILED
 *  This is another rather
 *   long message              DONE
 *  This is a short message    DONE
 * This is a rather long
 *  message                    FINISHED
'''.lstrip('\n')

        self.action.start('This is a rather long message')
        self.action.start('This is another rather long message')
        self.action.start('This is a very deep but still very long message')
        self.action.stop(True)
        self.action.stop()
        self.action.start('This is a short message')
        self.action.stop()
        self.action.stop()

        self._check(expected_result)

    def test_clean(self):
        expected_result = '''
 * Action1                     DONE
 * Action2                     RUNNING
 *  Action3                    RUNNING
 *   Action4                   DONE
 * Action5                     DONE
'''.lstrip('\n')

        self.action.start('Action1')
        self.action.stop()
        self.action.start('Action2')
        self.action.start('Action3')
        self.action.start('Action4')
        self.action.stop()

        self.action.clean()

        self.action.start('Action5')
        self.action.stop()

        self._check(expected_result)

    def test_hasrunningactions(self):
        self.assert_(not self.action.hasRunningActions())
        self.action.start('Test')
        self.assert_(self.action.hasRunningActions())
        self.action.start('Test2')
        self.assert_(self.action.hasRunningActions())
        self.action.stop()
        self.assert_(self.action.hasRunningActions())
        self.action.stop(True)
        self.assert_(not self.action.hasRunningActions())

    def test_start_stop_output(self):
        expected_result = '''
 * Outer                       RUNNING
 *  Inner                      RUNNING
Hello world
Beautiful world
 *  Inner                      DONE
 * Outer                       FINISHED
'''.lstrip('\n')

        self.action.start('Outer')
        self.action.start('Inner')
        self.action.startOutput()
        self.output.write('Hello world\nBeautiful world\n')
        self.action.stopOutput()
        self.action.stop()
        self.action.stop()

        self._check(expected_result)

    def test_start_stop_refcounting_mismatch(self):
        raise nose.SkipTest(
            'StartStopOutputCountException is no longer raised')
        self.action.start('Outer')

        self.action.start('Inner')
        self.action.startOutput()
        self.action.stopOutput()
        self.action.stop()

        self.assertRaises(StartStopOutputCountException,
                          self.action.stopOutput)

    def test_action_start_stop_refcounting_mismatch(self):
        raise nose.SkipTest(
            'StartStopOutputCountException is no longer raised')
        self.action.start('Test')

        self.action.startOutput() #1
        self.action.stopOutput()  #1

        self.action.startOutput() #2
        self.action.startOutput() #3
        self.action.stopOutput()  #3

        #2 was not stopped
        self.assertRaises(StartStopOutputCountException, self.action.stop)

    def test_primary_action_start_stop_refcounting_mismatch(self):
        raise nose.SkipTest(
            'StartStopOutputCountException is no longer raised')
        self.action.start('Test')
        self.action.startOutput()

        self.assertRaises(StartStopOutputCountException, self.action.stop)


from pylabs.testing import pylabsTestCase

class TestTrac170(pylabsTestCase):
    def setUp(self):
        pylabsTestCase.setUp(self)

        import sys
        from pylabs import q

        self._original_stdout = sys.stdout
        sys.stdout = self.output = StringIO()

        self._original_action = q.action
        q.action = ActionController(_width=40)

    def tearDown(self):
        import sys
        from pylabs import q

        q.action = self._original_action
        sys.stdout = self._original_stdout

        pylabsTestCase.tearDown(self)

    def _check(self, expected_result):
        self.assertEqual(expected_result, self.output.getvalue())

    def test_start_stop_refcounting_success(self):
        from pylabs import q

        expected_result = '''
 * Outer                       RUNNING
 *  Inner                      RUNNING
Hello world
 *  Inner                      DONE
Bye world
 * Outer                       FINISHED
'''.lstrip('\n')

        q.action.start('Outer')
        q.action.startOutput()

        q.action.start('Inner')
        q.action.startOutput()
        q.console.echo('Hello world')
        q.action.stopOutput()
        q.action.stop()

        q.console.echo('Bye world')
        q.action.stopOutput()
        q.action.stop()

        self._check(expected_result)