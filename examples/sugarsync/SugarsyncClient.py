from xml.dom import minidom
from xml2collections import xml2Dic as reformat
from SugarsyncObjects import *
import re
import urllib2, urllib
import base64
import mimetypes
import mimetools

from pylabs import q
#sugarsync status codes: http://www.sugarsync.com/developers/rest-api-reference/responseCodes/index.html

HTTP_CREATED = '201' #from practical examples, authorization created returns 201
HTTP_OK = '200'
HTTP_NO_CONTENT = '204' #An authorization token was created and provided to the client in the Location header.
HTTP_AUTH_REQUIRED = '401' # Authorization required.
HTTP_FORBIDDEN = '403(Forbidden)' #Authentication failed.
HTTP_NOT_FOUND = '404'

STATUS_OK = set([HTTP_CREATED, HTTP_OK, HTTP_NO_CONTENT])

AUTHORIZATION_HEADER = 'Authorization'

class SugarsyncClient(object):

    def __init__(self):
        self._auth_token = None
        self.recentFolders = None
        self.recentFiles = None

    def _clean(self, s):
        # Remove invalid characters
        s = re.sub('[^0-9a-zA-Z_]', '', s)
        # Remove leading characters until we find a letter or underscore
        s = re.sub('^[^a-zA-Z_]+', '', s)
        return s

    def login(self):
        cfgfile = q.tools.inifile.open( 'sugarsync.cfg')
        credendtials = cfgfile.getSectionAsDict('sugarsync_account') #loses case of the keys, can't be passed useing **kwargs!
        return self.authenticate(username=credendtials['username'], password=credendtials['password'], 
                                  accessKeyId=credendtials['accesskeyid'], privateAccessKey=credendtials['privateaccesskey'])
    
    def authenticate(self, username, password, accessKeyId, privateAccessKey):
        '''Creating an Authorization Token'''
        _baseurl = 'https://api.sugarsync.com/authorization'
        params = {'username':username, 'password':password, 'accessKeyId':accessKeyId, 'privateAccessKey':privateAccessKey}
        template = '''<?xml version="1.0" encoding="UTF-8" ?>
<authRequest>
    <username>%(username)s</username>
    <password>%(password)s</password>
    <accessKeyId>%(accessKeyId)s</accessKeyId>
    <privateAccessKey>%(privateAccessKey)s</privateAccessKey>
</authRequest>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : self._auth_token}
        resp = self._http_request(_baseurl, None, data=data, headers=headers)
        self._populateUserSession(resp)                                                                                                
        
    def _populateUserSession(self, resp):
        self.recentFolders = Hook()
        self.recentFiles = Hook()
        bodyDic = reformat(resp.read())
        self._auth_token_expiration = bodyDic['authorization'].expiration
        self._auth_user = bodyDic['authorization'].user
        self._auth_token = resp.headers['location']
        self.user = self.getUserInfo()

    def getUserInfo(self):
        '''Retrieving User Information'''
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = 'https://api.sugarsync.com/user'
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        user = User(resp.read())
        setattr(self.recentFolders, 'home', user.webArchive)
        return user

    def _crudFolder(self, folderUrl, displayName, method):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = folderUrl #'https://api.sugarsync.com/folder/myfolder'
        if method == 'DELETE':
            params, data = None
        else:
            params = {'displayName' : displayName}
            template = '''<?xml version="1.0" encoding="UTF-8"?>
    <folder>
        <displayName>%(displayName)s</displayName>
    </folder>'''
            data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data) if data else 0
                   ,'Authorization' : self._auth_token}

        resp = self._http_request(_baseurl, data=data, headers=headers, method=method)
        if method == 'DELETE': 
            return resp
        else:
            setattr(self.recentFolders, self._clean(displayName), resp.headers['location'])
            return resp

    def createFolder(self, parentFolderUrl, displayName):
        return self._crudFolder(parentFolderUrl, displayName, 'POST')

    def renameFolder(self, folderUrl, displayName):
        return self._crudFolder(folderUrl, displayName, 'PUT')
    
    def deleteFolder(self, folderUrl):
        return self._crudFolder(folderUrl, None, 'DELETE')
    
    def _crudFile(self, fileUrl, displayName, mediaType, method, opt=None):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = fileUrl
        if method == 'DELETE':
            params, data = None
        else:
            params = {'displayName' : displayName, 'mediaType' : mediaType, 'optional' : '<ParentCollection>%s</ParentCollection>'%opt if opt else ''}
            template = '''<?xml version="1.0" encoding="UTF-8"?>
    <file>
        <displayName>%(displayName)s</displayName>
        <mediaType>%(mediaType)s</mediaType>
        %(optional)s
    </file>'''
            data = template%params
            
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data) if data else 0
                   ,'Authorization' : self._auth_token}
        resp = self._http_request(_baseurl, data=data, headers=headers, method=method)
        if method == 'DELETE': 
            return resp
        else:
            newfileUrl = resp.headers['location']
            setattr(self.recentFiles, self._clean(displayName), newfileUrl)
            return newfileUrl
        
    def createFile(self, parentFolderUrl, displayName, mediaType):
        return self._crudFile(parentFolderUrl, displayName, mediaType, 'POST')
    
    def renameFile(self, fileUrl, newDisplayName, newMediaType, parentFolderUrl=None):
        return self._crudFile(fileUrl, newDisplayName, newMediaType, 'PUT', opt=parentFolderUrl)
        
    def deleteFile(self, fileUrl):
        return self._crudFile(fileUrl, None, None, method='DELETE')
    
    def copyFile(self, sourceFileUrl, targetFolder, targetFileName):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = targetFolder
        params = {'source' : sourceFileUrl, 'displayName' : targetFileName}
        template = '''<?xml version="1.0" encoding="UTF-8"?>
