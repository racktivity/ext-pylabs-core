#Import the q object in this module
from pylabs import q , i 
from dropbox.helpers import login_and_authorize
from pylabs.config import ConfigManagementItem, ItemSingleClass, ItemGroupClass
from dropbox import client, rest, auth
from oauth import oauth
import shutil


#The next lines only needed when implementing wrappers for servers
#from pymonkey.cmdb import CMDB
#from Server import Server
#from ServerStatus import ServerStatus
 



class DropboxFactory ():
    """
      this is a factory class to create instance of drpbox client 
     this method returns instance of dropboxManager which could be used to access different methods dropbox API. this method may take user name and password of dropbox user or may take token object. method return DropboxClient .it is important to consider the following while using this extension 
        
                -user must configure file  /opt/qbase3/cfg/qconfig/dropbox.cfg 
                -user of this extention  has to be aware  of dropbox terms of use in order to be able to obtain production key  
    
    
    """
   # OAuthToken
    
    
    def getClient(self, userName):
        """ this method returns instance of dropboxManager which could be used to access different methods dropbox API.
         this method may takes user name , user name must be predefined using q.clinets.dropbox._config 
         it is important to consider the following while using this extension 
        
                -user must configure file  /opt/qbase3/cfg/qconfig/dropbox.cfg  
                -user of this extention  has to be aware  of dropbox terms of use in order to be able to obtain production key  

        @param userName: dropbox user name 
       
        @return:  return DropboxClient instance with permission to access dropbox account of the user generated that client.  
        """
        q.logger.log('initializing drop box client ' )
       
        config = q.config.getConfig('dropbox')
        if not config:
            q.errorconditionhandler.raiseError("dropbox.cfg does not exists  ")
        if 'auth' not in config:
            q.errorconditionhandler.raiseError("dropbox.cfg does not include auth section  ")
        config = config['auth']
        
        dba = auth.Authenticator(config)
                
        q.logger.log('initializing drop box client using access token ' )
        try:
            userConfig=i.config.clients.dropbox.getConfig(userName)
        except:
            q.errorconditionhandler.raiseError(userName +" is not configured user name  ")
        
        access_token = oauth.OAuthToken(userConfig['key'], userConfig['secret'])
        
        dbClient = client.DropboxClient(config['server'], config['content_server'], config['port'], dba, access_token)
         
        return DropboxClient(dbClient, config)

     
