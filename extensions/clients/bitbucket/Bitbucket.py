import json
from pylabs import q
from pylabs.baseclasses import BaseEnumeration
from pylabs.Shell import *
import urllib

class RESTResultFormat(BaseEnumeration):
    """
    Enumerator of all supported Bitbucket REST result formats
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('json')
        cls.registerItem('yaml')
        cls.finishItemRegistration()

class RESTMethod(BaseEnumeration):
    """
    Enumerator of all supported REST methods
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('POST')
        cls.registerItem('GET')
        cls.registerItem('PUT')
        cls.registerItem('DELETE')
        cls.finishItemRegistration()

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
    @property accounts = account on bitbucket e.g. despieg, value is array of mercurial repo's
    """

    def __init__(self):
        self._accountnames= list()
        self._initialized = False
        self.accountsLocalRepoNames = dict()
        self.accountsRemoteRepoNames = dict()
        self.apiVersion = '1.0'
        self.apiURI = 'https://api.bitbucket.org'
        self.resultFormat = RESTResultFormat.JSON
        self.codedir = q.system.fs.joinPaths(q.dirs.baseDir, ".." , "code")
        q.system.fs.createDir(self.codedir)

    def init(self,force=False):
        if force or not self._initialized:
            self._getAccountNames()
            for account in self._accountnames:
                repos=self._getRepoNamesFromCodeDir(account)
                self.accountsLocalRepoNames[account]=repos

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
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())      
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
##

    def _getAccountPathLocal(self,accountName):
        return q.system.fs.joinPaths(self.codedir,"bitbucket_%s"%accountName) 

    def getRepoPathLocal(self,accountName="",repoName="",die=True):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())        
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo",self._getRepoNamesFromCodeDir(accountName))                
            if repoName==None:
                if die:
                    raise RuntimeError("Cannot find repo for accountName %s" % accountName)
                else:
                    return ""
        path=q.system.fs.joinPaths(self._getAccountPathLocal(accountName),repoName)
        q.system.fs.createDir(path)
        return path 

    def _getRepoNamesFromCodeDir(self,accountName=""):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        path=self._getAccountPathLocal(accountName)
        if q.system.fs.exists(path):
            return q.system.fs.listDirsInDir(path,False,True)
        else:
            return []

    def getRepoPathRemote(self,accountName="",repoName=""):
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        url,login,passwd=self.accountGetLoginInfo(accountName)
        if repoName=="":
            repoName=q.gui.dialog.askChoice("Select repo from bitbucket",self.getRepoNamesFromBitbucket(accountName))
        return "%s%s" % (url,repoName)

    def _callBitbucketRestAPI(self, accountName, call, method=RESTMethod.GET, uriParts=None, params=None, data=None):
        """
        Make a call to one of the Bitbucket REST API(s)

        @param accountName:     Bitbucket account name
        @type accountName:      string
        @param call:            Bitbucket REST call to make
        @type call:             L{BitbucketRESTCall}
        @param method:          REST method used to initiate the call
        @type method:           L{RESTMethod}
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
        # TODO - KDS: Need a better way than curl, the authentication doesnt seem to work when using the http pylabs extension.
        q.platform.ubuntu.checkInstall("curl","curl")
        resultTmpfile = q.system.fs.joinPaths(q.dirs.tmpDir, q.base.idgenerator.generateGUID())
        headerTmpfile = q.system.fs.joinPaths(q.dirs.tmpDir, q.base.idgenerator.generateGUID())
        accountConfig = self.accountGetConfig(accountName)
        uriPartsString = '%s/' %'/'.join(uriParts) if uriParts else ''
        parameters = params if params else dict()
        parameters['format'] = self.resultFormat

        dataString = ''
        if data:
            if type(data) is list:
                dataString = ','.join(data)
            elif type(data) is dict:
                dataString = urllib.urlencode(data)
            else:
                q.errorconditionhandler.raiseError("Invalid data type '%s', data value is '%s'." %(type(data), data))

        cmd = "curl --dump-header %(headerTmpfile)s --user %(login)s:%(password)s --request %(method)s '%(apiURI)s/%(apiVersion)s/%(call)s/%(accountName)s/%(uriParts)s?%(parameters)s' --data '%(data)s' > %(resultTmpfile)s" %{'headerTmpfile': headerTmpfile,
              'login': accountConfig['login'], 'password': accountConfig['passwd'], 'call': call, 'resultTmpfile': resultTmpfile, 'apiURI': self.apiURI, 'apiVersion': self.apiVersion,
              'accountName': accountConfig['login'], 'method': method, 'data': dataString, 'uriParts': uriPartsString, 'parameters': urllib.urlencode(parameters)}

        resultcode, content = q.system.process.execute(cmd, False, True)
        if resultcode > 0:
            q.errorconditionhandler.raiseError("Cannot get reponames from repo. Cannot execute %s" %cmd)

        # TODO - MNour: Add error checking and handling.
        content = q.system.fs.fileGetContents(resultTmpfile )
        q.system.fs.removeFile(resultTmpfile)
        q.system.fs.removeFile(headerTmpfile)

        try:
            object = json.loads(content) if content else dict()
        except:
            q.errorconditionhandler.raiseError("Cannot call rest api of bitbicket, call was %s" %cmd)

        # TODO - MNour: Do we need to construct Bitbucket resources classes out of json deserialized object ?
        return object

    def _getBitbucketRepoInfo(self, accountName):
        if accountName=="":
            raise RuntimeError("Cannot get repo info when account name not specified. Please call this function with accountName")

        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.USERS)

    def findRepoFromBitbucket(self,accountName="",partofName=None,reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        names=self.getRepoNamesFromBitbucket(accountName,partofName,reload)
        if partofName==None:
            q.gui.dialog.message("Select bitbucket repository")
            reposFound2=q.gui.dialog.askChoice("",names)                    
        else:
            reposFound2=[]
            for repo in repoNames:
                if repo.find(partofName)<>-1:
                    reposFound2.append(repo)
        if len(reposFound2)>1:
            raise RuntimeError("Found more than 1 choice, please use better search criteria")
        return reposFound2
    
    def getRepoNamesFromBitbucket(self,accountName="",partOfRepoName="",reload=False):
        """
        will use bbitbucket api to retrieven all repo information
        @param reload means reload from bitbucket   
        """
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        if self.accountsRemoteRepoNames.has_key(accountName) and reload==False:
            return self.accountsRemoteRepoNames[accountName]
        repos=self._getBitbucketRepoInfo(accountName)
        #ipshell()
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

    def checkoutRepo(self,accountName="",repoName="",branch="",forceUpdate=None):
        """
        @param branch when "" defaults to "default", when None will be asked
        """
        self.init()
        if accountName=="":
            accountName=q.gui.dialog.askChoice("Select bitbucket accountName",self._getAccountNames())
        if repoName=="":
            repoName=q.gui.dialog.askString("Reponame (wildcards are allowed e.g. kds_*)","*")
        #if repoName.find("*")<>-1:
        #    #wildcard
        #    repoName=reponame.replace("*","")
        # else:

        names=self.getRepoNamesFromBitbucket(accountName,repoName)

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
        
        url,login,passwd=self.accountGetLoginInfo(accountName)
        if url[-1]<>"/":
            url=url+"/"
        return q.clients.mercurial.getclient("/opt/code/%s/%s/" % (accountName,repoName) ,"%s%s" % (url,repoName),branch)

#########################################################################################################################
#    bitbucket REST
#########################################################################################################################

#    def accountGetRepos(self, accountName):
#        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.USERS)

    def getGroups(self, accountName):
        """
        Retrieve all Bitbucket groups for the given account.

        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return List of Bitbucket groups
        @rtype list
        @raise Exception in case of errors
        """
        # TODO - MNour: Objectization of returned values.
        self._validateValues(accountName=accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS)

    def getGroup(self, groupName, accountName):
        """
        Retrieve a Bitbucket group that has the same exact specified group name

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return Bitbucket L{Group}
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=accountName)
        groups = [group for group in self.getGroups(accountName) if group['name'] == groupName]
        if not groups:
            q.errorconditionhandler.raiseError('No group found with name [%s].' %groupName)

        return groups[0] if len(groups) == 1 else q.errorconditionhandler.raiseError('Found more than group with name [%s].' %groupName)

    # TODO - MNour: Implement this method
    def findGroup(self, regex, accountName):
        """
        Find Bitbucket group which matches the specified regular expression

        @param regex:       Regular expression using using which to match group names
        @type regex:        string
        @param accountName: Bitbucket account name
        @type accountName:  string
        @return List of Bitbucket L{Groups}
        @rtype list
        @raise Exception in case of errors
        """
        self._validateAccountName(accountName)
        q.errorconditionhandler.raiseError('Method not yet implemented.')

    def addGroup(self, groupName, accountName):
        """
        Add Bitbucket new group

        @param groupName:       Bitbucket new group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return The newly created Bitbucket L{Group}
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateGroupAndAccountNames(groupName, accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, RESTMethod.POST, name=groupName)

    def checkGroup(self, groupName, accountName):
        """
        Check whether group exists or not

        @param groupName:       Bitbucket group to lookup if exists
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return True if group exists, False otherwise
        """
        return len([group for group in self.getGroups(accountName) if group['name'] == groupName]) > 0

    def deleteGroup(self, groupName, accountName):
        """
        Delete the specified Bitbucket group

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @raise Exception in case of errors
        """
        self._validateGroupAndAccountNames(groupName, accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, RESTMethod.DELETE, [groupSlug])

    def getGroupMembers(self, groupName, accountName):
        """
        Retrieve Bitbucket group members

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return Bitbucket group members, empty if no members exist
        @rtype list
        @raise Exception in case of errors
        """
        self._validateGroupAndAccountNames(groupName, accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, uriParts=[groupSlug, 'members'])

    def addGroupMember(self, memberLogin, groupName, accountName):
        """
        Add a new member to a Bitbucket group

        @param memberLogin:     Bitbucket member login
        @type memberLogin:      string
        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return The L{Member} if it has been added successfully
        @rtype L{Member}
        @raise Exception in case of errors
        """
        self._validateMemberAndGroupAndAccountNames(memberLogin, groupName, accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, RESTMethod.PUT, uriParts=[groupSlug, 'members', memberLogin])

    def updateGroup(self, groupName, accountName, **kwargs):
        """
        Update Bitbucket group settings

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @param kwargs:          Bitbucket group setteings required to be updated\
        @type kwargs:           dict
        @return The L{Group} after update if update has been done successfully
        @rtype L{Group}
        @raise Exception in case of errors
        """
        self._validateGroupAndAccountNames(groupName, accountName)
        group = self.getGroup(groupName, accountName)
        if kwargs:
            if not str(BitbucketSettingsParam.NAME) in kwargs:
                kwargs[str(BitbucketSettingsParam.NAME)] = group[str(BitbucketSettingsParam.NAME)]

            if not BitbucketSettingsParam.PERMISSION in kwargs:
                kwargs[str(BitbucketSettingsParam.PERMISSION)] = group[str(BitbucketSettingsParam.PERMISSION)]

        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, RESTMethod.PUT, [group['slug']], **kwargs)

    def deleteGroupMember(self, memberLogin, groupName, accountName):
        """
        Delete a member from a Bitbucket group

        @param memberLogin:     Bitbucket member login
        @type memberLogin:      string
        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @raise Exception in case of errors
        """
        self._validateMemberAndGroupAndAccountNames(memberLogin, groupName, accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUPS, RESTMethod.DELETE, uriParts=[groupSlug, 'members', memberLogin])

    def getGroupPrivileges(self, accountName, filter=None, private=None):
        """
        Retrieve all group privileges specified by that Bitbucket account

        @param accountName:     Bitbucket account name
        @type accountName:      string
        @param filter:          Filtering the permissions of privileges we are looking for
        @type filter:           L{BitbucketPermission}
        @param private:         Defines whether to retrieve privileges defined on private repositories or not
        @type private:          boolean
        @return All L{Privilege}s specified by that Bitbucket account name
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(accountName=accountName)
        params = dict()
        if filter:
            params['filter'] = filter

        if private != None:
            params['private'] = private

        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUP_PRIVILEGES.value, params=params)

    def getRepoGroupPrivileges(self, repoName, accountName):
        """
        Retrieve all group privileges specified by that Bitbucket account on that Bitbucket repository

        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return All L{Privilege}s specified by that Bitbucket account name on that Bitbucket repository
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(repoName=repoName, accountName=accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUP_PRIVILEGES.value, uriParts=[repoName])

    def grantGroupPrivileges(self, groupName, repoName, privilege, accountName):
        """
        Grant a group privilege to the specified Bitbucket repository

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository
        @type repoName:         string
        @param privilege:       Group privilege
        @type privilege:        L{BitbucketPermission}
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return List L{Privilege}s granted to the specified repository
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, repoName=repoName, accountName=accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        return self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUP_PRIVILEGES.value, RESTMethod.PUT, uriParts=[repoName, accountName, groupSlug], data=[str(privilege)])

    def revokeRepoGroupPrivileges(self, groupName, repoName, accountName):
        """
        Revoke group privileges on the defined Bitbucket repository

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, repoName=repoName, accountName=accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUP_PRIVILEGES.value, RESTMethod.DELETE, uriParts=[repoName, accountName, groupSlug])

    def revokeGroupPrivileges(self, groupName, accountName):
        """
        Revoke all group privileges

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param repoName:        Bitbucket repository name
        @type repoName:         string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=accountName)
        groupSlug = self._getGroupSlug(groupName, accountName)
        self._callBitbucketRestAPI(accountName, BitbucketRESTCall.GROUP_PRIVILEGES.value, RESTMethod.DELETE, uriParts=[accountName, groupSlug])

    def _getGroupSlug(self, groupName, accountName):
        """
        Retriev Bitbucket group slug name

        @param groupName:       Bitbucket group name
        @type groupName:        string
        @param accountName:     Bitbucket account name
        @type accountName:      string
        @return Bitbucket group slug name or Exception in case of errors
        @rtype string
        """
        self._validateValues(groupName=groupName, accountName=accountName)
        group = self.getGroup(groupName, accountName)
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

    # TODO - MNour : We need a proper validation mechanism. @see http://jcp.org/en/jsr/detail?id=303
#    def _validateAccountName(self, accountName):
#        """
#        Validates both Bitbucket account name
#
#        @param accountName:     Bitbucket account name
#        @type accountName:      string
#        @raise Exception if account name is not valid
#        """
#        if not accountName:
#            q.errorconditionhandler.raiseError('Invalid account name: [%s].' %accountName)
#
#    def _validateGroupAndAccountNames(self, groupName, accountName):
#        """
#        Validates both Bitbucket account and group names
#
#        @param groupName:       Bitbucket group name
#        @type groupName:        string
#        @param accountName:     Bitbucket account name
#        @type accountName:      string
#        @raise Exception if account/group names or both are not valid
#        """
#        if not groupName or not accountName:
#            q.errorconditionhandler.raiseError('Invalid group name: [%s], or account name: [%s].' %(groupName, accountName))
#
#    def _validateMemberAndGroupAndAccountNames(self, memberLogin, groupName, accountName):
#        """
#        Validates both Bitbucket account and group names
#
#        @param memberLogin:     Bitbucket member login
#        @type memberLogin:      string
#        @param groupName:       Bitbucket group name
#        @type groupName:        string
#        @param accountName:     Bitbucket account name
#        @type accountName:      string
#        @raise Exception if account/group names or both are not valid
#        """
#        if not memberLogin or not groupName or not accountName:
#            q.errorconditionhandler.raiseError('Invalid member login: [%s], or group name: [%s], or account name: [%s].' %(memberLogin, groupName, accountName))

