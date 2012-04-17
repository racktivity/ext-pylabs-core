# @todo provide correct licence header

import operator

from pylabs import q
from functools import wraps
from resource_pooling import AbstractResourcePool


class ArakoonPoolClient(object):

    def __init__(self, clusterName, namespace=None, poolsize=100):
        '''
        Constructor of a database client for application server. The database
        client is actually a wrapped extended arakoon client.

        @param clusterName: name of the cluster to create the client for
        @type clusterName: String

        @param namespace: namespace the client should use
        @type namespace:String
        '''
        self._pool = ArakoonPool(poolsize, clusterName, namespace)


    def _withPool(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            client = self._pool.acquire()
            try:
                return getattr(client, func.__name__)(*args, **kwargs)
            finally:
                self._pool.release(client)
        return wrapper


    @_withPool
    def exists(self, key):
        '''
        @type key : string
        @param key : key
        @return : True if there is a value for that key, False otherwise
        '''

    @_withPool
    def get(self, key):
        '''
        Retrieve a single value from the store.

        Retrieve the value associated with the given key

        @type key: string
        @param key: The key whose value you are interested in

        @rtype: string
        @return: The value associated with the given key
        '''

    @_withPool
    def multiGet(self, keys):
        '''
        Retrieve the values for the keys in the given list.

        @type key: string list
        @rtype: string list

        @return: the values associated with the respective keys
        '''

    @_withPool
    def set(self, key, value):
        '''
        Update the value associated with the given key.

        If the key does not yet have a value associated with it, a new key value pair will be created.
        If the key does have a value associated with it, it is overwritten.
        For conditional value updates see L{testAndSet}

        @type key: string
        @type value: string
        @param key: The key whose associated value you want to update
        @param value: The value you want to store with the associated key

        @rtype: void
        '''

    @_withPool
    def delete(self, key):
        '''
        Remove a key-value pair from the store.

        @type key: string
        @param key: Remove this key and its associated value from the store

        @rtype: void
        '''

    @_withPool
    def range(self, beginKey="", beginKeyIncluded=True, endKey="", endKeyIncluded=True, maxElements=-1):
        '''
        Perform a range query on the store, retrieving the set of matching keys

        Retrieve a set of keys that lexographically fall between the beginKey and the endKey
        You can specify whether the beginKey and endKey need to be included in the result set
        Additionaly you can limit the size of the result set to maxElements. Default is to return all matching keys.

        @type beginKey: string option
        @type beginKeyIncluded: boolean
        @type endKey :string option
        @type endKeyIncluded: boolean
        @type maxElements: integer
        @param beginKey: Lower boundary of the requested range
        @param beginKeyIncluded: Indicates if the lower boundary should be part of the result set
        @param endKey: Upper boundary of the requested range
        @param endKeyIncluded: Indicates if the upper boundary should be part of the result set
        @param maxElements: The maximum number of keys to return. Negative means no maximum, all matches will be returned. Defaults to -1.

        @rtype: list of strings
        @return: Returns a list containing all matching keys
        '''

    @_withPool
    def range_entries(self, beginKey="", beginKeyIncluded=True, endKey="", endKeyIncluded=True, maxElements=-1):
        '''
        Perform a range query on the store, retrieving the set of matching key-value pairs

        Retrieve a set of keys that lexographically fall between the beginKey and the endKey
        You can specify whether the beginKey and endKey need to be included in the result set
        Additionaly you can limit the size of the result set to maxElements. Default is to return all matching keys.

        @type beginKey: string option
        @type beginKeyIncluded: boolean
        @type endKey :string option
        @type endKeyIncluded: boolean
        @type maxElements: integer
        @param beginKey: Lower boundary of the requested range
        @param beginKeyIncluded: Indicates if the lower boundary should be part of the result set
        @param endKey: Upper boundary of the requested range
        @param endKeyIncluded: Indicates if the upper boundary should be part of the result set
        @param maxElements: The maximum number of key-value pairs to return. Negative means no maximum, all matches will be returned. Defaults to -1.

        @rtype: list of strings
        @return: Returns a list containing all matching key-value pairs
        '''

    @_withPool
    def prefix(self, keyPrefix='', maxElements=-1):
        '''
        Retrieve a set of keys that match with the provided prefix.

        You can indicate whether the prefix should be included in the result set if there is a key that matches exactly
        Additionaly you can limit the size of the result set to maxElements

        @type keyPrefix: string
        @type maxElements: integer
        @param keyPrefix: The prefix that will be used when pattern matching the keys in the store
        @param maxElements: The maximum number of keys to return. Negative means no maximum, all matches will be returned. Defaults to -1.

        @rtype: list of strings
        @return: Returns a list of keys matching the provided prefix
        '''

    @_withPool
    def testAndSet(self, key, oldValue, newValue):
        '''
        Conditionaly update the value associcated with the provided key.

        The value associated with key will be updated to newValue if the current value in the store equals oldValue
        If the current value is different from oldValue, this is a no-op.
        Returns the value that was associated with key in the store prior to this operation. This way you can check if the update was executed or not.

        @type key: string
        @type oldValue: string option
        @type newValue: string
        @param key: The key whose value you want to updated
        @param oldValue: The expected current value associated with the key.
        @param newValue: The desired new value to be stored.

        @rtype: string
        @return: The value that was associated with the key prior to this operation
        '''


class ArakoonPool(AbstractResourcePool):

    def _getResourcesToClean(self):
        '''
        Gets the clients to be cleaned (destroyed) by the cleaner. In this
        case the oldest half of the total number of available clients.

        @return: set of clients to be cleaned (destroyed)
        @rtype: Set(DbClient)
        '''

        sortedClients = sorted(self._available,
            key=operator.attrgetter('pm_age'))
        middleIndex = len(sortedClients) / 2
        oldestClients = sortedClients[middleIndex:]

        return set(oldestClients)

    def _log(self, message, lvl):
        '''
        Logs a message with the q logger.

        @param message: message to log
        @type message: String

        @param lvl: level of the log message
        @type lvl: Integer
        '''

        q.logger.log(message, lvl)

    def _getNewResource(self, *args, **kwargs):
        '''
        Gets a new client.

        @param clusterName: name of the cluster the client should work with
        @type clusterName: String

        @return: new client
        @rtype: DbClient
        '''

        return q.clients.arakoon.getClient(*self._args, **self._kwargs)



