# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

from pylabs import q
from pylabs.baseclasses import BaseType
from pylabs.qpackages.server.Session import Session
from pylabs.qpackages.common.QPackageObject import QPackageObject

class SessionManager(BaseType):
    """
    Is responsible for all session on a qpackage server.

    Will create and expose all rsync modules for a session.
    """

    SESSION_TIMEOUT = 7200

    sessions = q.basetype.dictionary(doc='Dictionary of active sessions', default=dict(), allow_none=False)


    def sessionCreate(self, login, ipAddress=None):
        """
        Create a new session on the server (rsync) for the given client

        @param login: The client's login
        @param ipAdress: The client's ip address

        @return:      session object
        """
        session = self._getSessionForClient(login, ipAddress)
        if session and self.sessionValidate(session.id):
            return session

        session = Session()
        session.login = login
        session.ipAddress = ipAddress

        q.logger.log('Creating rsync read and write modules for the new session', 5)
        self._manageRsyncModules(session.id)
        self._manageVlistsDir(session.id)
        self.sessions[session.id] = session
        
        return session

    def _getSessionForClient(self, login, ipAddress):
        """
        Retrieve session for client with login and ipAddress
        @param login: The client's login
        @param ipAdress: The client's ip address
        """
        q.logger.log('Checking if client with login <%s> and ip address <%s>'%(login, ipAddress), 6)
        for session in self.sessions.itervalues():
            if str(login) == session.login and str(ipAddress) == session.ipAddress:
                return session
        return None
    
    def sessionDelete(self, sessionId):
        """
        Removes a given session from the server
        
        @param sessionId: The session's unique identifier
        """
        q.logger.log('Deleting session with id %s' % sessionId)

        if self.sessionExists(sessionId):        
            self._manageVlistsDir(sessionId, True)
            self._manageRsyncModules(sessionId, False)
            self.sessions.pop(sessionId)
    
    def sessionValidate(self, sessionId):
        """
        Checks if a session is still valid.
        
        @param sessionId: The session's unique identifier 
        
        @return:          Boolean indicating if session is valid or not
        """
        if self.sessionExists(sessionId):
            q.logger.log('Session <%s> was created on <%s> last update on <%s>'%(sessionId, self.sessions[sessionId].created, self.sessions[sessionId].updated), 6)
            if (q.base.time.getTimeEpoch() - self.sessions[sessionId].updated) < SessionManager.SESSION_TIMEOUT:
                return True
        return False
    
    def sessionExists(self, sessionId):
        """
        Checks if a session exists.
        @param sessionId: The session's unique identifier
        @return:          Boolean indicating if session exists or not
        """        
        return sessionId in self.sessions
    
    def sessionUpdate(self, sessionId):
        """
        Updates a given session's 'updated' timestamp to keep the session alive.
        @param sessionId: The session's unique identifier
        """
        q.logger.log('Updating session with id %s' % sessionId)
        
        if self.sessionExists(sessionId):
            self.sessions[sessionId].updated = q.base.time.getTimeEpoch()
        else:
            raise ValueError('Session with id %s does not exist! Maybe already expired?' % sessionId)

    def qpackageGetObject(self, sessionId, qpackageName, version, domain, moduleType='read'):
        """
        Retrieves a qpackage object from session
        @param sessionId: The session's unique identifier
        @param qpackageName: name of the qpackage to retrieve
        @param version: version of the qpackage to retrieve
        @param domain: domain name of the qpackage to retrieve
        @param moduleType: rsync module to retrieve qpackage from
        """
        return QPackageObject(domain, qpackageName, version, rootPath=q.system.fs.joinPaths(self.getSessionPath(sessionId), moduleType, 'qpackages'))

    def getSessionPath(self, sessionId):
        """
        Returns the path to the session
        @param sessionId: The session's unique identifier
        """
        return q.system.fs.joinPaths(q.dirs.varDir, 'sessions', sessionId)

    def sessionsCleanUp(self):
        """
        Deletes unused sessions
        """
        q.logger.log('Cleaning up unused sessions', 5)
        sessions = list(self.sessions)
        for sessionId in sessions:
            if not self.sessionValidate(sessionId):
                self.sessionDelete(sessionId)

    def _manageRsyncModules(self, sessionId, create=True):
        """
        Add/Delete rsync modules
        @param sessionId: 
        @param create: flad to indicate whether to create or remove
        """
        readOnlyDir, writeDir = self._manageSyncDirs(sessionId, create)

        q.manage.rsync.startChanges()
        if create:
            readOnlyModule = q.manage.rsync.cmdb.addModule('%s_read'%sessionId, readOnlyDir)
            readOnlyModule.readOnly = True
            readOnlyModule.mungeSymlinks = False

            writableModule = q.manage.rsync.cmdb.addModule('%s_write'%sessionId, writeDir)
            writableModule.readOnly = False
        else:
            if '%s_read'%sessionId in q.manage.rsync.cmdb.modules:
                q.logger.log('Removing rsync module <%s_read>'%sessionId, 5)
                q.manage.rsync.cmdb.removeModule('%s_read'%sessionId)
            if '%s_write'%sessionId in q.manage.rsync.cmdb.modules:
                q.logger.log('Removing rsync module <%s_write>'%sessionId, 5)
                q.manage.rsync.cmdb.removeModule('%s_write'%sessionId)
        q.manage.rsync.save()    

        q.manage.rsync.applyConfig()
    
    def _manageSyncDirs(self, sessionId, create=True):
        """
        Create/Remove session directories
        @param sessionId
        @param create: flad to indicate whether to create or remove
        """
        sessionDir = self.getSessionPath(sessionId)
        readOnlyDir = q.system.fs.joinPaths(sessionDir, 'read')
        writeDir = q.system.fs.joinPaths(sessionDir, 'write')
        if create:
            if not q.system.fs.isDir(sessionDir):
                q.logger.log('Creating session directory <%s>'%sessionDir, 5)
                q.system.fs.createDir(sessionDir)
    
            q.system.fs.createDir(readOnlyDir)
            q.system.fs.createDir(writeDir)
        else:
            if q.system.fs.isDir(readOnlyDir):
                q.system.fs.removeDirTree(readOnlyDir)
            if q.system.fs.isDir(writeDir):
                q.system.fs.removeDirTree(writeDir)

            q.system.fs.removeDirTree(sessionDir)

        return readOnlyDir, writeDir
    
    def _manageVlistsDir(self, sessionId, remove=False):
        """
        Create a symlink for /opt/qbase2/cfg/qpackageserver/vlists in session dir
        @param sessionId: id of the session
        """
        vlistDir = q.system.fs.joinPaths(q.dirs.cfgDir, 'qpackageserver', 'vlists')
        if remove:
            q.system.fs.unlink(q.system.fs.joinPaths(self.getSessionPath(sessionId), 'read', 'vlists'))
        else:
            q.system.fs.symlink(vlistDir, q.system.fs.joinPaths(self.getSessionPath(sessionId), 'read', 'vlists'))