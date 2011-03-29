from pylabs import q
import mimetypes
from urllib2 import HTTPError
from SugarsyncObjects import Hook
from SugarsyncObjects import xml2Dic as reformat
from SugarsyncObjects import cleanString
from functools import partial
import SugarsyncClient 
class Sugarsync(object):
    '''
    High level client for Sugarsync APIs
    '''
        
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
        self.__dict__ = {}
        self.folders = None
        self.albums = None
        sessionDict = None
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'sugarsync', 'sugarsync.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        if password and accesskeyid and privateaccesskey:
            try:
                sessionDict = q.clients.sugarsyncapi.authenticate(email, password, accesskeyid, privateaccesskey)
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
                sessionDict = q.clients.sugarsyncapi.authenticate(**credentials)
            else:
                raise RuntimeError('Credentials not stored, please enter full credentials')    
        self._initConnection(sessionDict)
                    
    def _initConnection(self, sessionDict):                
        self._auth_token_expiration = sessionDict['auth_token_expiration']
        self.user = sessionDict['user']
        self._auth_token = sessionDict['auth_token']
        self._user_session = q.clients.sugarsyncapi.getUserInfo(self._auth_token)
        #self.reset()
        
    
    def __getattribute__(self, name):
        if name == 'folders' and object.__getattribute__(self, 'folders') == None:
            q.logger.log('getting attribute folders for connection',5)
            self.folders = Folders(self, self._user_session.webArchive)
            return object.__getattribute__(self, 'folders')
        elif name == 'albums' and object.__getattribute__(self, 'albums') == None:
            q.logger.log('getting attribute albums for connection',5)
            self.albums = Albums(self, self._user_session.albums, 'albums')
            return object.__getattribute__(self, 'albums')
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for connection' % name)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for connection' % name)
            return object.__getattribute__(self, name)


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def reset(self):
        self.folders = Folders(self, self._user_session.webArchive)
        self.albums = Albums(self, self._user_session.albums, 'albums')  
          
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__getattribute__(key)
            
        
class Folder(object):
    def __init__(self, conn, baseurl, displayName, hasChildren=True):
        q.logger.log('initializing Folder',5)
        self._subFolders = None
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        self.files = None
        self.__setattr__('new', partial(self._new, self._baseurl))
        self.__setattr__('_children', q.clients.sugarsyncapi.getSubFolders(self._conn._auth_token, self._baseurl))
        self._hasChildren = hasChildren
        
        self._subFolders = dict(zip(
                                    map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                        filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                            map(lambda attr: getattr(attr, 'ref'),
                                                filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values()))))
        
        map(lambda folderObj: self.__setattr__(cleanString(folderObj.displayName), None),
            filter(lambda attr: hasattr(attr, 'displayName'), self._children.__dict__.values()))
        
    def __getattribute__(self, name):
        if name == 'files' and object.__getattribute__(self, 'files') == None:
            q.logger.log('getting attribute "files" for folder %s'%object.__getattribute__(self, '_displayName'),5)
            self.files = Files(object.__getattribute__(self, '_conn'), object.__getattribute__(self, '_baseurl'))
            return self.files
        elif object.__getattribute__(self, '_subFolders') and name in object.__getattribute__(self, '_subFolders').keys() and object.__getattribute__(self, name) == None:
            q.logger.log('getting attribute "folder" named %s for folder %s' %(name, object.__getattribute__(self, '_displayName')),5)
            folderRef = object.__getattribute__(self, '_subFolders')[name]
            self.__setattr__(name, Folder(object.__getattribute__(self, '_conn'), folderRef, name))
            return object.__getattribute__(self, name)
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for folder %s' %(name, object.__getattribute__(self, '_displayName')))
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for folder %s' %(name, object.__getattribute__(self, '_displayName')))
            return object.__getattribute__(self, name)
        
        
    def _new(self, parentUrl, displayName):
        q.logger.log('in _new',5)
        newfolderUrl = q.clients.sugarsyncapi.createFolder(self._conn._auth_token, parentUrl, displayName)
        self.__setattr__(cleanString(displayName), Folder(self._conn, newfolderUrl, displayName, False))
        
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        
    def __getitem__(self, key):
        key = cleanString(key)
        q.logger.log('getting item %s'%key, 5)
        if not self.files == None and key in self.files._files.keys():
            q.logger.log('found item in files', 5)
            return self.files[key]
        else:
            self.__getattribute__('files')
            if key in self.files._files.keys():
                q.logger.log('found item in files', 5)
                return self.files.__getattribute__(key)
        return self.__dict__[key]
    
    def __repr__(self):
        return '<Folder "%s" for user "%s" on Sugarsync>'%(self._displayName, self._conn._user_session.username)
    
