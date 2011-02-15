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

'''Implementation of CMDB, the pylabs Database (object persistance layer)'''

from __future__ import with_statement

__pychecker__ = 'no-reimport'

import time
import os
import os.path
import functools
import thread
import threading
import struct
try:
    import cPickle as pickle
except ImportError:
    import pickle

import pylabs

from pylabs.system.fs import lock_ as _lock, unlock_ as _unlock

#Some helper variables for ThreadLocalLock
_LOCK_DICT = dict() #Lock store
_HELPER_LOCK = threading.Lock() #Helper lock when modifying _LOCK_DICT

class ThreadLocalLock:
    '''Lock similar to threading.Lock, but release can only be called by the
    thread which acquired the lock also
    '''
    def __init__(self):
        self._lock = threading.Lock()

    def acquire(self):
        '''Acquire the lock

        This method is blocking.
        '''
        self._lock.acquire()
        self.thread_id = thread.get_ident()

    def release(self):
        '''Release the lock'''
        if not self.thread_id == thread.get_ident():
            raise RuntimeError(
                'Unable to unlock lock not acquired in current thread')

        self._lock.release()


def lock(name):
    '''Acquire a file-based interprocess lock

    This lock will also be in-process threadsafe. Basicly: if you got this lock,
    you're the only thread on the whole system who owns it.

    @param name: Lock identifier
    @type name: string
    '''
    if not name in _LOCK_DICT:
        _HELPER_LOCK.acquire()
        try:
            if not name in _LOCK_DICT:
                _LOCK_DICT[name] = ThreadLocalLock()
        finally:
            _HELPER_LOCK.release()

    _LOCK_DICT[name].acquire()
    try:
        _lock(name)
    except:
        _LOCK_DICT[name].release()
        raise

def unlock(name):
    '''Unlock a lock acquired through L{lock}
    
    @param name: Lock identifier
    @type name: string
    '''
    if not name in _LOCK_DICT:
        raise RuntimeError('Unknown lock')

    if not _LOCK_DICT[name].thread_id == thread.get_ident():
        raise RuntimeError('Lock not owned by current thread')

    try:
        _unlock(name)
    finally:
        _LOCK_DICT[name].release()


class FileLock(object):
    '''Context manager for L{lock} and L{unlock}'''
    def __init__(self, lock_name):
        self.lock_name = lock_name

    def __enter__(self):
        lock(self.lock_name)

    def __exit__(self, *exc_info):
        unlock(self.lock_name)


DEFAULT_LOCK_TIMEOUT = 10.0
DEFAULT_WAIT_TIMEOUT = 70.0
MAX_LOCK_TIMEOUT = 60.0

class CMDBException(Exception):
    '''Base class for any CMDB-related exception'''

class UnknownObjectException(CMDBException):
    '''Exception thrown when an unregistered object is requested'''

class ObjectNotOwnedException(CMDBException):
    '''Exception thrown when a lock is needed to perform an action on an
    object, but the lock is not owned by the current thread'''

class ObjectLockedException(CMDBException):
    '''Exception thrown when an object is locked'''

class LockWaitTimeoutException(CMDBException):
    '''Exception thrown when a lock acquisition timeout has passed'''

class DoubleLockException(CMDBException):
    '''Exception thrown when a second lock is requested on a locked object'''


