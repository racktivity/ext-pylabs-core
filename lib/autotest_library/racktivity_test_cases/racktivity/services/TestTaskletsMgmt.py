from nose.tools import *
from pymonkey import q, i
import xmlrpclib
import oauth2 as oauth

proxy = None
class OAuthTransport(xmlrpclib.Transport):
    def get_host_info(self, host):
        import urllib
        auth, host = urllib.splituser(host)
        q.logger.log('auth='+str(auth))
        if auth:
            user = auth.split(':')[0]
            path = q.system.fs.joinPaths(q.dirs.baseDir, "var", user + '.token')
            if not q.system.fs.exists(path): return host, None, None
            token_dict = q.system.fs.readObjectFromFile(path)
            #sign the oauth request
            consumer = oauth.Consumer(user, '')
            token = oauth.Token('token_$(%s)'%token_dict['oauth_token'], token_dict['oauth_token_secret'])
            oauth_req = oauth.Request.from_consumer_and_token(consumer, token, http_method='POST', http_url="http://racktivity/xmlrpc")
            oauth_req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
            oauth_headers = oauth_req.to_header()
            q.logger.log('EXTRA HEADERS after signing : '+str(oauth_headers))
            extra_headers = list()
            if oauth_headers.has_key('Authorization'):
                extra_headers = [("Authorization", oauth_headers['Authorization'])]
        else:
            extra_headers = None
        return host, extra_headers, None


def setup():
    global proxy
    cfg = q.config.getConfig("cloudapiconnection")['main']
    proxy = xmlrpclib.ServerProxy("http://%(login)s:%(passwd)s@%(server)s:8888/xmlrpc" % cfg)
    #a dummy cloud api connection
    ca = i.config.cloudApiConnection.find('main')
    proxy._ServerProxy__transport = OAuthTransport()

def testGetDirStructures_1():
    """
    @description: [0.AA.1.1] Get Tasklets directory structures
    @id: 0.AA.1.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: getDirStructure()
    @expected_result: function should return data like {result':{'returncode':True, 'dirstructure':dict}}
    """
    global proxy
    struct = proxy.cloud_api_taskletmgmt.getDirStructures()
    assert_true('result' in struct, "Invalid file structure returned")
    result = struct['result']
    assert_true(result['returncode'], "Return code is False")

def testCreateDirectory_1():
    """
    @description: [0.AA.2.1] Create a new tasklets directory
    @id: 0.AA.2.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: createDirectory(location, dirname, executionparams)
    @expected_result: function should return data like {result':{'returncode':True,'errormessage':String}}
    """
    global proxy
    dirname = "TestCreateDirectory"
    result = proxy.cloud_api_taskletmgmt.createDirectory("events", dirname, {})
    assert_true(result['result']['returncode'], "Failed to create direcotory")
    struct = proxy.cloud_api_taskletmgmt.getDirStructures()
    eventsdir = struct['result']['dirstructure']['events']
    assert_true(dirname in eventsdir['dirs'])
    
    #delete directory.
    result = proxy.cloud_api_taskletmgmt.deleteDirectory("events/%s" % dirname, {})
    assert_true(result['result']['returncode'], "Failed to delete directory")
    
    
def testDeleteDirectory_1():
    """
    @description: [0.AA.3.1] Delete a tasklets directory
    @id: 0.AA.3.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: deleteDirectory(location, executionparams)
    @expected_result: function should return data like {result':{'returncode':True,'errormessage':String}}
    """
    global proxy
    dirname = "TestDeleteDirectory"
    result = proxy.cloud_api_taskletmgmt.createDirectory("events", dirname, {})
    assert_true(result['result']['returncode'], "Failed to create direcotory")
    
    #delete directory.
    result = proxy.cloud_api_taskletmgmt.deleteDirectory("events/%s" % dirname, {})
    assert_true(result['result']['returncode'], "Failed to delete directory")
    struct = proxy.cloud_api_taskletmgmt.getDirStructures()
    eventsdir = struct['result']['dirstructure']['events']
    assert_false(dirname in eventsdir['dirs'], "Directory didn't go away after deletion")
    
def testUpdateFile_1():
    """
    @description: [0.AA.4.1] Test saving/updating a file
    @id: 0.AA.4.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: updateFile(location, executionparams)
    @expected_result: function should return data like {result':{'returncode':True,'errormessage':String}}
    """
    global proxy
    filename = "TestUpdateFile.py"
    filecontents = "Test file contents"
    result = proxy.cloud_api_taskletmgmt.updateFile("events/%s" % filename, filecontents, {})
    assert_true(result['result']['returncode'], "Failed to create file")
    
    #compare saved with
    result = proxy.cloud_api_taskletmgmt.getFileContents("events/%s" % filename, {})
    assert_true(result['result']['returncode'], "Failed to get file contents")
    assert_equal(result['result']['filecontents'], filecontents, "Contents saved is not the same as the contents loaded")
    
    result = proxy.cloud_api_taskletmgmt.deleteFile("events/%s" % filename, {})
    assert_true(result['result']['returncode'], "Failed to delete file")

def testGetFileContents_1():
    """
    @description: [0.AA.5.1] Test loading file contents
    @id: 0.AA.5.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: getFileContents(location, executionparams)
    @expected_result: function should return data like {result':{'returncode':True, 'filecontents':String,'errormessage':String}}
    """
    global proxy
    filename = "TestGetContentsFile.py"
    filecontents = "Test file contents"
    result = proxy.cloud_api_taskletmgmt.updateFile("events/%s" % filename, filecontents, {})
    assert_true(result['result']['returncode'], "Failed to create file")
    
    #compare saved with
    result = proxy.cloud_api_taskletmgmt.getFileContents("events/%s" % filename, {})
    assert_true(result['result']['returncode'], "Failed to get file contents")
    assert_equal(result['result']['filecontents'], filecontents, "Contents saved is not the same as the contents loaded")
    
    result = proxy.cloud_api_taskletmgmt.deleteFile("events/%s" % filename, {})
    assert_true(result['result']['returncode'], "Failed to delete file")

def testDeleteFile_1():
    """
    @description: [0.AA.6.1] Test deleting file
    @id: 0.AA.6.1
    @timestamp: 1298457130
    @signature: mazmy
    @params: deleteFile(location, executionparams)
    @expected_result: function should return data like {result':{'returncode':True,'errormessage':String}}
    """
    global proxy
    filename = "TestDeleteFile.py"
    filecontents = "Test file contents"
    result = proxy.cloud_api_taskletmgmt.updateFile("events/%s" % filename, filecontents, {})
    assert_true(result['result']['returncode'], "Failed to create file")
    
    result = proxy.cloud_api_taskletmgmt.deleteFile("events/%s" % filename, {})
    assert_true(result['result']['returncode'], "Failed to delete file")
    
    struct = proxy.cloud_api_taskletmgmt.getDirStructures()
    eventsdir = struct['result']['dirstructure']['events']
    assert_false(filename in eventsdir['files'], "File didn't go away after deletion")