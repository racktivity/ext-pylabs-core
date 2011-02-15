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

# NOTE: getFilesFrom is used in the code but does no longer exist

import re
import os
# attrgetter('_myAttribute') returns a method (not the attribute value)
# the returned method will return the attribute value when called
# this is great for properties
from operator import attrgetter

import pylabs

"""
The Sync module provides three Sync classes to do various Sync operations
(local sync, sync to server and sync from server)

This module replaces an old implementation with (almost) the same API. The only
known difference is the behaviour of SyncToServer: this version of the module
does _not_ automatically add forward slashes to the source and destination.
Fix your code accordingly.

This module was rewritten to add consistent and correct cygwin behaviour:
the old module did not convert local paths to cygwin paths in windows, causing
problems with paths that contained spaces. This new version should work
flawless in the Windows sandbox.
"""

def log(msg, level=9):
    return pylabs.q.logger.log(msg, level)

class Endpoint(object):
    def clean(self, value):
        raise NotImplementedError


class LocalEndpoint(Endpoint):
    #@todo why so complicated, why not just methods on the base rsync class?
    def clean(self, value):
        pylabs.q.logger.log("Cleaning local endpoint '%s'" % (value, ), 8)

        if pylabs.q.platform.isWindows():
            cleaned = self._getCygwinPath(pylabs.q.system.fs.pathShorten(value))
        else:
            cleaned = value

        pylabs.q.logger.log("Cleaned local endpoint: '%s'" % (cleaned, ), 8)
        return cleaned

    def _getCygwinPath(self, path):
        pylabs.q.logger.log("Converting path '%s' to a cygwin path" % (path, ), 5)
        driveLetter, path = os.path.splitdrive(path)
        convertedPath = "/".join(path.split(os.path.sep))
        if driveLetter:
            pylabs.q.logger.log("Found drive letter '%s'" % (driveLetter, ), 6)
            # Make drive letter lowercase and remove the ":"
            driveLetter = driveLetter.lower()
            driveLetter = driveLetter.replace(":", "")
            # convertedPath already starts with a '/', so there is no need to
            # add one between driveLetter and convetedPath
            convertedPath = "/cygdrive/%s%s" % (driveLetter, convertedPath)
        pylabs.q.logger.log("Converted path to '%s'" % (convertedPath, ), 6)
        return convertedPath

class RemoteEndpoint(Endpoint):
    def clean(self, value):
        value = value.replace("\\","/")
        if(value != '' and value[0] != "/"):
            value = "/%s" % (value, )

        return value

