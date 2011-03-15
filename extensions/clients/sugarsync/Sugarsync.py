import mimetypes
from urllib2 import HTTPError
from SugarsyncObjects import Hook
from SugarsyncObjects import xml2Dic as reformat
from SugarsyncObjects import cleanString
from pylabs import q
from functools import partial
import SugarsyncClient 
class Sugarsync(object):
    '''
    High level client for Sugarsync APIs
    '''
    
    def connect(self):
        '''
        Authenticate to sugarsync REST webservices
        
        The connect method uses the sugarsync.cfg ini file that should hold valid username, password, AccessKeyID and privateAccessKey
        the method populates the q.clients.sugarsync.user object with user information upon sucessful login
        
        @return: None
        '''
        self.client = q.clients.sugarsyncapi 
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'sugarsync', 'sugarsync.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        credentials = cfgfile.getSectionAsDict('sugarsync_account')
        self.client.authenticate(**credentials)
        self.user = self.client.user
        self._copyMethods()
        
    def listHomeFolders(self):
        '''
        Lists the folder in the webArchive associated with the current workspace
        
        The method lists the subfolders of the webArchive
        @return: list of Folder object containing essential folder attributes e.g. ref, displayName.
        '''
        coll = q.clients.sugarsyncapi.getSubFolders(q.clients.sugarsync.user.webArchive)
        return map(lambda attr: getattr(coll, attr), filter(lambda attr: attr.startswith('collection'), dir(coll)))
    
    def listHomeFolderUrls(self):
        '''
        Lists the folder URLs in the webArchive associated with the current workspace
        
        The method lists the subfolders of the webArchive
        @return: list of of URLs
        '''
        coll = self.listHomeFolders()
        return map(lambda x: x.ref, coll)
    
    def listHomeFiles(self):
        '''
        Lists the files in the webArchive associated with the current workspace
        
        The method lists the files in the webArchive
        @return: list of File object containing essential folder attributes e.g. ref, displayName, size, presentOnServer and mediaType
        '''        
        coll = q.clients.sugarsyncapi.getFolderContents(q.clients.sugarsync.user.webArchive)
        return map(lambda attr: getattr(coll, attr), filter(lambda attr: attr.startswith('file'), dir(coll)))
    
    def listHomeFileUrls(self):
        '''
        Lists the file URLs in the webArchive associated with the current workspace
        
        The method lists the files in the webArchive
        @return: list of of URLs
        '''
        coll = self.listHomeFiles()
        return map(lambda x: x.ref, coll)
    
    def _copyMethods(self):
        methodNames = ['copyFile',
 'createFolder',
 'deleteFile',
 'deleteFolder',
 'filePublicLinkCreate',
 'filePublicLinkDestroy',
 'getAlbumContents',
 'getAlbumInfo',
 'getAlbumsCollectionContents',
 'getAlbumsCollectionInfo',
 'getCollectionContents',
 'getFileInfo',
 'getFolderContents',
 'getFolderInfo',
 'getSubFolders',
 'getWorkspaceContents',
 'getWorkspaceInfo',
 'recentFiles',
 'recentFolders',
 'renameFile',
 'renameFolder',
 'retrieveEditedImage',
 'retrieveFileData']
        for name in methodNames:
            setattr(self, name, getattr(q.clients.sugarsyncapi, name))
    
    def getConnection(self, email, password=None, accesskeyid=None, privateaccesskey=None, saveCredentials=False):
        return SugarsyncConnection(email, password, accesskeyid, privateaccesskey, saveCredentials)
    