class Folders(object):
    def __init__(self, conn, baseurl):
        q.logger.log('initializing Folders',5)
        self._conn = conn
        self._baseurl = baseurl
        self._subFolders = {}
        q.logger.log('adding "new" attribute',5)
        self.__setattr__('new', partial(self._new, self._baseurl))
        q.logger.log('getting subfolders',5)
        self.__setattr__('_children', q.clients.sugarsyncapi.getSubFolders(self._conn._auth_token, self._baseurl))
        q.logger.log('children%s' % self._children,5)

        map(lambda folderObj: self.__setattr__(cleanString(folderObj.displayName), None),
            filter(lambda attr: hasattr(attr, 'displayName'), self._children.__dict__.values()))

        self._subFolders = dict(zip(
                                    map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                        filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                            map(lambda attr: getattr(attr, 'ref'),
                                                filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values()))))
    
    
    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_subFolders').keys() and object.__getattribute__(self, name) == None:
            q.logger.log('getting attribute folder named %s for folder' % name,5)
            folderRef = object.__getattribute__(self, '_subFolders')[name]
            self.__setattr__(name, Folder(object.__getattribute__(self, '_conn'), folderRef, name))
            return object.__getattribute__(self, name)
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, name)
        
        
    def __setattr__(self, name, value):
        q.logger.log('adding attribute %s to folders' % name)
        object.__setattr__(self, name, value)
        q.logger.log('done adding attribute %s to folders' % name)
    
    
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
            
    def _new(self, parentUrl, displayName):
        q.logger.log('in _new',5)
        newfolderUrl = q.clients.sugarsyncapi.createFolder(self._conn._auth_token, parentUrl, displayName)
        self.__setattr__(cleanString(displayName), Folder(self._conn, newfolderUrl, displayName, False))
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]
        
              
class Files(object):
    def __init__(self, conn, parentUrl):
        q.logger.log('initializing files')
        self._conn = conn
        self._parentUrl = parentUrl
        self._files = {}
        self._children = q.clients.sugarsyncapi.getFolderContents(self._conn._auth_token, self._parentUrl)
        q.logger.log('children%s' % self._children)
        
        map(lambda fileObj: self.__setattr__(cleanString(fileObj.displayName), None),
            filter(lambda attr: hasattr(attr, 'mediaType'), self._children.__dict__.values()))
        
        
        self._files = dict(zip(
                                map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                    filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                        map(lambda attr: getattr(attr, 'ref'),
                                            filter(lambda child: hasattr(child, 'mediaType'), self._children.__dict__.values()))))
        
    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_files').keys() and object.__getattribute__(self, name) == None:
            q.logger.log('files %s' % name)
            q.logger.log('getting attribute file named %s for files' % name,5)
            fileRef = object.__getattribute__(self, '_files')[name]
            self.__setattr__(name, File(object.__getattribute__(self, '_conn'), fileRef, name))
            return object.__getattribute__(self, name)
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, name)

    
    def __setattr__(self, name, value):
        q.logger.log('adding attribute %s to folders' % name)
        object.__setattr__(self, name, value)
        q.logger.log('done adding attribute %s to folders' % name)
        
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
    
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
    
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]       

class File(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self._baseurl = baseurl
        self.displayName = displayName
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)

    def upload(self, localFilePath):
        q.clients.sugarsyncapi.putFileData(self._conn._auth_token, self.fileData, localFilePath)
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)

    def download(self, localFilePath):
        """
        download the selected file to a local location.
        You can enter a folder path for the file to be downloaded in or a file path to rename the file manually.
        """
        
        if self.presentOnServer:
            try:
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
            except IOError:
                localFilePath = localFilePath+'/%s'%self.displayName
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
        else:
            return False
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]
    
    def __repr__(self):
        return '<File "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)
       
class Albums(object):
    def __init__(self, conn, baseurl, displayName):
        q.logger.log('initializing albums',5)
        self._albums = {}
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        self._children = q.clients.sugarsyncapi.getAlbumsCollectionContents(self._conn._auth_token, self._baseurl)
       
        map(lambda fileObj: self.__setattr__(cleanString(fileObj.displayName), None),
             filter(lambda attr: hasattr(attr, 'displayName'), self._children.__dict__.values()))

        self._albums = dict(zip(
                                 map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                     filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                         map(lambda attr: getattr(attr, 'ref'),
                                             filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values()))))
       
        q.logger.log('albums%s' % self._albums,5)
       

    def __getattribute__(self, name):
        q.logger.log('getting attribute %s from albums' % name,5)
        if name in object.__getattribute__(self, '_albums').keys() and object.__getattribute__(self, name) == None:
            albumRef = object.__getattribute__(self, '_albums')[name]
            self.__setattr__(name, Album(object.__getattribute__(self, '_conn'), albumRef, name))
            return object.__getattribute__(self, name)
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for folder' % name)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for folder' % name)
            return object.__getattribute__(self, name)
           
           
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
           
    def __setattr__(self, name, value):
        q.logger.log('adding attribute %s to folders' % name)
        object.__setattr__(self, name, value)
        q.logger.log('done adding attribute %s to folders' % name)
       
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__getattribute__(key)
        