class Sync(object):
    """
    The new Sync is a wrapper on top of Rsync (part of sandbox on Microsoft Windows)
    
    Abstract class, #@todo doesn't look like an abstract class?
    """
    #@todo why distinction between endpoints & destination dir
    _destinationEndpoint = None  #@todo how can this be none and not the endpoint?
    _sourceEndpoint = None        #@todo how can this be none and not the endpoint?

    _destinationDir = None

    def executeCommand(self,command,nrRetries=10):
        """
        better wrapped process execute function
        checks for errors and will repeat, sometimes happens rsync server is not reachable for short time
        """
        exitcode=1
        counter=0
        pylabs.q.logger.log("RSYNC: " + command, 5)
        while exitcode<>0 and counter < nrRetries:
            (exitcode, output) = pylabs.q.system.process.execute(command.strip(), dieOnNonZeroExitCode=False,outputToStdout=False)
            if exitcode<>0:
                pylabs.q.logger.log('RSYNC FAILED (%s): [%s]' % (str(exitcode), output), 2)
                pylabs.q.logger.log("RSYNC WILL TRY AGAIN: %s/%s" % (counter,nrRetries))
                counter +=1
        if counter == nrRetries:
            q.eventhandler.raiseCriticalError("Cannot use rsync to sync content from or to server, have tried multiple times, please check log and try rsync command manually. \nProbably means server is no longer available.")
        return [exitcode,output]                
    
    def setDestinationDir(self, value):
        """
        Set destinationdir
        
        public method for backwards compatibility
        """
    #@todo if someone calls this and endpoint is not the class yet this will fail? Looks wrong.
        self._destinationDir = self._destinationEndpoint.clean(value)
        log("Destination dir set to '%s' (dirty: '%s')" % (value, self._destinationDir), 9)

    destinationdir = property(fget=attrgetter('_destinationDir'), fset=setDestinationDir) # TODO doc

    _sourceDir = list()

    def setSourceDir(self, value):
        """
        Set sourcedir
        
        public method for backwards compatibility
        """
        self._sourceDir = self._sourceEndpoint.clean(value)
        log("Source dir set to '%s' (dirty: '%s')" % (self._sourceDir, value), 9)

    sourcedir = property(fget=attrgetter('_sourceDir'), fset=setSourceDir) # TODO doc

    def setSourceFile(self, value):
        # This is an ugly hack, used by syncFile and
        # i.qlayer.applianceInstaller.setupAppliance()
        log("Setting source file to '%s'" % (value, ), 9)
        self.setSourceDir(value)

    _rsyncModule = None

    def setRsyncModule(self, destModule):
        """
        specify rsync module to work from
        
        public method for backwards compatibility
        """
        #TODO: we have to check if module exists
        destModule = destModule.replace("/", "")
        self._rsyncModule = destModule
        #if destModule not in self.modulesOnServer: #@remark because we don't do the checkconnection any more we don't know the modules.
        #    raise ValueError("Can not set rsync module on rsync server because module is unknown. Known modules: %s" % self.modulesOnServer)

    rsyncmodule = property(fget=attrgetter('_rsyncModule'), fset=setRsyncModule) # TODO doc  #@todo all very unclean, some are properties, others aren't. WHY?

    filesFrom = None
    server = None
    modulesOnServer = list()
    
    """skip based on checksum, not mod-time & size"""
    _skipBasedOnCRC = False

    def enableSkipBasedOnCRC(self):
        """
        skip based on checksum, not mod-time & size
        """
        self._skipBasedOnCRC = True

    def disableSkipBasedOnCRC(self):
        """
        use CRC to see if files are equal
        """
        self._skipBasedOnCRC = False

    _port = None

    def _setPort(self, value):
        if value == 0:
            value = None
        self._port = value

    port = property(fget=attrgetter('_port'), fset=_setPort)

    """verbose option"""
    _verbose = False

    def enableVerbose (self):
        self._verbose = True

    def disableVerbose (self):
        self._verbose = False

    """archive mode option"""
    _archive = False

    def enableArchive (self):
        self._archive = True

    def disableArchive (self):
        self._archive = False

    """Keep the permissions, owner and group of files when copying"""
    _keepPermissionsOwnerGroup = False

    def enableKeepPermissionsOwnerGroup (self):
        self._keepPermissionsOwnerGroup = True

    def disableKeepPermissionsOwnerGroup (self):
        self._keepPermissionsOwnerGroup = False

    """recurse into directories"""
    _recursive = True

    def enableRecursive(self):
        self._recursive = True

    def disableRecursive(self):
        self._recursive = False

    """skip files that are newer on the receiver"""
    _update = False

    def enableUpdate(self):
        self._update = True

    """delete extraneous files from dest dirs"""
    _delete = False

    def enableDelete(self):
        self._delete = True

    """only update files that already exist"""
    _existing = False

    def enableExisting(self):
        self._existing = True

    """copy symlinks as symlinks, treat symlinked dir on receiver as dir"""
    _keepSymlinkedDirs = False

    def enableKeepSymlinkedDirs(self):
        self._keepSymlinkedDirs = True

    def disableKeepSymlinkedDirs(self):
        self._keepSymlinkedDirs = False

    """include filters"""
    _includeFilter = list()

    def addIncludeFilter(self, rule):
        """
        add include rule
        rule is a line like specified in rsync
        """
        self._includeFilter.append(rule)

    """exclude filters"""
    _excludeFilter = list()

    def addExcludeFilter(self, rule):
        """
        add exclude rule
        rule is a line like specified in rsync
        """
        self._excludeFilter.append(rule)

    def clearFilters(self):
        self._excludeFilter = list()
        self._includeFilter = list()

    # Here we can add new options easily to be added to the Rsync command
    def _constructCommandOptions(self, dryRun=False):

        # We copy symlinks as symlinks. THIS WILL BREAK IF THE VAPP symlinks
        # outside its own dir
        command = "rsync -l --copy-unsafe-links "

        if self.port :
            command = command + '--port=' + str(self.port) + ' '
        if self._skipBasedOnCRC :
            command = command + "--checksum "
        if self._verbose :
            command = command + "--verbose --progress "
        if self._archive :
            command = command + "--archive "
        if self._keepPermissionsOwnerGroup :
            command = command + "-pog "
        if self._recursive :
            command = command + "--recursive "
        if self._update :
            command = command + "--update "
        if self._delete :
            command = command + "--delete "
        if self._existing :
            command = command + "--existing "
        if self._keepSymlinkedDirs :
            command = command + "-lK "
        if dryRun:
            command = command + "-n "
        if pylabs.q.platform.isWindows():
            command = command + "--perms --chmod=a=rwx,Da+x "

        if not len(self._includeFilter) == 0 :
            while not len(self._includeFilter) == 0 :
                rule = self._includeFilter.pop()
                command = command + '--include=' + rule + ' '

        if not len(self._excludeFilter) == 0 :
            while not len(self._excludeFilter) == 0 :
                rule = self._excludeFilter.pop()
                command = command + '--exclude=' + rule + ' '

        if not self.filesFrom == None :
            command = command + '--files-from=' + '"' + self.filesFrom + '" '

        return command

    def do(self, dryRun=False, ignoreErrorNr=0):
        """
        if dryrun True than only what would have been done will be logged, not executed
        """
        raise NotImplementedError


