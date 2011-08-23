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

class cmdbTestCase(pylabsTestCase):
    def setUp(self):
        pylabsTestCase.setUp(self)
        self.cmdbobject = "testcase"

    def tearDown(self):
        pylabsTestCase.tearDown(self)
        from pylabs import q
        cmdbdir = q.system.fs.joinPaths(q.dirs.cmdbDir, self.cmdbobject)
        if q.system.fs.exists(cmdbdir):
            q.system.fs.removeDirTree(cmdbdir)
       


class TestCMDB(cmdbTestCase):

    def test_instanciation(self):
        '''Test whether we can create a CMDB instance'''
        p = CMDB()
        self.assert_(p)

    def test_register_type(self):
        '''Test whether we can register a new object type'''
        p = CMDB()
        p.registerObject(self.cmdbobject, None)

    def test_unregistered_type(self):
        '''Test whether we can't store a not-registered type'''
        p = CMDB()
        p.saveObject(self.cmdbobject, None)

    def test_get_unregistered_type(self):
        '''Test whether getting an object of which no version was saved yet raises an exception'''
        p = CMDB()
        self.assertRaises(UnknownObjectException, p.getObject, self.cmdbobject)

    def test_storage(self):
        '''Test whether we can store an object in CMDB'''
        p = CMDB()
        p.registerObject(self.cmdbobject, None)
        p.getObjectWithLock(self.cmdbobject)
        p.saveObject(self.cmdbobject, None)

    def test_store_retrieve_none(self):
        '''Test register-store-retrieve cycle using None as object'''
        p = CMDB()
        p.registerObject(self.cmdbobject, None)
        p.getObjectWithLock(self.cmdbobject)
        p.saveObject(self.cmdbobject, None)
        v = p.getObjectWithLock(self.cmdbobject)
        self.assertEqual(v, None)

    def test_store_retrieve_dict(self):
        '''Test register-store-retrieve cycle using dict as object'''
        d = {
            'foo': 'bar',
            'baz': ['bat', '123', ],
        }
        p = CMDB()
        p.registerObject(self.cmdbobject, None)
        v = p.getObjectWithLock(self.cmdbobject)
        p.saveObject(self.cmdbobject, d)
        v = p.getObjectWithLock(self.cmdbobject)
        self.assertEqual(v, d)

    def test_generations(self):
        '''Test whether register-store-retrieve-store-retrieve works fine'''
        l = random.randint(0, 100)
        l1 = [random.randint(0, 100) for i in xrange(l)]
        l2 = [random.randint(0, 100) for i in xrange(l / 2)]
        p = CMDB()
        p.registerObject(self.cmdbobject, None)
        p.getObjectWithLock(self.cmdbobject)
        p.saveObject(self.cmdbobject, l1)
        v = p.getObjectWithLock(self.cmdbobject)
        self.assertEqual(v, l1)
        p.saveObject(self.cmdbobject, l2)
        v = p.getObjectWithLock(self.cmdbobject)
        self.assertEqual(v, l2)

from pylabs.cmdb import DoubleLockException, ObjectNotOwnedException

from pylabs.cmdb.cmdb import lock, unlock
class TestThreadSafeFileLock(cmdbTestCase):
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