class Album(object):
    def __init__(self, conn, baseurl, displayName):
        q.logger.log('initializing album %s' % displayName,5)
        self._conn = conn
        self._baseurl = baseurl
        self._displayName = displayName
        self.photos = None
        
    def __getattribute__(self, name):
        if name == 'photos' and object.__getattribute__(self, 'photos') == None:
            q.logger.log('getting attribute photos for album',5)
            self.photos = Photos(object.__getattribute__(self, '_conn'), object.__getattribute__(self, '_baseurl'))
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for album' % name)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting %s folders for album' % name)
            return object.__getattribute__(self, name)
        
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
        
    def __getitem__(self, key):
        key = cleanString(key)
        q.logger.log('getting item %s'%key, 5)
        if not self.photos == None and key in self.photos._photos.keys():
            q.logger.log('found item in files', 5)
            return self.photos[key]
        else:
            self.__getattribute__('photos')
            if key in self.photos._photos.keys():
                q.logger.log('found item in photos', 5)
                return self.photos.__getattribute__(key)
        return self.__dict__[key]
    
    def __repr__(self):
        return '<Album "%s" for user "%s" on Sugarsync>'%(self._displayName, self._conn._user_session.username)

class Photos(object):
    def __init__(self, conn, parentUrl):
       self._conn = conn
       self._photos = {}
       self._parentUrl = parentUrl
       self._children = q.clients.sugarsyncapi.getAlbumContents(self._conn._auth_token, self._parentUrl)
       
       
       map(lambda photoObj: self.__setattr__(cleanString(photoObj.displayName), None),
            filter(lambda attr: hasattr(attr, 'mediaType'), self._children.__dict__.values()))

       self._photos = dict(zip(
                                map(lambda attr: cleanString(getattr(attr, 'displayName')),
                                    filter(lambda child: hasattr(child, 'displayName'), self._children.__dict__.values())),
                                        map(lambda attr: getattr(attr, 'ref'),
                                            filter(lambda child: hasattr(child, 'mediaType'), self._children.__dict__.values()))))
       
       
       
    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_photos').keys() and object.__getattribute__(self, name) == None:
            q.logger.log('photos %s' % name)
            q.logger.log('getting attribute photo named %s for photos' % name,5)
            fileRef = object.__getattribute__(self, '_photos')[name]
            self.__setattr__(name, Photo(object.__getattribute__(self, '_conn'), fileRef, name))
            return object.__getattribute__(self, name)
        elif name in object.__getattribute__(self, '__dict__'):
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, '__dict__')[name]
        else:
            q.logger.log('getting attribute %s for folder' % name,5)
            return object.__getattribute__(self, name)


    
    def __setattr__(self, name, value):
        q.logger.log('adding attribute %s to folders' % name)
        object.__setattr__(self, name, value)
        q.logger.log('done adding attribute %s to folders' % name)
       
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)
    
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]

class Photo(object):
    def __init__(self, conn, baseurl, displayName):
        self._conn = conn
        self._baseurl = baseurl
        self.displayName = displayName
        self.__dict__.update(q.clients.sugarsyncapi.getFileInfo(self._conn._auth_token, self._baseurl).__dict__)
        
    def __iter__(self):
        return SugarsyncIterator(self.__dict__)

    def download(self, localFilePath):
        """
        download the selected photo to a local location.
        You can enter a folder path for the file to be downloaded in or a file path to rename the photo manually.
        """
        if self.presentOnServer:
            try:
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
            except IOError:
                localFilePath = localFilePath+'/%s'%self.displayName
                q.clients.sugarsyncapi.retrieveFileData(self._conn._auth_token, self.fileData, localFilePath)
        else:
            return False
        
    def __getitem__(self, key):
        key = cleanString(key)
        return self.__dict__[key]
    
    def __repr__(self):
        return '<Photo "%s" for user "%s" on Sugarsync>'%(self.displayName, self._conn._user_session.username)
    
class SugarsyncIterator(object):
    def __init__(self, dict):
        self.inputDict = dict
        self.attributes = map(lambda attr: self.inputDict[attr], filter(lambda attr: attr not in ['new', 'files'], filter(lambda attr: not attr.startswith('_'), self.inputDict.keys())))
        self.index = 0

    
    def __iter__(self):
        return self
    
    
    def next(self):
        if self.index == len(self.attributes):
            raise StopIteration()
        attr = self.attributes[self.index]
        self.index += 1
        return attr