class SyncLocal(Sync):
    _destinationEndpoint = LocalEndpoint()
    _sourceEndpoint = LocalEndpoint()

    def __init__(self, sourcePrefix):
        Sync.__init__(self)  #@todo don't find an __init__ on sync?????????
        if not sourcePrefix:
            raise TypeError('SyncLocal needs a sourcePrefix')

        if not pylabs.q.system.fs.exists(sourcePrefix):
            raise ValueError('SyncLocal: sourcePrefix needs to be existing dir')

        sourcePrefix = sourcePrefix.rstrip(os.sep)
        self._sourcePrefix = sourcePrefix

    def _addRsyncCommandDestDir(self, command):
        if self.destinationdir :
            command = '%s "%s" ' % (command, self.destinationdir)
        return command

    #command format could be one of the following:
    #    1- rsync [OPTION]... SRC [SRC]... DEST
    #    2- rsync [OPTION]... SRC
    def _constructRsyncCommand(self, dryRun=False):
        #@TODO: implement
        command = self._constructCommandOptions(dryRun)
        command = command + '"' + self.sourcedir + '" '
        command = self._addRsyncCommandDestDir(command)
        return command.strip()

    def do(self, dryRun=False, ignoreErrorNr=0):
        destSubs = pylabs.q.system.fs.WalkExtended(self.destinationdir)
        if self.sourcedir.rstrip(os.sep) in destSubs:
            pylabs.q.logger.log("SKIPPED local sync from [%s] to [%s]" % (self.sourcedir, self.destinationdir), 7)
            return

        command = self._constructRsyncCommand(dryRun)

        (exitcode, output) = self.executeCommand(command)
        
        #@todo looks like weard code, needs to be checked
        if isinstance(ignoreErrorNr, list):
            if exitcode != 0 and (not exitcode in ignoreErrorNr):
                pylabs.q.logger.log('RSYNC FAILED (%s): [%s]' % (str(exitcode), output), 2)
        else:
            if exitcode != 0 and exitcode != ignoreErrorNr:
                pylabs.q.logger.log('RSYNC FAILED (%s): [%s]' % (str(exitcode), output), 2)

