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

'''Unit tests for pylabs.system.fs'''

import unittest
import time
import threading
import tempfile
import shutil
import os
import itertools

from pylabs.system.fs import SystemFS
from pylabs import q, pylabsTestCase
from pylabs.enumerators import PlatformType

LOCKNAME = 'TestLocking'

class TestLocking(pylabsTestCase):
    '''Test interprocess file-based locking'''

    def tearDown(self):
        try:
            q.system.fs.unlock_(LOCKNAME)
        except:
            pass
        pylabsTestCase.tearDown(self)

    class LockAcquirer(threading.Thread):
        GOTLOCK = 1
        WAITLOCK = 2
        RELEASEDLOCK = 3
        LOCKFAIL = 4

        def __init__(self, name, eventqueue, fs, timeout=None, sleeptime=5, threadEvent = None):
            threading.Thread.__init__(self)
            # If no threadEvent is given, create a new instance and set it so wait() won't hang
            if not threadEvent:
                threadEvent = threading.Event()
                threadEvent.set()
            self._event = threadEvent
            self._name = name
            self._eventqueue = eventqueue
            self._fs = fs
            self._timeout = timeout
            self._sleeptime = sleeptime

        def run(self):
            print self._name, 'acquiring lock'
            if self._timeout:
                gl = self._fs.lock_(LOCKNAME, locktimeout=self._timeout)
            else:
                gl = self._fs.lock_(LOCKNAME)
            if not gl:
                print 'Unable to get lock in time'
                self._eventqueue.append({'name': self._name, 'event': self.LOCKFAIL, })
                return
            self._event.wait() # If another thread locked this event, wait for it
            print self._name, 'got lock'
            self._eventqueue.append({'name': self._name, 'event': self.GOTLOCK, })
            print self._name, 'sleeping', self._sleeptime, 'seconds'
            time.sleep(self._sleeptime)
            self._event.clear() # Lock the event to this thread
            try:
                print self._name, 'unlocking'
                self._fs.unlock_(LOCKNAME)
                print self._name, 'unlocked'
                self._eventqueue.append({'name': self._name, 'event': self.RELEASEDLOCK, })
            finally:
                self._event.set() # Release the event


    def test_standard_lock(self):
        '''Test locking using default parameters'''
        fs = SystemFS()

        events = list()
        threadEvent = threading.Event()
        threadEvent.set()
        la = TestLocking.LockAcquirer('a1', events, fs, threadEvent=threadEvent)
        lf = TestLocking.LockAcquirer('a2', events, fs, threadEvent=threadEvent)
        la.start()
        time.sleep(1)
        lf.start()

        la.join()
        lf.join()

        self.assertEqual(events, [
            {'name': 'a1', 'event': TestLocking.LockAcquirer.GOTLOCK},
            {'name': 'a1', 'event': TestLocking.LockAcquirer.RELEASEDLOCK},
            {'name': 'a2', 'event': TestLocking.LockAcquirer.GOTLOCK},
            {'name': 'a2', 'event': TestLocking.LockAcquirer.RELEASEDLOCK}
        ])

    def test_lock_timeout(self):
        '''Test whether lock times out correctly'''
        fs = SystemFS()

        events = list()

        la = TestLocking.LockAcquirer('a1', events, fs, sleeptime=10)
        lf = TestLocking.LockAcquirer('a2', events, fs, timeout=2)
        la.start()
        time.sleep(1)
        lf.start()

        la.join()
        lf.join()

        self.assertEqual(events, [
            {'name': 'a1', 'event': TestLocking.LockAcquirer.GOTLOCK},
            {'name': 'a2', 'event': TestLocking.LockAcquirer.LOCKFAIL},
            {'name': 'a1', 'event': TestLocking.LockAcquirer.RELEASEDLOCK},
        ])