#####################################################################################################################
#crowd m                                                                                                            #
#####################################################################################################################
    def crowdCheck_user(self,crowd_api_url, crowd_login, crowd_password):
        command = "curl -u %s:%s -H 'Accept: application/json' %sdirectory/crowd%%20to%%20bitbucket%%20syncing%%20tool/user/%s" %(crowd_login, crowd_password, crowd_api_url, crowd_login)
#curl -u admin:admin -H "Accept: application/json" http://localhost:8095/crowd/rest/admin/latest/directory/crowd%20to%20bitbucket%20syncing%20tool/user/admin
        try:
            user_found = q.system.process.run(command)[1]
        except:
            q.errorconditionhandler.raiseError("Error while executing command : %s"%command)
        else:
            try:
                user = json.loads(user_found)
            except:
                q.errorconditionhandler.raiseError("user credentials is no right... Lodin: %s password :%s"%(crowd_login, crowd_password))
            else:
                user_name = str(user.get("username"))
                if user_name == crowd_login:
                    return True

    def crowdCheck_group(self,crowd_api_url, crowd_login, crowd_password, crowd_group_to_sync):
        user = self.crowdCheck_user(crowd_api_url, crowd_login, crowd_password)
        if user:
            command = "curl -u %s:%s -H 'Accept: application/json' %sdirectory/crowd%%20to%%20bitbucket%%20syncing%%20tool/group/%s" %(crowd_login, crowd_password, crowd_api_url, crowd_group_to_sync)
    #curl -u admin:admin -H "Accept: application/json" http://localhost:8095/crowd/rest/admin/latest/directory/crowd%20to%20bitbucket%20syncing%20tool/group/crowd-administrators
            try:
                group_found = q.system.process.run(command)[1]
            except:
                q.errorconditionhandler.raiseError("Error while executing command : %s"%command)
            else:
                
                try:
                    group = json.loads(group_found)
                except:
                    q.errorconditionhandler.raiseError("Group %s does not exist."%crowd_group_to_sync)
                else:
                    group_name = str(group.get("name"))
                    if group_name == crowd_group_to_sync:
                        return True


    def crowdGet_group_members(self,crowd_api_url, crowd_login, crowd_password, crowd_group_to_sync):
        group_members = list()
        command = "curl -u %s:%s -H 'Accept: application/json' %sdirectory/crowd%%20to%%20bitbucket%%20syncing%%20tool/user?search="%(crowd_login, crowd_password, crowd_api_url)