class SyncToServer(Sync):
    _destinationEndpoint = RemoteEndpoint()
    _sourceEndpoint = LocalEndpoint()

    login = None
    passwd = None

    def __init__(self, server, module, port=0):
        Sync.__init__(self)
        self.server = server
        self.port = port
        #self.checkConnection()  #@todo hope this does not give problems, right now the process is very non flexible because this check takes too much time if too many modules
        self.setRsyncModule(module)  #@todo above has been implemented as property but we dont use it as such

    # @todo this is not robust. I get some erroneous modules (e.g. "WELCOME")
    def checkConnection(self):
        # e.g cmd: "rsync 127.0.0.1::"   this will list all modules on local rsync server
        if self.port != 0:
            command = 'rsync --port=%d %s::' % (self.port, self.server)
            pylabs.q.logger.log("Checking connection: %s" % (command, ))
            exitcode, output = pylabs.q.system.process.execute(command, False, outputToStdout=False)
        else:
            command = "rsync %s::" % (self.server, )
            pylabs.q.logger.log("Checking connection: %s" % (command, ))
            exitcode, output=pylabs.q.system.process.execute(command, False, outputToStdout=False)
        if ( exitcode==0):
            modules = output
            lines = output.splitlines()
            modules = []
            for line in lines:
                line = line.strip()
                if line <> "":
                    cols = line.split("\t")
                    module = cols[0].strip()
                    modules.append(module)
            self.modulesOnServer = modules
        else:
            pylabs.q.errorconditionhandler.raiseCriticalError("there are no active connections")


    #command format could be one of the following:
    #    1- rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
    #    2- rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
    #    3- rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
    def _constructRsyncCommand(self, dryRun=False):
        if self.server == None:
            raise TypeError("have to specify rsync server")
        if self.rsyncmodule == None :
            raise TypeError("have to specify rsync module")

        command = self._constructCommandOptions(dryRun)
        command = '%s"%s" ' % (command, self.sourcedir)

        if self.login != None :
            command = command + '"rsync://' + self.login + "@" + self.server
            os.environ['RSYNC_PASSWORD'] = "%s" % self.passwd
        else:
            command = command + '"rsync://' + self.server

        command = command + '/' + self.rsyncmodule + '/' + self.destinationdir + '"'
        return command

    def do(self, dryRun=False):
        command = self._constructRsyncCommand(dryRun)
        pylabs.q.logger.log("Sync: %s" % (command, ), 5)
        (exitcode, output) = self.executeCommand(command)

class SyncFromServer(SyncToServer):
    _destinationEndpoint = LocalEndpoint()
    _sourceEndpoint = RemoteEndpoint()

    #command format could be one of the following:
    #    1- rsync [OPTION]... [USER@]HOST:SRC [DEST]
    #    2- rsync [OPTION]... [USER@]HOST::SRC [DEST]
    #    3- rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
    def _constructRsyncCommand(self, dryRun=False):
        if self.server == None:
            raise TypeError("have to specify rsync server")
        if self.rsyncmodule == None :
            raise TypeError("have to specify rsync module")
        if self.destinationdir == None :
            raise TypeError("have to specify rsync destinationdir")

        #this function overwrite the base class function
        command = self._constructCommandOptions(dryRun)
        sourceDir = self.sourcedir
        destDir=  self.destinationdir

        if self.login <> None :
            command = command + self.login + "@"
            os.environ['RSYNC_PASSWORD'] = "%s" % self.passwd
        command = command + self.server
        command = command + "::"

        command = command + self.rsyncmodule + "/" + sourceDir + " "

        command = command + '"' + destDir + '" '
        return command

    def dir(self, path, listSymlinks=False):
        """
        List the directories and files from path in the rsync module.
        By default symlinks are not displayed, setting listSymlinks to True will show the symlinks

        @param path: path from which we wan't to view the files
        @type path: string
        @param listSymlinks: return symlinks if True
        @type listSymlinks: bool

        @return: list of found files and directories
        @rtype: iterable
        """
        if self.server == None:
            raise TypeError("have to specify rsync server")
        if self.rsyncmodule == None :
            raise TypeError("have to specify rsync module")

        # Fix up path
        # TODO -> method? (a method for converting a file path to an url path)
        path = path.replace("\\","/")
        # Must end with '/'
        if not path.endswith('/'):
            path = "%s/" % path

        command = "rsync --list-only "
        if self.port :
            command = command + '--port=' + str(self.port) + ' '
        if self.login :
            command = command + self.login + "@"
        command = command + self.server
        command = command + "::"
        command = command + self.rsyncmodule + "/" + path + " "

        pylabs.q.logger.log("Sync dir command: '%s'" % command,5)

        returncode, output = self.executeCommand(command)

        lines = output.splitlines()
        paths = list()
        if listSymlinks:
            reobj = re.compile(r"^[l|d|-][r|w|x|s|-]{9}\W+[0-9]+\W[0-9]{4}/[0-9]{2}/[0-9]{2}\W[0-9]{2}:[0-9]{2}:[0-9]{2}\W(.*)$")
        else:
            reobj = re.compile(r"^[d|-][r|w|x|s|-]{9}\W+[0-9]+\W[0-9]{4}/[0-9]{2}/[0-9]{2}\W[0-9]{2}:[0-9]{2}:[0-9]{2}\W(.*)$")

        for line in lines:
            match = reobj.search(line)
            if match:
                path = match.group(1)
                if path != "." and path != "..":
                    paths.append(path)
        return paths

    def syncFile(self,source): # Used once  #@what is this??????
        self.setSourceFile(source)
        self.do()
        self.setSourceFile('')
