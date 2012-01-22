import json
from pylabs import q
from pylabs.baseclasses import BaseEnumeration
import urllib

class BitbucketRESTCall(BaseEnumeration):
    """
    Enumerator of all supported Bitbucket REST calls
    """

    def __init__(self, value=None):
        self.value = value

    @classmethod
    def _initItems(cls):
        cls.registerItem('groups')
        cls.registerItem('group_privileges', value='group-privileges')
        cls.registerItem('users')
        cls.registerItem('repositories')
        cls.registerItem('user')
        cls.finishItemRegistration()

class BitbucketSettingsParam(BaseEnumeration):
    """
    Enumerator of all supported Bitbucket permissions
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('name')
        cls.registerItem('permission')
        cls.registerItem('auto_add')
        cls.finishItemRegistration()

class BitbucketPermission(BaseEnumeration):
    """
    Enumerator of all supported Bitbucket permissions
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('read')
        cls.registerItem('write')
        cls.registerItem('admin')
        cls.finishItemRegistration()

class Bitbucket:
    """
    Bitbucket client enables administrators and developers leveraging Bitbucket services through PyLabs

    @property accounts = account on bitbucket e.g. despieg, value is array of mercurial repo's
    """

    def __init__(self):
        self._accountnames= list()
        self._initialized = False
        self.accountsLocalRepoNames = dict()
        self.accountsRemoteRepoNames = dict()
        self.apiVersion = '1.0'
        self.apiURI = 'https://api.bitbucket.org'
        self.resultFormat = q.enumerators.RESTResultFormat.JSON
        self.codedir = q.system.fs.joinPaths(q.dirs.baseDir, ".." , "code")
        q.system.fs.createDir(self.codedir)

    def init(self,force=False):
        if force or not self._initialized:
            self._getAccountNames()
            for account in self._accountnames:
                repos=self._getRepoNamesFromCodeDir(account)
                self.accountsLocalRepoNames[account]=repos


    def _getRepoNamesFromCodeDir(self, account):
        accounts = self._getAccountNames()
        if account in accounts:
            bitbucket_connection = BitbucketConnection(account)
            return bitbucket_connection._getRepoNamesFromCodeDir()
        else:
            raise RuntimeError('Account "%s" does not exist'%account)

    def _getAccountNames(self):
        names = q.clients.bitbucket._config.list()
        self._accountnames = names
        return names

    def accountAdd(self,account="",login="",passwd=""):
        """
        All params need to be filled in, when 1 not filled in will ask all of them
        """
        if account<>"" and login<>"" and passwd<>"":
            try:
                self._config.remove(account)
            except:
                pass
            self._config.add(account, {"login": login, "passwd": passwd})
        else:
            self._config.add()
        # TODO - MNour: Uncomment when _syncBitbucketConfigToMercurialConfig is done.
        # self._syncBitbucketConfigToMercurialConfig()

    def accountsReview(self):
        self._config.review()
        # TODO - MNour: Uncomment when _syncBitbucketConfigToMercurialConfig is done.
        # self._syncBitbucketConfigToMercurialConfig()
        
    def accountsShow(self):
        self._config.show()

    def accountsRemove(self,accountName=""):
        self._config.remove(accountName)
        # TODO - MNour: Uncomment when _syncBitbucketConfigToMercurialConfig is done.
        # self._syncBitbucketConfigToMercurialConfig()

    def accountGetConfig(self,accountName=""):
        return self._config.getConfig(accountName)
        
    def accountGetLoginInfo(self,accountName=""):
        """
        """
        self.init()
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select Bitbucket account name",self._getAccountNames())
        config=self.accountGetConfig(accountName)
        login=config["login"]
        passwd=config["passwd"]
        if login=="" or passwd=="":
            self.accountsReview(accountName)
        url=" https://%s:%s@bitbucket.org/%s/" % (login,passwd,accountName)
        return url,login,passwd