<fileCopy source="%(source)s">
   <displayName>%(displayName)s</displayName>
</fileCopy>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : self._auth_token}
        resp = self._http_request(_baseurl, data=data, headers=headers, method='POST')
        return resp
    
    def _crudPublicFileLink(self, fileUrl, enable=True):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = fileUrl
        params = {'enabled' : str(enable).lower()}
        template = '''<?xml version="1.0" encoding="UTF-8"?>
<file>
<publicLink enabled="%(enabled)s"/>
</file>'''
        data = template%params
        headers = {'Content-Type' : 'application/xml'
                   ,'Content-Length' : len(data)
                   ,'Authorization' : self._auth_token}
        resp = self._http_request(_baseurl, data=data, headers=headers, method='PUT')
        file = File(resp.read())
        return file
    
    def filePublicLinkCreate(self, fileUrl):
        return self._crudPublicFileLink(fileUrl, True)
        
    def filePublicLinkDestroy(self, fileUrl):
        return self._crudPublicFileLink(fileUrl, False)
             
    def getFolderInfo(self, folderUrl):
        '''Retrieving Folder Representation'''
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = folderUrl
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        folder = Folder(resp.read())
        return folder

    def getFileInfo(self, fileUrl):
        '''Retrieving File Representation'''
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = fileUrl
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        file = File(resp.read())
        return file

    def getWorkspaceInfo(self, workspaceUrl):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = workspaceUrl
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        workspace = Workspace(resp.read())
        return workspace
    
    def getAlbumsCollectionInfo(self, albumsUrl):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = albumsUrl
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        albums = Albums(resp.read())
        return albums
    
    def getAlbumInfo(self, albumUrl):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = albumUrl
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        album = Album(resp.read())
        return album

    def _updateUrlParams(self, url, **kwargs):
        _scheme, _netloc, _url, _params, _query, _fragment = urllib2.urlparse.urlparse(url)
        params = urllib2.urlparse.parse_qs(_query)
        for k, v in params:#parse_qs puts the values in a list which corrupts the url later on
            params[k] = v.pop() if isinstance(v, list) else v
            
        for k, v in kwargs.items():
            if v is not None: params[k] = v
        _query = urllib.urlencode(params)
        return urllib2.urlparse.urlunparse((_scheme, _netloc, _url, _params, _query, _fragment))

    def getCollectionContents(self, contentsUrl, type=None, start=0, max_=500):
        '''RetrievingCollectionContentsRepresentation'''
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = contentsUrl if contentsUrl.split('/')[-1].startswith('contents') else '%s/contents'%contentsUrl
        _baseurl = self._updateUrlParams(_baseurl, type=type, start=start, max=max_)
        resp = self._http_request(_baseurl, headers={'Authorization' : self._auth_token})
        coll = CollectionContents(resp.read())
        return coll

    def getFolderContents(self, folderUrl, start=0, max_=500):
        return self.getCollectionContents(folderUrl, 'file', start, max_)

    def getWorkspaceContents(self, workspaceUrl, start=0, max_=500):
        return self.getCollectionContents(workspaceUrl, 'folder', start, max_)
    
    def getAlbumsCollectionContents(self, albumsCollectionUrl, start=0, max_=500):
        return self.getCollectionContents(albumsCollectionUrl, type='folder', start=start, max_=max_)
    
    def getAlbumContents(self, albumUrl, start=0, max_=500):
        return self.getCollectionContents(albumUrl, type=None, start=start, max_=max_)

    def _http_request(self, url, args=None, data=None, headers=None, method=None):
        request = urllib2.Request(url, data=data)
        if headers:
            for key, value in headers.iteritems():
                request.add_header(key, value)
        if not method:
            method = 'POST' if data else 'GET'
        request.get_method = lambda: method
        resp = urllib2.urlopen(request)
        if resp.code not in (201, 200, 204):
            raise Exception('unexpected HTTP response status %s'%resp.code)
        return resp
        
    def putFileData(self, fileUrl, localFilePath):
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _baseurl = fileUrl if fileUrl.split('/')[-1].startswith('data') else '%s/data'%fileUrl
        data = open(localFilePath).read()
        content_type = mimetypes.guess_type(localFilePath)[0]
        headers = {'Content-Type' : content_type
                   ,'Content-Length' : len(data)
                   ,'Authorization' : self._auth_token}
        resp = self._http_request(_baseurl, data=data, headers=headers, method='PUT')
            
    def retrieveFileData(self, fileUrl, downloadPath, customHeaders=None):
        '''
        urllib has an advantage over urllib2 that it handles automatic download of files, currently it doesn't support base64 decoding of content
        '''
        _baseurl = fileUrl if fileUrl.split('/')[-1].startswith('data') else '%s/data'%fileUrl        
        if not self._auth_token: raise Exception('Not logged in, must authenticate first')
        _urlopener = urllib.FancyURLopener()
        _urlopener.addheader('Authorization', self._auth_token)
        if customHeaders:
            for k, v in customHeaders.items():
                _urlopener.addheader(k, v)
        return _urlopener.retrieve(_baseurl, downloadPath, None, None)
    
    def retrieveEditedImage(self, imageUrl, downloadPath, widthPixels, heightPixels, square=False, clockWiseRotationCount=0):
        imageTranscodingHeader = 'image/jpeg; pxmax=%(widthPixels)s;pymax=%(heightPixels)s;sq=(%(square)d);r=(%(clockWiseRotationCount)d);'
        customHeaders = {'Accept' : imageTranscodingHeader%{'widthPixels' : widthPixels, 'heightPixels' : heightPixels, 'square' : 1 if square else 0, 'clockWiseRotationCount' : clockWiseRotationCount%4}}
        return self.retrieveFileData(imageUrl, downloadPath, customHeaders)
        

 