#curl -u admin:admin -H "Accept: application/json" http://localhost:8095/crowd/rest/admin/latest/directory/crowd%20to%20bitbucket%20syncing%20tool/user?search=
        try:
            users = q.system.process.run(command)[1]
        except:
            q.errorconditionhandler.raiseError("Error while executing command : %s"%command)
        else:
            users_list = list()
            users = (json.loads(users))['user']
#            users2 = users['user']
            for user in users:
                users_list.append(str(user.get("username")))
            
            for user_key in users_list:
                
                command1 = "curl -u %s:%s -H 'Accept: application/json' %sdirectory/crowd%%20to%%20bitbucket%%20syncing%%20tool/user/%s/memberships"%(crowd_login, crowd_password, crowd_api_url, user_key)
#curl -u admin:admin -H "Accept: application/json" http://localhost:8095/crowd/rest/admin/latest/directory/crowd%20to%20bitbucket%20syncing%20tool/user/admin/memberships
                try:
                    groups = q.system.process.run(command1)[1]
                except:
                    q.errorconditionhandler.raiseError("Error while executing command : %s"%command1)
                else:
                    print groups
#                    (json.loads(groups))['group']
                    groups_j = (json.loads(groups))#['group']
                    print groups_j
                    groups_j_2 = groups_j['group']
                    for group in groups_j_2:
                        group_name = group.get('name')
                        if group_name == crowd_group_to_sync:
                            group_members.append(user_key)
                            break
        
            return group_members
    
    def synchronizegroup(crowd_api_url, crowd_login, crowd_password, crowd_group_to_sync,\
                         bitbucket_api_url, bitbucket_login, bitbucket_password, bitbucket_repository):
        
        if self.crowdCheck_group(crowd_api_url, crowd_login, crowd_password, crowd_group_to_sync):
            pass
        