class TestDirs(pylabsTestCase):
    '''Test the directory functionalities'''

    def test_isDir(self):
        fs=SystemFS()
        self.assertEqual(fs.isDir(q.dirs.tmpDir), os.path.isdir(q.dirs.tmpDir), "The q.system.fs.isDir() failed")

    def test_exists(self):
        fs=SystemFS()
        self.assertEqual(fs.exists(q.dirs.tmpDir), os.path.exists(q.dirs.tmpDir), "q.system.fs.exists() failed")

    def test_dir(self):
        fs=SystemFS()
        fs.createDir(os.path.join(q.dirs.tmpDir, "unit_test"))
        self.assert_(os.path.exists(os.path.join(q.dirs.tmpDir, "unit_test")), "q.system.fs.createDir: dir was not created")
        fs.removeDir(os.path.join(q.dirs.tmpDir, "unit_test"))
        self.failIf(os.path.exists(os.path.join(q.dirs.tmpDir, "unit_test")), "q.system.removeDir: dir was not removed")

class TestFilenames(unittest.TestCase):
    def test_generic_invalid_empty(self):
        '''Test whether an empty filename is invalid'''
        fs = SystemFS()
        filename = ''
        self.assertFalse(fs.validateFilename(filename))


    def test_unix_valid(self):
        '''Test whether a complex but valid UNIX filename is valid'''
        fs = SystemFS()
        filename = '.test_kf456\';.,^$&@(@'
        self.assert_(fs.validateFilename(filename, platform=PlatformType.UNIX))

    def test_unix_invalid_null(self):
        '''Test whether a UNIX filename containing null is invalid'''
        fs = SystemFS()
        filename = 'foo.bar\0.baz'
        self.assertFalse(fs.validateFilename(filename, platform=PlatformType.UNIX))

    def test_unix_invalid_slash(self):
        '''Test whether a UNIX filename containing / is invalid'''
        fs = SystemFS()
        filename = 'foo/bar.txt'
        self.assertFalse(fs.validateFilename(filename, platform=PlatformType.UNIX))

    def test_unix_invalid_length(self):
        '''Test whether a UNIX filename of 256 characters is invalid'''
        fs = SystemFS()
        filename = 'a' * 256
        self.assertFalse(fs.validateFilename(filename, platform=PlatformType.UNIX))


    def test_windows_valid(self):
        '''Test whether a complex but valid Windows filename is valid'''
        fs = SystemFS()
        filename = 'This is a valid Wind0ws filename with some characters like ^{[]'
        self.assert_(fs.validateFilename(filename, platform=PlatformType.WIN))

    def test_windows_invalid_length(self):
        '''Test whether a Windows filename of 256 characters is invalid'''
        fs = SystemFS()
        filename = 'a' * 256
        self.assertFalse(fs.validateFilename(filename, platform=PlatformType.WIN))

    def test_windows_invalid_characters(self):
        '''Test whether a Windows filename containing invalid characters is invalid'''
        fs = SystemFS()

        for i in xrange(30):
            self.assertFalse(fs.validateFilename('abc%s.txt' % chr(i), platform=PlatformType.WIN))

        for c in ('<', '>', ':', '"', '/', '\\', '|', '?', '*', ):
            self.assertFalse(fs.validateFilename('abc%s.txt' % c, platform=PlatformType.WIN))

    def test_windows_invalid_ending_space(self):
        '''Test whether a Windows filename ending with a space is invalid'''
        fs = SystemFS()
        self.assertFalse(fs.validateFilename('test.txt ', platform=PlatformType.WIN))

    def test_windows_invalid_ending_dot(self):
        '''Test whether a Windows filename ending with a dot is invalid'''
        fs = SystemFS()
        self.assertFalse(fs.validateFilename('test.txt.', platform=PlatformType.WIN))

    def test_windows_invalid_basenames(self):
        '''Test whether Windows filenames using a DOS device as basename are invalid'''
        fs = SystemFS()
        invalids = itertools.chain(('CON', 'PRN', 'AUX', 'CLOCK$', 'NUL', ),
                                   ('COM%d' % i for i in xrange(1, 9)),
                                   ('LPT%d' % i for i in xrange(1, 9))
                                  )
        for invalid in invalids:
            self.assertFalse(fs.validateFilename('%s.txt' % invalid, platform=PlatformType.WIN))

    def test_unsupported_platform(self):
        '''Test whether checking against an unsupported platform raises an error'''
        fs = SystemFS()
        self.assertRaises(NotImplementedError, fs.validateFilename, 'test', platform=PlatformType.OTHER)