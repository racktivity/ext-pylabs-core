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

'''Unittests for CMDB'''
from __future__ import with_statement

import unittest
import tempfile
import random
import shutil
import threading
import time

from pylabs.cmdb import CMDB, UnknownObjectException
from pylabs import pylabsTestCase

class TestCMDB(pylabsTestCase):
    def test_instanciation(self):
        '''Test whether we can create a CMDB instance'''
        p = CMDB()
        self.assert_(p)

    def test_register_type(self):
        '''Test whether we can register a new object type'''
        p = CMDB()
        p.registerObject('testcase', None)

    def test_unregistered_type(self):
        '''Test whether we can't store a not-registered type'''
        p = CMDB()
        p.saveObject('foo', None)

    def test_get_unregistered_type(self):
        '''Test whether getting an object of which no version was saved yet raises an exception'''
        p = CMDB()
        self.assertRaises(UnknownObjectException, p.getObject, 'foobar')

    def test_storage(self):
        '''Test whether we can store an object in CMDB'''
        p = CMDB()
        p.registerObject('testcase', None)
        p.getObjectWithLock('testcase')
        p.saveObject('testcase', None)

    def test_store_retrieve_none(self):
        '''Test register-store-retrieve cycle using None as object'''
        p = CMDB()
        p.registerObject('testcase-none', None)
        p.getObjectWithLock('testcase-none')
        p.saveObject('testcase-none', None)
        v = p.getObjectWithLock('testcase-none')
        self.assertEqual(v, None)

    def test_store_retrieve_dict(self):
        '''Test register-store-retrieve cycle using dict as object'''
        d = {
            'foo': 'bar',
            'baz': ['bat', '123', ],
        }
        p = CMDB()
        p.registerObject('testcase-dict', None)
        v = p.getObjectWithLock('testcase-dict')
        p.saveObject('testcase-dict', d)
        v = p.getObjectWithLock('testcase-dict')
        self.assertEqual(v, d)

    def test_generations(self):
        '''Test whether register-store-retrieve-store-retrieve works fine'''
        l = random.randint(0, 100)
        l1 = [random.randint(0, 100) for i in xrange(l)]
        l2 = [random.randint(0, 100) for i in xrange(l / 2)]
        p = CMDB()
        p.registerObject('testcase-generations', None)
        p.getObjectWithLock('testcase-generations')
        p.saveObject('testcase-generations', l1)
        v = p.getObjectWithLock('testcase-generations')
        self.assertEqual(v, l1)
        p.saveObject('testcase-generations', l2)
        v = p.getObjectWithLock('testcase-generations')
        self.assertEqual(v, l2)

from pylabs.cmdb import DoubleLockException, ObjectNotOwnedException