class TestCMDBLocking(cmdbTestCase):
    def test_reentrant_lock(self):
        '''Test whether retaking a lock fails'''
        p = CMDB()
        p.saveObject(self.cmdbobject, dict())
        p.getObjectWithLock(self.cmdbobject)
        self.assertRaises(DoubleLockException, p.getObjectWithLock,
                self.cmdbobject)

    def test_double_save(self):
        '''Test whether two save calls fails'''
        p = CMDB()
        p.saveObject(self.cmdbobject, 123)
        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, self.cmdbobject, 456)

    def test_multiple_release(self):
        '''Test whether multiple release calls succeeds'''
        p = CMDB()
        p.saveObject(self.cmdbobject, 123)
        p.getObjectWithLock(self.cmdbobject)
        p.releaseObjectLock(self.cmdbobject)
        p.releaseObjectLock(self.cmdbobject)
        p.releaseObjectLock(self.cmdbobject)

    def test_context_manager(self):
        p = CMDB()
        p.saveObject(self.cmdbobject, 456)

        with p(self.cmdbobject) as value:
            self.assertEquals(value, 456)
            p.saveObject(self.cmdbobject, 123)

        self.assert_(not p.pm_isLocked(self.cmdbobject))

        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, self.cmdbobject, 456)

    def test_release(self):
        p = CMDB()

        events = list()

        def run1():
            try:
                p.saveObject(self.cmdbobject, 123)
            except Exception, e:
                events.append((1, e, ))
                return

            try:
                p.getObjectWithLock(self.cmdbobject)
            except Exception, e:
                events.append((2, e, ))
                return

            try:
                p.releaseObjectLock(self.cmdbobject)
            except Exception, e:
                events.append((3, e, ))
                return

        def run2():
            if p.pm_isLocked(self.cmdbobject):
                events.append((4, Exception('Object locked'), ))

            try:
                p.getObjectWithLock(self.cmdbobject)
            except Exception, e:
                events.append((5, e, ))
                return

            try:
                p.releaseObjectLock(self.cmdbobject)
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

        p.saveObject(self.cmdbobject, 123)

        def run():
            p.getObjectWithLock(self.cmdbobject, locktimeout=3)
            time.sleep(3)

        t1 = threading.Thread(target=run)

        t1.start()
        time.sleep(1)

        self.assert_(p.pm_isLocked(self.cmdbobject))

        start = time.time()
        p.getObjectWithLock(self.cmdbobject)
        end = time.time()

        #end - start must be somewhere close to 3
        self.assert_(end - start > 2)
        self.assert_(end - start < 4)

    def test_getobject(self):
        p = CMDB()
        p.saveObject(self.cmdbobject, 456)

        def run():
            p.getObjectWithLock(self.cmdbobject)

        start = time.time()
        value = p.getObject(self.cmdbobject)
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
            p.saveObject(self.cmdbobject, 123)
            events.append(RUN1_SAVE)

            helper_lock.release()
            #Give run2 time to getObject
            time.sleep(1)

            o = p.getObjectWithLock(self.cmdbobject)
            events.append(RUN1_GET_WITH_LOCK)
            if o != 123:
                events.append(ERROR)
                return

            time.sleep(2)
            p.releaseObjectLock(self.cmdbobject)
            events.append(RUN1_RELEASE)

        def run3():
            start = time.time()
            p.getObjectWithLock(self.cmdbobject)
            end = time.time()
            events.append(RUN3_GET_WITH_LOCK)

            if end - start > 4.5:
                events.append(ERROR)

        t3 = threading.Thread(target=run3)

        def run2():
            helper_lock.acquire()

            o = p.getObject(self.cmdbobject)
            events.append(RUN2_GET)

            if o != 123:
                events.append(ERROR)
                return

            #Give thread 1 time to get the object, with lock
            time.sleep(2)

            start = time.time()
            p.getObjectWithLock(self.cmdbobject, locktimeout=4)
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
        p.saveObject(self.cmdbobject, None)

        o = p.getObjectWithLock(self.cmdbobject, locktimeout=1)
        
        time.sleep(2)

        p.saveObject('test-test', 123)
    
    def test_timeout_lock_lost(self):
        p = CMDB()
        p.saveObject(self.cmdbobject, None)

        def run():
            o = p.getObjectWithLock(self.cmdbobject)
        t = threading.Thread(target=run)

        o = p.getObjectWithLock(self.cmdbobject, locktimeout=2)

        t.start()
        t.join()
        #Object has been owned by another thread by now

        self.assertRaises(ObjectNotOwnedException,
                p.saveObject, self.cmdbobject, 123)


class TestTrac180(cmdbTestCase):
    '''Regression test for Trac #180'''

    def test_timeout_relock(self):
        p = CMDB()
        p.saveObject(self.cmdbobject, None)

        from pylabs.cmdb.cmdb import DEFAULT_LOCK_TIMEOUT, isLocked, isSafe

        p.getObjectWithLock(self.cmdbobject)
        self.assert_(isLocked(self.cmdbobject))
        self.assert_(isSafe(self.cmdbobject))

        time.sleep(DEFAULT_LOCK_TIMEOUT + 1.0)

        self.assert_(not isLocked(self.cmdbobject))
        self.assert_(isSafe(self.cmdbobject))

        p.getObjectWithLock(self.cmdbobject)
        self.assert_(isLocked(self.cmdbobject))
        self.assert_(isSafe(self.cmdbobject))
