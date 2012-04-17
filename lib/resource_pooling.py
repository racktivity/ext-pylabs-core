# @todo provide correct licence header

import random
import threading
from functools import wraps
from abc import ABCMeta, abstractmethod


class AbstractResourcePool(object):
    '''
    AbstractResourcePool is an abstract class that provides functionality to pool
    resources. It also provides functionality to (automatically) maintain/clean
    itself.

    Extend this class and implement the _getNewResource method to create a
    resource pool for a custom object.

    *Important!*
    The pool doesn't provide a way to lock itself and its resources. It should
    therefore only be used in threads that are scheduled cooperatively. If not
    pool cleaning will not be reliable. To recapitulate, the pool is not thread-
    safe for concurrent access.

    *Important!*
    Note that pool its resource management is error prone. For instance, it is
    possible use a resource after releasing it back into the pool. This can
    result in very unexpected behaviour. It is therefore advisable to never
    store a reference to a resource.
    '''

    __metaclass__ = ABCMeta

    DEFAULT_MAX_SIZE = 1000

    def __init__(self, poolsize=DEFAULT_MAX_SIZE, *args, **kwargs):
        '''
        AbstractResourcePool constructor.

        @param maxSize: maximum size of the pool, defaults to
            AbstractResourcePool.DEFAULT_MAX_SIZE
        @type maxSize: Integer
        '''

        self.maxSize = poolsize
        self._args = args
        self._kwargs = kwargs

        self._available = set()
        self._acquired = set()
        self._lock = threading.RLock()

        self._isAutoCleaning = False
        self._autoCleanGreenlet = None

    def _threadsafe(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                return func(self, *args, **kwargs)
        return wrapper

    @property
    def maxSize(self):
        '''
        Gets the maximum size of the pool.

        @return: maximum size of the pool
        @rtype: Integer
        '''

        return self._maxSize

    @maxSize.setter
    def maxSize(self, size):
        '''
        Sets the maximum size of the pool (after validating it).

        @param size: maximum size of the pool
        @type size: Integer
        '''

        if not isinstance(size, int):
            errorMessage = 'Invalid maximum size type, expected integer'
            self._log(errorMessage, 2)
            raise TypeError(errorMessage)
        elif size < 1:
            errorMessage = 'Invalid maximum size value, expected non zero'\
                ' positive number'
            self._log(errorMessage, 2)
            raise ValueError(errorMessage)

        self._maxSize = size

    @property
    def numberAvailable(self):
        '''
        Gets the number of available resources.

        @return: number of available resources
        @rtype: Integer
        '''

        return len(self._available)

    @property
    def numberAcquired(self):
        '''
        Gets the number of acquired resources.

        @return: number of acquired resources
        @rtype: Integer
        '''

        return len(self._acquired)
    
    @_threadsafe
    def acquire(self):
        '''
        Acquires a resource from the pool. When none available, a new one is
        created.

        @return: available resource
        @rtype: Object
        '''

        self._logWithStats('Acquiring pool resource', 4)

        resource = self._findAvailable()

        if resource:
            self._available.remove(resource)
            self._acquired.add(resource)
        else:
            resource = self._acquireNew()

        self._logWithStats('Acquired pool resource', 4)

        return resource

    @_threadsafe
    def release(self, resource):
        '''
        Releases a previously acquired resource back to the pool.

        @param resource: acquired resource to release
        @type resource: Object
        '''

        self._logWithStats('Releasing pool resource', 4)

        if resource not in self._acquired:
            errorMessage = 'Could not release resource, resource not acquired'
            self._log(errorMessage, 2)
            raise LookupError(errorMessage)

        self._acquired.remove(resource)
        self._available.add(resource)

        self._logWithStats('Released pool resource', 4)

    @_threadsafe
    def destroy(self, resource):
        '''
        Destroys an available resource.

        @param resource: available resource to destroy
        @type resource: Object
        '''

        self._logWithStats('Destroying pool resource', 4)

        if resource not in self._available:
            errorMessage = 'Could not destroy resource, resource not available'\
                ', release resource before destroying it'
            self._log(errorMessage, 2)
            raise RuntimeError(errorMessage)

        self._available.remove(resource)

        self._logWithStats('Destroyed pool resource', 4)

    @_threadsafe
    def destroyAvailable(self):
        '''Destroys all available resources.'''

        self._logWithStats('Destroying all available pool resources', 4)

        availableResources = list(self._available)

        for resource in availableResources:
            self.destroy(resource)

        resourceCount = len(availableResources)
        self._logWithStats('Destroyed all (%d) available resources'
            % resourceCount, 4)

    @_threadsafe
    def releaseAndDestroy(self, resource):
        '''
        Releases and destroys a resource.

        @param resource: resource to release and destroy
        @type resource: Object
        '''

        self.release(resource)
        self.destroy(resource)

    
    @_threadsafe
    def clean(self):
        '''
        Cleans the pool destroying all unnecessary available resources.
        '''

        self._logWithStats('Cleaning pool', 4)

        resources = self._getResourcesToClean()

        for resource in resources:
            self.destroy(resource)

        resourceCount = len(resources)

        self._logWithStats('Cleaned pool, destroying %d unnecessary available'
            'resources' % resourceCount, 4)

    @_threadsafe
    def empty(self):
        '''
        Empties the pool destroying all available and acquired resources.
        '''

        self._logWithStats('Emptying pool', 4)

        for resource in list(self._available):
            self.destroy(resource)

        for resource in list(self._acquired):
            self.releaseAndDestroy(resource)

        totalCount = self.numberAvailable + self.numberAcquired

        self._logWithStats('Emptied pool, destroying %d resources' % totalCount,
            4)

    def getStats(self):
        '''
        Gets the stats of the pool.

        @return: stats of the pool
        @rtype: String
        '''

        return '''\
available: %d
acquired: %d''' % (self.numberAvailable, self.numberAcquired)

    
    def _findAvailable(self):
        '''
        Finds an available resource.

        @return: available resource, None when none are available
        @rtype: Object
        '''

        if self._available:
            availableResources = list(self._available)
            return random.choice(availableResources)
        else:
            return None

    def _acquireNew(self):
        '''
        Acquires a newly created resource.

        @return: new resource
        @rtype: Object
        '''

        totalCount = self.numberAvailable + self.numberAcquired

        if (totalCount + 1) > self._maxSize:
            if self._available:
                self.clean()
            else:
                errorMessage = 'Cannot acquire a new resource because the pool'\
                    'size will exceed the maximum %d' % self._maxSize
                self._log(errorMessage, 2)
                raise RuntimeError(errorMessage)

        resource = self._getNewResource()
        self._acquired.add(resource)

        return resource

    def _getResourcesToClean(self):
        '''
        Gets the resources to be cleaned (destroyed) by the cleaner.

        @return: set of resources to be cleaned (destroyed)
        @rtype: Set(Object)
        '''

        return self._available.copy()

    def _logWithStats(self, message, lvl):
        '''
        Logs a message suffixed with the pool stats.

        @param message: message to log
        @type message: String

        @param lvl: level of the log message
        @type lvl: Integer
        '''

        rawStats = self.getStats()
        rawStatsLines = rawStats.split('\n')
        rawStatsLine = ' - '.join(rawStatsLines)
        messageWithStats = '%s (%s)' % (message, rawStatsLine)
        self._log(messageWithStats, lvl)

    @abstractmethod
    def _log(self, message, lvl):
        '''
        Logs a message.

        @param message: message to log
        @type message: String

        @param lvl: level of the log message
        @type lvl: Integer
        '''

        raise NotImplementedError()

    @abstractmethod
    def _getNewResource(self):
        '''
        Gets a new resource.

        @return: new resource
        @rtype: Object
        '''

        raise NotImplementedError()