##    def _syncBitbucketConfigToMercurialConfig(self):
##        mercurialconnections=q.clients.mercurial.config.list()
##        for mercurialconnection in mercurialconnections:
##            if mercurialconnection.find("bitbucket_")==0:
##                q.clients.mercurial.config.remove(mercurialconnection.replace("bitbucket_",""))
##        for account in self._getAccountNames():
##            login=self.accountGetConfig(account)["login"]
##            passwd=self.accountGetConfig(account)["passwd"]
##            url = "http://bitbucket.org/%s/" % account
##            q.clients.mercurial.config.add("bitbucket_%s"%account,{"url":url,"login":login,"passwd":passwd})
##            #print "bitbucket_%s"%account

    def getConnection(self, accountName = '', accountLogin = '', accountPasswd = ''):
        if q.qshellconfig.interactive:
            if not accountName:
                accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
            
            accounts = self._getAccountNames()
            if not accountName in accounts:
                if not accountLogin:
                    accountLogin = q.gui.dialog.askString("Please enter account Login:")
                if not accountPasswd:
                    accountPasswd = q.gui.dialog.askPassword("Please enter account Password", True)
                
                self.accountAdd(accountName, accountLogin, accountPasswd)
            
            bitbucket_connection = BitbucketConnection(accountName)

            return bitbucket_connection