class DropboxClient ():
    
    def __init__(self, client  , config):
        self._client = client
        self.token = client.token
        self._config = config
        self._root = config["root"]
        
    def getAccountInfo(self):
        """
        Retrieve information about the user's account.
        """
        response= self._client.account_info()
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    
      
    
    
    
    def putFile(self , to_path, file):
        """
        upload file contents
         The filename is taken from the file_obj name currently, so you can't
        have the local file named differently than it's target name.  This may
        change in future versions.

        Finally, this function is not terribly efficient due to Python's
        HTTPConnection requiring all of the file be read into ram for the POST.
        Future versions will avoid this problem.
        
        @param param to_path:  is the `directory` path to put the file (NOT the full path).
        @param param uploadedFile: is an open and ready to read file object that will be uploaded OR the path of file to be uploaded 
        """
        if isinstance(file, str):
            uploadedFile=open(file)
        else:
            uploadedFile=file
      
        response= self._client.put_file(self._root , to_path , uploadedFile)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    
    def getFile(self,  from_path ):
        """
        Retrieves a file from the given root ("dropbox" or "sandbox") based on
        from_path as the `full path` to the file.  
        
        Unlike the other calls, this
        one returns a raw HTTPResponse with the connection open.  You should 
        do your read and any processing you need and then close it.
          
        @param from_path : the path of drop box 
        @return: return HTTPResponse Object . use resp.read() to get your stream 
            
        """
        
        response = self._client.get_file(self._root ,  from_path)
        if response.status ==400 or response.status ==404:
            raise  q.errorconditionhandler.raiseError(eval(response.read()))
        return  response
  
         
        
    def getFileToLocalPath(self,  from_path , download_path):
        """
        Retrieves a file from the given root ("dropbox" or "sandbox") based on
        from_path as the `full path` to the file.  
        
        @param from_path : the path of drop box 
        @param download_path: the local path to which file to be download
       
        """
        response =self._client.get_file(self._root ,  from_path )
        if response.status ==400 or response.status ==404:
            raise  q.errorconditionhandler.raiseError(eval(response.read()))
        downloadedFile = open(download_path, "w")
        shutil.copyfileobj(response, downloadedFile)
        downloadedFile.close()
        response.close()
        
    def copyFile(self, from_path, to_path):
        """
        Copy a file or folder to a new location in dropbox.

        @param from_path: Required. from_path specifies either a file or folder to be copied to the location specified by to_path. This path is interpreted relative to the location specified by root.
        @param to_path: Required. to_path specifies the destination path including the new name for file or folder. This path is interpreted relative to the location specified by root.
        """
      
        
        response= self._client.file_copy(self._root , from_path, to_path)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    def createFolder(self, path):
        """
        Create a folder relative to the user's Dropbox root 
        """
        
        response= self._client.file_create_folder(self._root , path)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    def deleteFile(self,  path):
        """
        Delete a file or folder.
        """
          
        response= self._client.file_delete(self._root , path)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    def moveFile(self, from_path, to_path):
        """
        Move a file or folder to a new location.
        @param from_path: Required. from_path specifies either a file or folder to be copied to the location specified by to_path. This path is interpreted relative to the location specified by root.
        @param to_path. Required. to_path specifies the destination path including the new name for file or folder. This path is interpreted relative to the location specified by root.
        """
          
        response= self._client.file_move(self._root , from_path, to_path)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data
    def metadata(self,  path, file_limit=10000, hash=None, list=True, status_in_response=False, callback=None):
        """
        The metadata API location provides the ability to retrieve file and
        folder metadata and manipulate the directory structure by moving or
        deleting files and folders.

        @param  callback. Optional. The server will wrap its response of format inside a call to the argument specified by callback. Value must contains only alphanumeric characters and underscores.
        @param  file_limit. Optional. Default is 10000. When listing a directory, the service will not report listings containing more than file_limit files and will instead respond with a 406 (Not Acceptable) status response.
        @param   Optional. Listing return values include a hash representing the state of the directory's contents. If you provide this argument to the metadata call, you give the service an opportunity to respond with a "304 Not Modified" status code instead of a full (potentially very large) directory listing. This argument is ignored if the specified path is associated with a file or if list=false.
        @param   Optional. The strings true and false are valid values. true is the default. If true, this call returns a list of metadata representations for the contents of the directory. If false, this call returns the metadata for the directory itself.
        @param   status_in_response. Optional. Some clients (e.g., Flash) cannot handle HTTP status codes well. If this parameter is set to true, the service will always return a 200 status and report the relevant status code via additional information in the response body. Default is false.
        """ 
        
          
        response= self._client.metadata(self._root ,path, file_limit, hash, list, status_in_response, callback)
        if "error" in response.data:
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.data

    def createAccount(self, email='', password='', first_name='', last_name='' ):
        """
        creates new account
        @param email: email of the new user 
        @param password: plain text password of new user 
        @param firstName: first Name of new user 
        @param last_name: last name of new user 
        
         
        """
          
        response= self._client.account(email, password, first_name, last_name)
        if response.status == 400 :
            raise  q.errorconditionhandler.raiseError(response.data['error'])
        return  response.body
    def thumbnail(self,  from_path, download_path):
        """
        return thumbnail for image file 
        @param from_path: image path on dropbox
        @param download_path: localPath to download the image  
        """
        
        response =self._client.thumbnail(self._root,   from_path )
        if response.status ==400 or response.status ==404:
            raise  q.errorconditionhandler.raiseError(eval(response.read()))
        downloadedFile = open(download_path, "w")
        shutil.copyfileobj(response, downloadedFile)
        downloadedFile.close()
        response.close()
        
        
        
   
