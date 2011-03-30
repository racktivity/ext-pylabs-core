import json
from pylabs import q
from pylabs.baseclasses import BaseEnumeration
from pylabs.Shell import *
import urllib

class CrowdResource(BaseEnumeration):
    """
    Enumerator of all supported Crowd resources
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('directory')
        cls.registerItem('group')
        cls.registerItem('user')
        cls.finishItemRegistration()

class Crowd:
    """
    Crowd client enables administrators and developers leveraging Crowd services through PyLabs
    """

    def __init__(self):
        self.apiVersion = 'latest'
        self.context = 'crowd'
        self.apiName = 'admin'
        self.apiURI = 'http://localhost:8095'
        self.resultFormat = q.enumerators.RESTResultFormat.JSON

    def accountAdd(self, account='', login='', passwd=''):
        """
        Add new Crowd account

        @param account:         Crowd account name
        @type account:          string
        @param login:           Crowd account login
        @type login:            string
        @param passwd:          Crowd account password
        @type passwd:           string
        """
        if account != '' and login != '' and passwd != '':
            try:
                self._config.remove(account)
            except:
                pass
            self._config.add(account, {'login': login, 'passwd': passwd})
        else:
            self._config.add()

    def accountsReview(self):
        """
        Review Crowd accounts
        """
        self._config.review()

    def accountsShow(self):
        """
        Show Crowd accounts
        """
        self._config.show()

    def accountsRemove(self, accountName=''):
        """
        Remove Crowd account
        """
        self._config.remove(accountName)

    def accountGetConfig(self, accountName=''):
        """
        Retriev Crowd account configuration
        """
        return self._config.getConfig(accountName)

    def accountGetLoginInfo(self, accountName=''):
        """
        """
        # TODO - MNour: Do we still need this line
        # self.init()
        if accountName == '':
            accountName = q.gui.dialog.askChoice('Select Crowd account name', self._getAccountNames())

        config = self.accountGetConfig(accountName)
        login = config['login']
        passwd = config['passwd']
        if login == '' or passwd == '':
            self.accountsReview(accountName)

        # TODO - MNour: Rwrite this line to follow the Crowd conventions
        # url = " https://%s:%s@bitbucket.org/%s/" % (login, passwd, accountName)
        url = ''
        return url, login, passwd

    def getGroup(self, groupName, directoryName, accountName):
        """
        Retrieve the specified Crowd group

        @param groupName:           Crowd group name
        @type groupName:            string
        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd accountName
        @type accountName:          string
        @return Crowd L{Group} with the specified name if any
        @rtype L{}
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, directoryName=directoryName, accountName=accountName)
        groups = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.GROUP)],
                                        params={'search': groupName})

        if groups and len(groups['group']) > 1:
            q.errorconditionhandler.raiseError("Found more than one group with name '%s'." %groupName)

        return groups['group'] if groups else dict()

    def getGroups(self, directoryName, accountName):
        """
        Retrieve all Crowd groups defined under the specified Crowd directory

        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd accountName
        @type accountName:          string
        @return A list of Crowd L{Group} definitions, empty list if no groups defined under this directory
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(directoryName=directoryName, accountName=accountName)
        groups = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.GROUP)],
                                        params={'search': ''})

        return groups['group'] if groups else list()

    def checkGroup(self, groupName, directoryName, accountName):
        """
        Check for the existence of a Crowd group in a the specified Crowd directory

        @param groupName:           Crowd group name
        @type groupName:            string
        @param directiryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd account name
        @type accountName:          string
        @return True if group exists, False otherwise
        @rtype Boolean
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, accountName=accountName)
        groups = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.GROUP)],
                                        params={'search': groupName})

        if groups:
            return len(groups['group']) == 1

        return False

    def getUsers(self, directoryName, accountName):
        """
        Retrieve all Crowd users defined under the specified Crowd directory

        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd accountName
        @type accountName:          string
        @return A list of Crowd L{User} definitions, empty list if no users defined under this directory
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(directoryName=directoryName, accountName=accountName)
        users = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.USER)],
                                       params={'search': ''})

        return users['user'] if users else list()

    def getUser(self, userName, directoryName, accountName):
        """
        Retrieve the specified Crowd user

        @param userName:            Crowd uer name
        @type userName:             string
        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd accountName
        @type accountName:          string
        @return Crowd L{User} with the specified name if any
        @rtype L{User}
        @raise Exception in case of errors
        """
        self._validateValues(userName=userName, directoryName=directoryName, accountName=accountName)
        users = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.USER)],
                                       params={'search': userName})

        if users and len(users['user']) > 1:
            q.errorconditionhandler.raiseError("Found more than one user with name '%s'." %userName)

        return users['user'] if users else dict()

    def checkUser(self, userName, directoryName, accountName):
        """
        Check for the existence of a Crowd user in a the specified Crowd directory

        @param userName:            Crowd user name
        @type userName:             string
        @param directiryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd account name
        @type accountName:          string
        @return True if user exists, False otherwise
        @rtype Boolean
        @raise Exception in case of errors
        """
        self._validateValues(userName=userName, directoryName=directoryName, accountName=accountName)
        users = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.USER)],
                                        params={'search': userName})

        if users:
            return len(users['user']) == 1

        return False

    def getUserGroupMemberships(self, userName, directoryName, accountName):
        """
        Retrieve all Crowd group the specified user is a member of

        @param userName:            Crowd user name
        @type userName:             string
        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd account name
        @type accountName:          string
        @return List of Crowd L{Group}s, empty list if user is not a member of any group
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(userName=userName, directoryName=directoryName, accountName=accountName)
        groups = self._callCrowdRestAPI(accountName, CrowdResource.DIRECTORY, uriParts=[directoryName, str(CrowdResource.USER), userName, 'memberships'])
        return groups['group'] if groups else list()

    def checkUserGroupMemebership(self, userName, groupName, directoryName, accountName):
        """
        Check whethe the user is a member of the Crowd group specified

        @param userName:            Crowd user name
        @type userName:             string
        @param groupName:           Crowd group name
        @type groupName:            string
        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd accountName
        @return True if the user is a member of the group specified, False otherwise
        @rtype Boolean
        @raise Exception in case of errors
        """
        self._validateValues(userName=userName, groupName=groupName, directoryName=directoryName, accountName=accountName)
        groups = self.getUserGroupMemberships(userName, directoryName, accountName)
        if groups:
            return len([group for group in groups if group['name'] == groupName]) == 1

        return False

    def getGroupUsers(self, groupName, directoryName, accountName):
        """
        Retrieve all users in the specified Crowd group

        @param groupName:           Crowd group name
        @type groupName:            string
        @param directoryName:       Crowd directory name
        @type directoryName:        string
        @param accountName:         Crowd account name
        @type accountName:          string
        @return List of Crowd L{User}s, or empty list if no users defined in the specified group
        @rtype list
        @raise Exception in case of errors
        """
        self._validateValues(groupName=groupName, directoryName=directoryName, accountName=accountName)
        users = self.getUsers(directoryName, accountName)
        return [user['username'] for user in users if self.checkUserGroupMemebership(user['username'], groupName, directoryName, accountName)]

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

    def _getAccountNames(self):
        names = q.clients.crowd._config.list()
        # TODO - MNour: Do we still need this line
        # self._accountnames = names
        return names

    # TODO - MNour: Rwrite this method to work with Crowd REST API(s)
    def _callCrowdRestAPI(self, accountName, call, method=q.enumerators.RESTMethod.GET, uriParts=None, params=None, data=None):
        """
        Make a call to one of the Crowd REST API(s)

        @param accountName:     Bitbucket account name
        @type accountName:      string
        @param call:            Crowd REST call/resource to access
        @type call:             L{CrowdResource}
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
        # TODO - KDS: Need a better way than curl, the authentication doesnt seem to work when using the http pylabs extension.
        q.platform.ubuntu.checkInstall("curl","curl")
        resultTmpfile = q.system.fs.joinPaths(q.dirs.tmpDir, q.base.idgenerator.generateGUID())
        headerTmpfile = q.system.fs.joinPaths(q.dirs.tmpDir, q.base.idgenerator.generateGUID())
        accountConfig = self.accountGetConfig(accountName)
        uriPartsString = '%s/' %'/'.join(uriParts).replace(' ', '%20') if uriParts else ''
        parameters = urllib.urlencode(params).replace('+', '%20') if params else dict()

        dataString = ''
        if data:
            if type(data) is list:
                dataString = ','.join(data)
            elif type(data) is dict:
                dataString = urllib.urlencode(data)
            else:
                q.errorconditionhandler.raiseError("Invalid data type '%s', data value is '%s'." %(type(data), data))

        cmd = "curl --dump-header %(headerTmpfile)s --user %(login)s:%(password)s --request %(method)s --header 'Accept: application/%(resultFormat)s' '%(apiURI)s/%(context)s/rest/%(apiName)s/%(apiVersion)s/%(call)s/%(uriParts)s?%(parameters)s' > %(resultTmpfile)s" %{'headerTmpfile': headerTmpfile,
              'login': accountConfig['login'], 'password': accountConfig['passwd'], 'call': call, 'resultTmpfile': resultTmpfile,
              'apiURI': self.apiURI, 'apiVersion': self.apiVersion, 'method': method, 'uriParts': uriPartsString,
              'parameters': parameters, 'context': self.context, 'apiName': self.apiName, 'resultFormat': self.resultFormat}

        resultcode, content = q.system.process.execute(cmd, False, True)
        if resultcode > 0:
            q.errorconditionhandler.raiseError('Error while accessing Crowd %s resource. Cannot execute %s' %(call, cmd))

        # TODO - MNour: Add error checking and handling.
        content = q.system.fs.fileGetContents(resultTmpfile )
        q.system.fs.removeFile(resultTmpfile)
        q.system.fs.removeFile(headerTmpfile)

        try:
            object = json.loads(content) if content else dict()
        except:
            q.errorconditionhandler.raiseError('Cannot call rest api of Crowd, call was %s' %cmd)

        # TODO - MNour: Do we need to construct Bitbucket resources classes out of json deserialized object ?
        return object