class SugarsyncConnection(object):
    def __init__(self, email, password=None, accesskeyid=None, privateaccesskey=None, saveCredentials=False):
        resp = None
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'sugarsync', 'sugarsync.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        if password and accesskeyid and privateaccesskey:
            try:
                resp = q.clients.sugarsyncapi.authenticate(email, password, accesskeyid, privateaccesskey)
            except HTTPError, ex:
                q.logger.log(ex)
                if ex.code == SugarsyncClient.HTTP_AUTH_REQUIRED:
                    raise RuntimeError('Authorization Error: Wrong credentials, please verify and try again')
            if saveCredentials:
                cfgfile.addSection(email)
                params = {'username':email, 'password':password, 'accessKeyId':accesskeyid, 'privateAccessKey':privateaccesskey}
                for k, v in params.items():
                    cfgfile.addParam(email, k, v)
        else:
            if cfgfile.checkSection(email):
                credentials = cfgfile.getSectionAsDict(email)
                resp = q.clients.sugarsyncapi.authenticate(**credentials)
            else:
                raise RuntimeError('Credentials not stored, please enter full credentials')    
        self._initConnection(resp)
                    
    def _initConnection(self, resp):                
        bodyDic = reformat(resp.read())
        self._auth_token_expiration = bodyDic['authorization'].expiration
        self.user = bodyDic['authorization'].user
        self._auth_token = resp.headers['location']
        self._user_session = q.clients.sugarsyncapi.getUserInfo(self._auth_token)
        self.folders = Folder(self, self._user_session.webArchive, 'home')
            
        
class Folder(object):
    def __init__(self, conn, baseurl, displayName, hasChildren=True):
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        setattr(self, 'new', partial(self._new, self._baseurl))
        setattr(self, 'files', Files(self._conn, self._baseurl))
        if hasChildren:
            children = q.clients.sugarsyncapi.getSubFolders(self._conn._auth_token, self._baseurl)
            map(lambda folderObj: setattr(self, cleanString(folderObj._displayName), folderObj),
                map(lambda initArgs: Folder(*initArgs),
                    [(self._conn, col.ref, col.displayName) for col in 
                        map(lambda attr: getattr(children, attr), 
                            filter(lambda attr: attr.startswith('collection'), dir(children))
                        )
                    ]
                )
            )
            
    def _new(self, parentUrl, displayName):
        newfolderUrl = q.clients.sugarsyncapi.createFolder(self._conn._auth_token, parentUrl, displayName)
        setattr(self, cleanString(displayName), Folder(self._conn, newfolderUrl, displayName, False))
          
class Files(object):
    def __init__(self, conn, parentUrl):
        self._conn = conn
        self._parentUrl = parentUrl
        children = q.clients.sugarsyncapi.getFolderContents(self._conn._auth_token, self._parentUrl)
        map(lambda fileObj: setattr(self, cleanString(fileObj._displayName), fileObj),
            map(lambda initArgs: File(*initArgs),
                [(self._conn, col.ref, col.displayName) for col in 
                    map(lambda attr: getattr(children, attr), 
                        filter(lambda attr: attr.startswith('file'), dir(children))
                    )
                ]
            )
        )
        
    def new(self, localFilePath, displayName=None, mediaType='application/octet-stream'):
        self._putFile(localFilePath, self._parentUrl, displayName, mediaType)
        
    def _putFile(self, localFilePath, parentFolderUrl, displayName=None, mediaType='application/octet-stream'):
        '''Puts a new file from local path to sugarsync
        
        This scenario method creates the file metadata entry and then puts the file data if successful
        the new file url is set as an attribute of the q.clients.sugarsync.recentFiles with the displayName as attribute name
        @param localFilePath: a valid system path to the local file
        @type: path
        @param parentFolderUrl: a valid sugarsync folder url owned by the current user e.g. webArchive and sub folders
        @type: url
        @param displayName: an alias for the file on the server, if None the local file name would be used
        @type: string
        @param mediaType: a valid mime type describing the file content, if not specified the file extension would be used to guess a valid mimetype
        '''
        displayName = displayName or q.system.fs.getBaseName(localFilePath)
        mediaType = mimetypes.guess_type(localFilePath)[0] or mediaType 
        resp = q.clients.sugarsyncapi.createFile(self._conn._auth_token, parentFolderUrl, displayName, mediaType)
        #simple check for successful file metadata creation
        if not (isinstance(resp, str) and resp.startswith('https://api.sugarsync.com/file')): raise Exception('Error while creating file')
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, resp, localFilePath)
        setattr(self, cleanString(displayName), File(self._conn, resp, cleanString(displayName)))
        

class File(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)
        
    def upload(self, localFilePath):
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, self.fileData, localFilePath)
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)

    def download(self, localFilePath):
        if self.presentOnServer:
            q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
        else:
            return False