from pylabs import q
import cgi
import os
import errno
import urllib
from urllib2 import URLError


class VFSClientExtension(object):
    def __init__(self):
        pass
    
    def getConnection(self, host, port, sslEnabled=False):
        ''' Establishes an HTTP connection on the given host, and port
        
        @param host: The IP address to connect to
        @param port: The port number to connect to
        @param sslEnabled: If True, the client will attempt to invoke methods on top of https instead of http
        
        @return: A connection instance of VFSClientConnection '''
        
        return VFSClientConnection(host, port, sslEnabled)

class VFSClientConnection():
    def __init__(self, host, port, sslEnabled):
        self.host = host
        self.port = port
        self.sslEnabled = sslEnabled
        self.httpConnection = q.clients.http.getConnection()
    
    def _formatUrl(self, service, **kwargs):
        args = {'host': self.host,
                'port': self.port,
                'service': service,
                'params': urllib.urlencode(kwargs)}
        if self.sslEnabled:
            return 'https://%(host)s:%(port)s/%(service)s?%(params)s'%args
        else:            
            return 'http://%(host)s:%(port)s/%(service)s?%(params)s'%args
    
    def fileGetInfo(self, path):
        ''' Gets file info from the Server\'s VFS object store 
        
        @param path: The absolute path of the file
        
        @return: A dictionary of the file information
        '''
        url = self._formatUrl(service='fileGetInfo', path=path)
        try:
            result = self.httpConnection.get(url)
        except Exception as ex:
            return 'Exception encountered. Message: %s'%ex.info
        return eval(result.read())
    
    def dirstat(self, path):
        ''' Gets directory info from the Server\'s VFS object store 
        
        @param path: The absolute path of the directory
        
        @return: A dictionary of the directory information
        '''        
        url = self._formatUrl(service='dirstat', path=path)
        try:
            result = self.httpConnection.get(url)
        except Exception as ex:
            return 'Exception encountered. Message: %s'%ex.info       
        return eval(result.read())
    
    def listVersions(self):
        ''' Lists the metadata versions of VFS Server 
        
        @return: A dictionary of metadata versions in the form of 'Human-readable Epoch version':Epoch Version'''
        
        url = self._formatUrl(service='listVersions')
        try:
            result = self.httpConnection.get(url)
        except Exception as ex:
            return 'Exception enountered. Message: %s'%ex.info
        return eval(result.read())
    
    def getFromVersionEpoch(self, versionEpoch):
        ''' Instructs the VFS server to point to the metadata epoch version specified
        
        @param versionEpoch: The epoch version to retrieve'''
        
        url = self._formatUrl('getFromVersionEpoch', versionEpoch=versionEpoch)
        try:
            result = self.httpConnection.get(url)
        except Exception as ex:
            return 'Exception enountered. Message: %s'%ex.info
        return eval(result.read())
    
    def getLatest(self):
        ''' Instructs the VFS server to point to the latest metadata version'''
        
        url = self._formatUrl('getLatest')
        try:
            result = self.httpConnection.get(url)
        except Exception as ex:
            return 'Exception enountered. Message: %s'%ex.info
        return eval(result.read())        
    
    
    