class CMDBLock(object):
    '''Process- and thread-safe lock on one CMDB object'''

    #Lockfile struct data format
    #PID TID starttime releasetime
    STRUCT_FORMAT = 'Lldd'

    def __init__(self, base_dir, type_name):
        '''Initialize a new CMDBLock

        @param base_dir: CMDB base folder
        @type base_dir: string
        @param type_name: CMDB object type name
        @type type_name: string
        '''
        self.base_dir = base_dir
        self.type_name = type_name

    @property
    def access_lock_name(self):
        '''Name of FileLock used to lock down CMDB lockfile access'''
        return 'cmdb_%s_access_lock' % self.type_name

    @property
    def lock_path(self):
        '''Path of CMDB lock lockfile path'''
        return pylabs.q.system.fs.joinPaths(
                self.base_dir, self.type_name, 'lock')

    def _safe(self, take_lock):
        '''Check whether the object lock is currently owned by the current
        thread

        @param take_lock: Whether or not to acquire the file-based lock to lock
                          access to the CMDB lock file. Internal usage.
        @type take_lock: bool
        '''
        if take_lock:
            lock(self.access_lock_name)

        try:
            #Lock file exists AND owned by this thread
            if not pylabs.q.system.fs.exists(self.lock_path):
                return False

            pid, tid, _, _ = self._read()

            return pid == os.getpid() and tid == thread.get_ident()

        finally:
            if take_lock:
                unlock(self.access_lock_name)

    def _free(self, take_lock):
        '''Check whether no lock on the object is acquired at all, system-wide

        @param take_lock: Whether or not to acquire the file-based lock to lock
                          access to the CMDB lock file. Internal usage.
        @type take_lock: bool
        '''
        if take_lock:
            lock(self.access_lock_name)

        try:
            #Lock file does not exist OR endtime is exceeded
            if not os.path.exists(self.lock_path):
                return True

            _, _, _, endtime = self._read()
            if endtime < time.time():
                return True

        finally:
            if take_lock:
                unlock(self.access_lock_name)

        return False

    safe = property(fget=functools.partial(_safe, take_lock=True),
            doc='The lock is owned by the current thread')
    free = property(fget=functools.partial(_free, take_lock=True),
            doc='The lock is not owned by any thread on the system')

    def _read(self):
        '''Read out the CMDB lock file

        @return: Lock data, as defined in L{STRUCT_FORMAT}
        @rtype: tuple

        @see: STRUCT_FORMAT
        '''
        #Not using filegetcontents etc since we want control over the open
        #format identifiers
        with open(self.lock_path, 'rb') as fd:
            data = fd.read()
            
        return struct.unpack(self.STRUCT_FORMAT, data)

    def _write(self, timeout):
        '''Write out a CMDB lock file

        @param timeout: Lock timeout in seconds
        @type timeout: number
        '''
        timeout = min(timeout, MAX_LOCK_TIMEOUT)
        start = time.time()

        args = (os.getpid(), thread.get_ident(), start, start + timeout)

        lockdir = os.path.abspath(os.path.join(self.lock_path, '..'))
        if not pylabs.q.system.fs.exists(lockdir):
            pylabs.q.system.fs.createDir(lockdir)

        data = struct.pack(self.STRUCT_FORMAT, *args)
        with open(self.lock_path, 'wb') as fd:
            fd.write(data)

    def acquire(self, timeout):
        '''Acquire the lock for a given timeframe

        @param timeout: Lock timeout in seconds
        @type timeout: number
        '''
        with FileLock(self.access_lock_name):
            if not self._free(False) and not self._safe(False):
                raise ObjectLockedException('Object is locked')

            self._write(timeout)

    def release(self):
        '''Release the lock'''
        #Actually we don't really need to release the lock since we are allowed
        #to reuse it etc. Just keep this to maintain a lock-like API and make
        #our context manager code happy
        pass

    def force_release(self):
        '''Force-release the lock

        This, in contrast to L{release}, actually releases the lockfile, so the
        lock can't be re-used anymore, even if it timed out already.
        '''
        with FileLock(self.access_lock_name):
            if not self._safe(False):
                raise ObjectNotOwnedException( \
                    'Object not owned by current thread')
            pylabs.q.system.fs.removeFile(self.lock_path)

    #These are used to use CMDBLock as a context manager
    def __enter__(self):
        self.acquire(MAX_LOCK_TIMEOUT)

    def __exit__(self, *exc_info):
        self.release()