class BitbucketConnection(object):
    
    def __init__(self, accountName):
        self.accountName = accountName
        self.codedir = q.system.fs.joinPaths(q.dirs.baseDir, ".." , "code")
        self.bitbucket_client = q.clients.bitbucket
        self.accountPathLocal = q.system.fs.joinPaths(self.codedir,"bitbucket_%s"%accountName)
    
    def addGroup(self, groupName):
        """
        Add Bitbucket new group

        @param groupName:       Bitbucket new group name
        @type groupName:        string
        @return The newly created Bitbucket L{Group}
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, q.enumerators.RESTMethod.POST, uriParts=[self.accountName], data={'name': groupName})

#    def _getAccountPathLocal(self,accountName):
#        return q.system.fs.joinPaths(self.codedir,"bitbucket_%s"%accountName)

    def getRepoPathLocal(self,repoName="",die=True):      
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo",self._getRepoNamesFromCodeDir())
            if repoName==None:
                if die:
                    raise RuntimeError("Cannot find repo for accountName %s" % self.accountName)
                else:
                    return ""
        path=q.system.fs.joinPaths(self.accountPathLocal,repoName)
        q.system.fs.createDir(path)
        return path


    def _getRepoNamesFromCodeDir(self):#,accountName=""):
        if q.system.fs.exists(self.accountPathLocal):#path):
            return q.system.fs.listDirsInDir(self.accountPathLocal,False,True)
        else:
            return []

    def getRepoPathRemote(self,repoName=""):
        url,login,passwd=self.bitbucket_client.accountGetLoginInfo(self.accountName)
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo from bitbucket",self.getRepoNamesFromBitbucket())
        return "%s%s" % (url,repoName)

    def _callBitbucketRestAPI(self, call, method=q.enumerators.RESTMethod.GET, uriParts=None, params=None, data=None):
        """
        Make a call to one of the Bitbucket REST API(s)

        @param call:            Bitbucket REST call to make
        @type call:             L{BitbucketRESTCall}
        @param method:          REST method used to initiate the call
        @type method:           L{q.enumerators.RESTMethod}
        @param uriParts:        Addtional parts to be added to the URI
        @type uriParts:         list
        @param params:          Optional params to be sent URL encoded in the REST request URI
        @type params:           dict
        @param data:            Optional data to be sent through the call
        @type data:             list or dict
        @return A deserialized result from JSON to its Python represemtation
        @raise Exception in case of errors
        """
        # TODO - MNour: Think about a generic REST client that can be configured and used from different components.
        # url, login, passwd = self.accountGetLoginInfo(accountName)
        #http=q.clients.http.getconnection()
        #http.addAuthentication(login,passwd)
        #url="https://api.bitbucket.org/1.0/users/%s/" % self._getBitbucketUsernameFromUrl(url)
        #content=http.get(url)
        accountConfig = self.bitbucket_client.accountGetConfig(self.accountName)
        uriPartsString = '%s/' %'/'.join(uriParts) if uriParts else ''
        parameters = params if params else dict()
        parameters['format'] = self.bitbucket_client.resultFormat

        dataString = ''
        if data:
            if type(data) is list:
                dataString = ','.join(data)
            elif type(data) is dict:
                dataString = urllib.urlencode(data)
            else:
                q.errorconditionhandler.raiseError("Invalid data type '%s', data value is '%s'." %(type(data), data))

        import urllib2
        auth = urllib2.base64.standard_b64encode("%s:%s" % (accountConfig['login'], accountConfig['passwd']))
        headers = {'Authorization': 'Basic %s' % auth }
        url = "%(apiURI)s/%(apiVersion)s/%(call)s/%(uriParts)s?%(parameters)s" % {
                      'call': call, 
                      'apiURI': self.bitbucket_client.apiURI,
                      'apiVersion': self.bitbucket_client.apiVersion, 
                      'uriParts': uriPartsString, 
                      'parameters': urllib.urlencode(parameters)}
        req = urllib2.Request(url, headers=headers, data=dataString)
        req.get_method = lambda : str(method)
        content = urllib2.urlopen(req).read()

        try:
            object = json.loads(content) if content else dict()
        except:
            q.errorconditionhandler.raiseError("Cannot call rest api of bitbucket, call was %s" %url)

        # TODO - MNour: Do we need to construct Bitbucket resources classes out of json deserialized object ?
        return object

    def _getBitbucketRepoInfo(self):
        return self._callBitbucketRestAPI(BitbucketRESTCall.USERS, uriParts=[self.accountName])

    def findRepoFromBitbucket(self,partofName=None,reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        names=self.getRepoNamesFromBitbucket(partofName,reload)
        if partofName==None:
            q.gui.dialog.message("Select bitbucket repository")
            reposFound2=q.gui.dialog.askChoice("",names)
        else:
            reposFound2=[]
            for repo in names:
                if repo.find(partofName)<>-1:
                    reposFound2.append(repo)
        if len(reposFound2)>1:
            raise RuntimeError("Found more than 1 choice, please use better search criteria")
        return reposFound2
    
    def getRepoNamesFromBitbucket(self,partOfRepoName="",reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        if self.bitbucket_client.accountsRemoteRepoNames.has_key(self.accountName) and reload==False:
            return self.bitbucket_client.accountsRemoteRepoNames[self.accountName]
        repos=self._getBitbucketRepoInfo()
        repoNames=[str(repo["slug"]) for repo in repos["repositories"]] 
        if partOfRepoName<>"":
            if partOfRepoName.find("*")<>-1:
                partOfRepoName=partOfRepoName.replace("*","").replace("?","").lower()
                repoNames2=[]
                for name in repoNames:
                    name2=name.lower()
                    if name2.find(partOfRepoName)<>-1:
                        repoNames2.append(name)
            else:
                partOfRepoName=partOfRepoName.replace("*","").replace("?","").lower()
                repoNames2=[]
                for name in repoNames:
                    name2=name.lower()
                    if name2==partOfRepoName:
                        repoNames2.append(name)
            
                #print name2 + " " + partOfRepoName + " " + str(name2.find(partOfRepoName))
            repoNames=repoNames2
        
        return repoNames

    def checkoutRepo(self,repoName="",branch="",forceUpdate=None):
        """
        @param branch when "" defaults to "default", when None will be asked
        """
        self.bitbucket_client.init()
        if repoName=="":
            repoName=q.gui.dialog.askString("Reponame (wildcards are allowed e.g. kds_*)","*")
        #if repoName.find("*")<>-1:
        #    #wildcard
        #    repoName=reponame.replace("*","")
        # else:

        names=self.getRepoNamesFromBitbucket(repoName)

        if len(names)==1:
            if repoName=="":
                repoName=q.gui.dialog.askString("Reponame found = (press enter if yes or change)",names[0])
            repoName=names[0]
        if len(names)==0:
            repoName=q.gui.dialog.askString("Could not find matching name on repo please specify")
        if len(names)>1:
            repoName=q.gui.dialog.askChoice("select repoName",names,pageSize=300, sortChoices=True)

        if branch==None:
            branch=q.gui.dialog.askString("Branchname","default")      
        if branch=="":
            branch="default"
        if forceUpdate==None:
            forceUpdate=q.gui.dialog.askYesNo("Do you want to force an update (if not will try to merge)")  
        
        url,login,passwd = self.bitbucket_client.accountGetLoginInfo(self.accountName)
        if url[-1]<>"/":
            url=url+"/"
        return q.clients.mercurial.getclient("/opt/code/%s/%s/" % (self.accountName,repoName) ,"%s%s" % (url,repoName),branch)

    def getGroups(self):
        """
        Retrieve all Bitbucket groups for the given account.

        @return List of Bitbucket groups
        @rtype list
        @raise Exception in case of errors
        """
        # TODO - MNour: Objectization of returned values.
        self._validateValues(accountName=self.accountName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, uriParts=[self.accountName])

    def getGroup(self, groupName):
        """
        Retrieve a Bitbucket group that has the same exact specified group name

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @return Bitbucket L{Group}
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        groups = [group for group in self.getGroups() if group['name'] == groupName]#self.getGroups(self.accountName)
        if not groups:
            q.errorconditionhandler.raiseError('No group found with name [%s].' %groupName)

        return groups[0] if len(groups) == 1 else q.errorconditionhandler.raiseError('Found more than group with name [%s].' %groupName)

    # TODO - MNour: Implement this method
    def findGroup(self, regex):
        """
        Find Bitbucket group which matches the specified regular expression

        @param regex:       Regular expression using using which to match group names
        @type regex:        string
        @return List of Bitbucket L{Groups}
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(accountName=self.accountName)
        q.errorconditionhandler.raiseError('Method not yet implemented.')



    def getRepos(self):
        """
        Retrieve all Bitbucket repositories which can be access by the account specified

        @return List of Bitbucket L{Repository}(s), or empty list of not repositories accessed by the specified account
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(accountName=self.accountName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.USER, uriParts=[str(BitbucketRESTCall.REPOSITORIES)])

    def checkRepo(self, repoName):
        """
        Check for the existence of a Bitbucket repository

        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @return True if the Bitbucket repository exists, False otherwise
        @rtype Boolean
        @raise Exception in case of error
        """
        self._validateValues(repoName=repoName, accountName=self.accountName)
        return len([repo for repo in self.getRepos() if repo['name'] == repoName]) > 0

    def checkGroup(self, groupName):
        """
        Check whether group exists or not

        @param groupName:       Bitbucket group to lookup if exists
        @type groupName:        string
        @return True if group exists, False otherwise
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        return len([group for group in self.getGroups() if group['name'] == groupName]) > 0

    def deleteGroup(self, groupName):
        """
        Delete the specified Bitbucket group

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, q.enumerators.RESTMethod.DELETE, uriParts=[self.accountName, groupSlug])

    def getGroupMembers(self, groupName):
        """
        Retrieve Bitbucket group members

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @return Bitbucket group members, empty if no members exist
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        return [member['username'] for member in self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, uriParts=[self.accountName, groupSlug, 'members'])]

    def addGroupMember(self, memberLogin, groupName):
        """
        Add a new member to a Bitbucket group

        @param memberLogin:     Bitbucket member login
        @type memberLogin:      string
        @param groupName:       Bitbucket group name
        @type groupName:        string
        @return The L{Member} if it has been added successfully
        @rtype L{Member}
        @raise Exception in case of errors
        """
        self._validateValues(memberLogin=memberLogin, groupName=groupName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, q.enumerators.RESTMethod.PUT, uriParts=[self.accountName, groupSlug, 'members', memberLogin])

    def updateGroup(self, groupName, **kwargs):
        """
        Update Bitbucket group settings

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param kwargs:          Bitbucket group setteings required to be updated\
        @type kwargs:           dict
        @return The L{Group} after update if update has been done successfully
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        group = self.getGroup(groupName)
        if kwargs:
            if not str(BitbucketSettingsParam.NAME) in kwargs:
                kwargs[str(BitbucketSettingsParam.NAME)] = group[str(BitbucketSettingsParam.NAME)]

            if not BitbucketSettingsParam.PERMISSION in kwargs:
                kwargs[str(BitbucketSettingsParam.PERMISSION)] = group[str(BitbucketSettingsParam.PERMISSION)]

        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, q.enumerators.RESTMethod.PUT, [group['slug']], **kwargs)

    def deleteGroupMember(self, memberLogin, groupName):
        """
        Delete a member from a Bitbucket group

        @param memberLogin:     Bitbucket member login
        @type memberLogin:      string
        @param groupName:       Bitbucket group name
        @type groupName:        string
        @raise Exception in case of errors
        """
        self._validateValues(memberLogin=memberLogin, groupName=groupName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        self._callBitbucketRestAPI(BitbucketRESTCall.GROUPS, q.enumerators.RESTMethod.DELETE, uriParts=[self.accountName, groupSlug, 'members', memberLogin])

    def getGroupPrivileges(self, filter=None, private=None):
        """
        Retrieve all group privileges specified by that Bitbucket account

        @param filter:          Filtering the permissions of privileges we are looking for
        @type filter:           L{BitbucketPermission}
        @param private:         Defines whether to retrieve privileges defined on private repositories or not
        @type private:          boolean
        @return All L{Privilege}s specified by that Bitbucket account name
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(accountName=self.accountName)
        params = dict()
        if filter:
            params['filter'] = filter

        if private != None:
            params['private'] = private

        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUP_PRIVILEGES.value, uriParts=[self.accountName], params=params)

    def getRepoGroupPrivileges(self, repoName):
        """
        Retrieve all group privileges specified by that Bitbucket account on that Bitbucket repository

        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @return All L{Privilege}s specified by that Bitbucket account name on that Bitbucket repository
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(repoName=repoName, accountName=self.accountName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUP_PRIVILEGES.value, uriParts=[self.accountName, repoName])

    def grantGroupPrivileges(self, groupName, repoName, privilege):
        """
        Grant a group privilege to the specified Bitbucket repository

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository
        @type repoName:         string
        @param privilege:       Group privilege
        @type privilege:        L{BitbucketPermission}
        @return List L{Privilege}s granted to the specified repository
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, repoName=repoName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        return self._callBitbucketRestAPI(BitbucketRESTCall.GROUP_PRIVILEGES.value, q.enumerators.RESTMethod.PUT,
                                          uriParts=[self.accountName, repoName, self.accountName, groupSlug], data=[str(privilege)])

    def revokeRepoGroupPrivileges(self, groupName, repoName):
        """
        Revoke group privileges on the defined Bitbucket repository

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, repoName=repoName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        self._callBitbucketRestAPI(BitbucketRESTCall.GROUP_PRIVILEGES.value, q.enumerators.RESTMethod.DELETE,
                                   uriParts=[self.accountName, repoName, self.accountName, groupSlug])

    def revokeGroupPrivileges(self, groupName):
        """
        Revoke all group privileges

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        groupSlug = self._getGroupSlug(groupName)
        self._callBitbucketRestAPI(BitbucketRESTCall.GROUP_PRIVILEGES.value, q.enumerators.RESTMethod.DELETE,
                                   uriParts=[self.accountName, self.accountName, groupSlug])

    def _getGroupSlug(self, groupName):
        """
        Retriev Bitbucket group slug name

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @return Bitbucket group slug name or Exception in case of errors
        @rtype string
        """
        self._validateValues(groupName=groupName, accountName=self.accountName)
        group = self.getGroup(groupName)
        return group['slug']

    def _validateValues(self, **kwargs):
        """
        Validate values that they are not neither None nor empty valued

        @param kwargs:          Values to be validated
        @type kwargs:           dict
        @raise Exception in case one or more values do not satisfy the conditions specified above
        """
        invalidValues = dict()
        for key in kwargs:
            if not kwargs[key]:
                invalidValues[key] = kwargs[key]

        if invalidValues:
            q.errorconditionhandler.raiseError('Invalid values: %s' %invalidValues)