from pylabs.cmdb.cmdb import lock, unlock
class TestThreadSafeFileLock(pylabsTestCase):
    def test_basic(self):
        lock('foo')
        unlock('foo')

    def test_multi_thread(self):
        events = list()

        def run1():
            lock('foo')
            events.append(0)
            time.sleep(1)
            events.append(2)
            unlock('foo')

        def run2():
            time.sleep(0.5)
            events.append(1)
            lock('foo')
            events.append(3)
            unlock('foo')
            events.append(4)

        t1 = threading.Thread(target=run1)
        t2 = threading.Thread(target=run2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        self.assertEqual(events, range(5))


class TestCMDBLocking(pylabsTestCase):
    def test_reentrant_lock(self):
        '''Test whether retaking a lock fails'''
        p = CMDB()
        p.saveObject('testcase-reentrant', dict())
        p.getObjectWithLock('testcase-reentrant')
        self.assertRaises(DoubleLockException, p.getObjectWithLock,
                'testcase-reentrant')

    def test_double_save(self):
        '''Test whether two save calls fails'''
        p = CMDB()
        p.saveObject('testcase-double-save', 123)
        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, 'testcase-double-save', 456)

    def test_multiple_release(self):
        '''Test whether multiple release calls succeeds'''
        p = CMDB()
        p.saveObject('test-multiple-release', 123)
        p.getObjectWithLock('test-multiple-release')
        p.releaseObjectLock('test-multiple-release')
        p.releaseObjectLock('test-multiple-release')
        p.releaseObjectLock('test-multiple-release')

    def test_context_manager(self):
        p = CMDB()
        p.saveObject('test-context-manager', 456)

        with p('test-context-manager') as value:
            self.assertEquals(value, 456)
            p.saveObject('test-context-manager', 123)

        self.assert_(not p.pm_isLocked('test-context-manager'))

        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, 'test-context-manager', 456)

    def test_release(self):
        p = CMDB()

        events = list()

        def run1():
            try:
                p.saveObject('test-release', 123)
            except Exception, e:
                events.append((1, e, ))
                return

            try:
                p.getObjectWithLock('test-release')
            except Exception, e:
                events.append((2, e, ))
                return

            try:
                p.releaseObjectLock('test-release')
            except Exception, e:
                events.append((3, e, ))
                return

        def run2():
            if p.pm_isLocked('test-release'):
                events.append((4, Exception('Object locked'), ))

            try:
                p.getObjectWithLock('test-release')
            except Exception, e:
                events.append((5, e, ))
                return

            try:
                p.releaseObjectLock('test-release')
            except Exception, e:
                event.append((6, e, ))
                return

        t1 = threading.Thread(target=run1)
        t2 = threading.Thread(target=run2)

        t1.start()
        t1.join()
        
        t2.start()
        t2.join()

        self.assert_(not events)

    def test_timeout(self):
        p = CMDB()

        p.saveObject('test-timeout', 123)

        def run():
            p.getObjectWithLock('test-timeout', locktimeout=3)
            time.sleep(3)

        t1 = threading.Thread(target=run)

        t1.start()
        time.sleep(1)

        self.assert_(p.pm_isLocked('test-timeout'))

        start = time.time()
        p.getObjectWithLock('test-timeout')
        end = time.time()

        #end - start must be somewhere close to 3
        self.assert_(end - start > 2)
        self.assert_(end - start < 4)

    def test_getobject(self):
        p = CMDB()
        p.saveObject('test-getobject', 456)

        def run():
            p.getObjectWithLock('test-getobject')

        start = time.time()
        value = p.getObject('test-getobject')
        end = time.time()

        self.assertEquals(value, 456)
        #getObject should be non-blocking, so the time to fetch the object
        #should be at least less than 1s
        self.assert_(end - start < 1.0)

    def test_multi_threads(self):
        p = CMDB()
        events = list()

        helper_lock = threading.Lock()
        helper_lock.acquire()

        i = 0
        RUN1_SAVE = i; i += 1
        RUN1_GET_WITH_LOCK = i; i += 1
        RUN1_RELEASE = i; i += 1

        RUN2_GET = i; i += 1
        RUN2_GET_WITH_LOCK = i; i += 1

        RUN3_GET_WITH_LOCK = i; i += 1

        ERROR = i

        def run1():
            p.saveObject('test-multi-threads', 123)
            events.append(RUN1_SAVE)

            helper_lock.release()
            #Give run2 time to getObject
            time.sleep(1)

            o = p.getObjectWithLock('test-multi-threads')
            events.append(RUN1_GET_WITH_LOCK)
            if o != 123:
                events.append(ERROR)
                return

            time.sleep(2)
            p.releaseObjectLock('test-multi-threads')
            events.append(RUN1_RELEASE)

        def run3():
            start = time.time()
            p.getObjectWithLock('test-multi-threads')
            end = time.time()
            events.append(RUN3_GET_WITH_LOCK)

            if end - start > 4.5:
                events.append(ERROR)

        t3 = threading.Thread(target=run3)

        def run2():
            helper_lock.acquire()

            o = p.getObject('test-multi-threads')
            events.append(RUN2_GET)

            if o != 123:
                events.append(ERROR)
                return

            #Give thread 1 time to get the object, with lock
            time.sleep(2)

            start = time.time()
            p.getObjectWithLock('test-multi-threads', locktimeout=4)
            t3.start()
            events.append(RUN2_GET_WITH_LOCK)
            end = time.time()

            if not end - start < 3:
                events.append(ERROR)
                return

            helper_lock.release()


        t1 = threading.Thread(target=run1)
        t2 = threading.Thread(target=run2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        t3.join()

        expected_events = [RUN1_SAVE, RUN2_GET, RUN1_GET_WITH_LOCK,
                RUN1_RELEASE, RUN2_GET_WITH_LOCK, RUN3_GET_WITH_LOCK]

        self.assertEquals(events, expected_events)

    def test_timeout_but_lock_kept(self):
        p = CMDB()
        p.saveObject('test-tblk', None)

        o = p.getObjectWithLock('test-tblk', locktimeout=1)
        
        time.sleep(2)

        p.saveObject('test-test', 123)
    
    def test_timeout_lock_lost(self):
        p = CMDB()
        p.saveObject('test-tll', None)

        def run():
            o = p.getObjectWithLock('test-tll')
        t = threading.Thread(target=run)

        o = p.getObjectWithLock('test-tll', locktimeout=2)

        t.start()
        t.join()
        #Object has been owned by another thread by now

        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, 'test-tll', 123)


class TestTrac180(pylabsTestCase):
    '''Regression test for Trac #180'''

    def test_timeout_relock(self):
        p = CMDB()
        p.saveObject('test-trac180', None)

        from pylabs.cmdb.cmdb import DEFAULT_LOCK_TIMEOUT, isLocked, isSafe

        p.getObjectWithLock('test-trac180')
        self.assert_(isLocked('test-trac180'))
        self.assert_(isSafe('test-trac180'))

        time.sleep(DEFAULT_LOCK_TIMEOUT + 1.0)

        self.assert_(not isLocked('test-trac180'))
        self.assert_(isSafe('test-trac180'))

        p.getObjectWithLock('test-trac180')
        self.assert_(isLocked('test-trac180'))
        self.assert_(isSafe('test-trac180'))