class CMDBObject(object):
    '''Access methods to an on-disk CMDB object'''
    def __init__(self, type_name, base_dir):
        '''Initialize a new CMDBObject

        @param type_name: CMDB object type name
        @type type_name: string
        @param base_dir: Base folder of CMDB storage
        @type base_dir: string
        '''
        self.type_name = type_name
        self.base_dir = base_dir

    @property
    def dir_path(self):
        '''Storage folder of this object'''
        return pylabs.q.system.fs.joinPaths(self.base_dir, self.type_name)

    @property
    def config_path(self):
        '''Path to configuration file of this object'''
        return pylabs.q.system.fs.joinPaths(self.dir_path, 'main.cfg')

    def object_path(self, version):
        '''Path to object file of a given version of this object'''
        return pylabs.q.system.fs.joinPaths(
                self.dir_path, 'versions', '%s.db' % version)

    @property
    def exists(self):
        '''Check whether an object is stored in CMDB'''
        return pylabs.q.system.fs.exists(self.config_path)

    @property
    def value(self):
        '''Actual object value'''
        if not self.exists:
            raise UnknownObjectException('Unknown object %s in %s' % \
                    (self.type_name, self.base_dir, ))

        #dbfile found
        with open(self.config_path, 'r') as fd:
            version = fd.read()

        version = version.strip()

        with open(self.object_path(version), 'rb') as fd:
            object_ = pickle.load(fd)

        return object_

    def register(self):
        '''Register a new object type'''
        if not self.exists:
            pylabs.q.system.fs.createDir(
                    pylabs.q.system.fs.joinPaths(self.dir_path, 'versions'))

    def save(self, object_, register):
        '''Save an object to disk

        @param object_: Object to store
        @type object_: object
        @param register: Register object type if not found
        @type register: bool
        '''
        #Only save if we got the lock
        object_lock = self._cmdb_lock

        #Only check lock if object doesn't exist
        if self.exists:
            if not object_lock.safe:
                raise ObjectNotOwnedException('Object not owned by current thread')

        with object_lock:
            if register:
                self.register()

            path, version = self._calculate_new_object_path()

            with open(path, 'wb') as fd:
                pickle.dump(object_, fd)

            with open(self.config_path, 'w') as fd:
                fd.write(version)

            object_lock.force_release()

    def lock(self, timeout):
        '''Acquire a lock on this object type
        
        @param timeout: Lock lifetime in seconds
        @type timeout: number
        '''
        if self._cmdb_lock.safe and not self._cmdb_lock.free:
            raise DoubleLockException

        self._cmdb_lock.acquire(timeout)

    def unlock(self):
        '''Release lock on this object type'''
        object_lock = self._cmdb_lock

        if not object_lock.safe:
            raise ObjectNotOwnedException('Object not owned by current thread')

        object_lock.force_release()

    def is_locked(self):
        '''Check whether the object type is locked
        
        @return: Whether the object type is locked
        @rtype: bool
        '''
        object_lock = self._cmdb_lock
        return not object_lock.free

    def is_safe(self):
        '''Check whether the object type is safe to be saved by the current
        thread

        @return: Whether the object type is safe
        @rtype: bool
        '''
        object_lock = self._cmdb_lock
        return object_lock.safe

    def _calculate_new_object_path(self):
        '''Calculate path and version for a new object'''
        version = str(time.time())
        path = self.object_path(version)
        return path, version

    @property
    def _cmdb_lock(self):
        '''Create CMDBLock for the current object'''
        return CMDBLock(self.base_dir, self.type_name)


class CMDBContextManager(object):
    '''Context manager for CMDB objects, including lock/unlock'''
    def __init__(self, object_type_name):
        self.object_type_name = object_type_name

    def __enter__(self):
        return pylabs.q.cmdb.getObjectWithLock(self.object_type_name)

    def __exit__(self, *exc_info):
        #We can ignore ObjectNotOwnedException here, since it is possible the
        #object lock is no longer ours when the 'with' context is exited in the
        #consumer code. If the lock would not be owned where necessary inside
        #the with context, the exception will be propagated upstream, so that's
        #not an issue.
        try:
            pylabs.q.cmdb.releaseObjectLock(self.object_type_name)
        except ObjectNotOwnedException:
            pass


def getObject(objectTypeName, version=None):
    '''Get an object from the CMDB store, without locking

    Versioning is not implemented currently.

    @param objectTypeName: Name of the object type
    @type objectTypeName: string
    @param version: Version to retrieve
    @type version: string

    @return: CMDB object value
    @rtype: object

    @raise UnknownObjectException: Object type unknown
    '''
    pylabs.q.logger.log('[CMDB] Get object %s' % objectTypeName, 4)
    if version:
        raise NotImplementedError

    object_ = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)
    if not object_.exists:
        raise UnknownObjectException('Unknown object %s in %s' % \
                    (objectTypeName, pylabs.q.dirs.cmdbDir, ))

    return object_.value

def registerObject(objectTypeName, object_):
    '''Register and save a new object type

    @param objectTypeName: Name of the object type
    @type objectTypeName: string
    @param object_: Object to store
    @type object_: object

    @see: saveObject
    '''
    saveObject(objectTypeName, object_, True)

def saveObject(objectTypeName, object_, register=True):
    '''Save an object in CMDB

    @param objectTypeName: Name of the object type
    @type objectTypeName: string
    @param object_: Object to store
    @type object_: object
    @param register: Register the object type if unknown
    @type register: bool
    '''
    pylabs.q.logger.log('[CMDB] Save object %s' % objectTypeName, 4)
    cmdb_object = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)
    cmdb_object.save(object_, register)

def existsObject(objectTypeName):
    '''Check whether a given object type exists

    @param objectTypeName: Name of the object type
    @type objectTypeName: string

    @return: Whether the object type exists
    @rtype: bool
    '''
    pylabs.q.logger.log(
            '[CMDB] Check whether object %s exists' % objectTypeName, 5)
    return CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir).exists

def releaseObjectLock(objectTypeName):
    '''Release the lock on an object

    @param objectTypeName: Name of the object type
    @type objectTypeName: string
    '''
    pylabs.q.logger.log(
            '[CMDB] Release lock on object %s' % objectTypeName, 4)
    cmdb_object = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)
    try:
        cmdb_object.unlock()
    except ObjectNotOwnedException:
        pass

def getObjectWithLock(objectTypeName, locktimeout=DEFAULT_LOCK_TIMEOUT, \
        waittimeout=DEFAULT_WAIT_TIMEOUT, version=None):
    '''Lock an object and return the value

    @param objectTypeName: Name of the object type
    @type objectTypeName: string
    @param locktimeout: Lifetime of the lock in seconds
    @type locktimeout: number
    @param waittimeout: Maximum time to wait before the lock can be acquired
    @type waittimeout: number
    @param version: Version to retrieve
    @type version: string

    @return: CMDB object value
    @rtype: object

    @raise UnknownObjectException: Object type unknown
    @raise LockWaitTimeoutException: Lock acquisition timed out
    @raise ValueError: The locktimeout exceeds the maximum timeout value
    '''
    pylabs.q.logger.log('[CMDB] Get object %s with lock' % objectTypeName, 4)
    if version:
        raise NotImplementedError

    if locktimeout > MAX_LOCK_TIMEOUT:
        raise ValueError("Maximum lock timeout is %d seconds" % MAX_LOCK_TIMEOUT)

    cmdb_object = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)

    if not cmdb_object.exists:
        raise UnknownObjectException('Unknown object %s in %s' % \
                    (objectTypeName, pylabs.q.dirs.cmdbDir, ))

    start = time.time()
    locked = False

    while time.time() < start + waittimeout:
        try:
            cmdb_object.lock(locktimeout)
            locked = True
            break
        except ObjectLockedException:
            time.sleep(0.1)

    if locked:
        return getObject(objectTypeName, version)

    raise LockWaitTimeoutException('Unable to get lock in time')

def isLocked(objectTypeName):
    '''Check whether the object is locked

    @param objectTypeName: Name of the object type
    @type objectTypeName: string

    @return: Whether the object is locked
    @rtype: bool
    '''
    cmdb_object = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)
    return cmdb_object.is_locked()

def isSafe(objectTypeName):
    '''Check whether access to the object is safe

    @param objectTypeName: Name of the object type
    @type objectTypeName: string

    @return: Whether the object can be saved safely
    @rtype: bool
    '''
    cmdb_object = CMDBObject(objectTypeName, pylabs.q.dirs.cmdbDir)
    return cmdb_object.is_safe()


class CMDB:
    '''Exposure class of CMDB access methods'''
    getObject = staticmethod(getObject)
    getObjectWithLock = staticmethod(getObjectWithLock)
    existsObject = staticmethod(existsObject)
    saveObject = staticmethod(saveObject)
    #registerObject is kept for backwards compatibility. It is the same as
    #saveObject
    registerObject = staticmethod(registerObject)
    releaseObjectLock = staticmethod(releaseObjectLock)

    #This is internal, mainly for testing purposes, since not exposed in the
    #spec
    pm_isLocked = staticmethod(isLocked)

    #This is our context processor code
    def __call__(self, objectTypeName):
        '''Use CMDB as a context processor

        >>> with q.cmdb('myobject') as value:
        ...     value.a = 123
        ...     q.cmdb.saveObject('myobject', value)
        '''
        return CMDBContextManager(objectTypeName)