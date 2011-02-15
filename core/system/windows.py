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

import sys, os, threading, time
import os.path

if not sys.platform.startswith('win'):
    raise RuntimeError("WindowsSystem module only supported on Windows operating system")

import win32pdh
import win32api
import win32process
import win32file
import win32security
import win32netcon
import win32net
import win32service
import win32serviceutil
from win32com.client import GetObject
import ntsecuritycon as con
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from ctypes import *
#import CommandLauncher
#PSAPI.DLL
psapi = windll.psapi
#Kernel32.DLL
kernel = windll.kernel32
from win32com.shell import shell, shellcon
import _winreg as reg
from pylabs.enumerators.WinRegHiveType import WinRegHiveType
from pylabs.enumerators.WinRegValueType import WinRegValueType

import pylabs
from pylabs.inifile import IniFile
import shutil

class WindowsSystem:

    mythreads = []
    _userEveryone = None

    # Singleton pattern
    __shared_state = {}

    _wmi = GetObject('winmgmts:')

    def __init__(self):
        self.__dict__ = self.__shared_state

    def createStartMenuShortcut(self, description, executable, workingDir, startMenuSubdir="", iconLocation=None, createDesktopShortcut=False, putInStartup=False):
        '''Create a shortcut in the Start menu

        @type description: string
        @param description: The description of the shortcut.
        @type executable: string
        @param executable: The path in which the executable of the application is located.
        @type workingDir: string
        @param workingDir: The working folder of the application
        @type startMenuSubdir:  string
        @param startMenuSubdir: The name of the folder in the Start menu.
        @type iconLocation: string
        @param iconLocation: The folder in which the application icon is located.
        @type createDesktopShortcut: boolean
        @param createDesktopShortcut: Indicates if a shortcut must be put on the desktop.
        @type putInStartup: boolean
        @param putInStartup: Indicates if an application must be started with Windows.
        '''
        import pythoncom
        from win32com.shell import shell
        import os

        # Add shortcut to startmenu
        startmenu = self.getStartMenuProgramsPath()
        if not pylabs.q.system.fs.exists("%s\\%s" % (startmenu, startMenuSubdir)):
            pylabs.q.system.fs.createDir("%s\\%s" % (startmenu, startMenuSubdir))

        shortcut_startmenu = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut_startmenu.SetPath(executable)
        shortcut_startmenu.SetDescription(description)
        if not iconLocation is None:
            shortcut_startmenu.SetIconLocation(iconLocation, 0)
        shortcut_startmenu.SetWorkingDirectory(workingDir)
        shortcut_startmenu.QueryInterface(pythoncom.IID_IPersistFile).Save("%s\\%s\\%s.lnk" % (startmenu, startMenuSubdir, description), 0)

        if putInStartup:
            startupfolder = self.getStartupPath()
            if not pylabs.q.system.fs.exists(startupfolder):
                pylabs.q.system.fs.createDir(startupfolder)
            shortcut_startup = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
            shortcut_startup.SetPath(executable)
            shortcut_startup.SetDescription(description)
            if not iconLocation is None:
                shortcut_startup.SetIconLocation(iconLocation, 0)
            shortcut_startup.SetWorkingDirectory(workingDir)
            shortcut_startup.QueryInterface(pythoncom.IID_IPersistFile).Save("%s\\%s.lnk" % (startupfolder, description),0)

        if createDesktopShortcut:
            desktopfolder = self.getDesktopPath()
            shortcut_desktop = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
            shortcut_desktop.SetPath(executable)
            shortcut_desktop.SetDescription(description)
            if not iconLocation is None:
                shortcut_desktop.SetIconLocation(iconLocation, 0)
            shortcut_desktop.SetWorkingDirectory(workingDir)
            shortcut_desktop.QueryInterface(pythoncom.IID_IPersistFile).Save("%s\\%s.lnk" % (desktopfolder, description),0)

        pylabs.q.console.echo('Shortcuts created')

    def isNTFSVolume(self, driveletter):
        """Boolean indicating whether a volume is NTFS

        @param driveletter: The letter of the drive to check
        @type driveletter: string
        """

        # Strip away : / \
        while driveletter.endswith(":") or driveletter.endswith("\\") or driveletter.endswith("/"):
            driveletter = driveletter[:-1]
        if not len(driveletter) == 1:
            raise ValueError("Wrong parameter for WindowsSystem.isNTFSVolume: [%s] is not a valid drive letter." % driveletter)
        fTest = '%s:\\' % driveletter
        volumeInformation = win32api.GetVolumeInformation(fTest)
        fileSystem = volumeInformation[4]
        result = fileSystem == 'NTFS'
        return result

    def grantEveryoneFilePermission(self, dirpath, filepath=""):
        """Grant full control to the group I{Everyone} in this folder and all sub-folders

        This function grants full control to the Windows group I{Everyone} for files in the
        C{dirpath} its sub-folders.
        If a C{filepath} is specified, only the permissions of a specific file are updated.

        @type dirpath: string
        @param dirpath: The full path of the folder for which these permissions are set
        @type filepath: string
        @param filepath: The full path to a specific file.
        """

        # Execute command only on NTFS filesystem. Otherwise pass silently
        fullpath = os.path.abspath(dirpath)
        driveLetter = os.path.splitdrive(fullpath)[0]
        if not self.isNTFSVolume(driveLetter):
            pylabs.q.logger.log("Skipped file permissions update - filesystem for [%s] is not NTFS" % dirpath, 6)
            return

        def _grantFile(fileName, securityDescriptor):
            '''Set security on a file'''
            pylabs.q.logger.log("granting all access to everyone on %s" % fileName, 6)
            win32security.SetFileSecurity(fileName, win32security.DACL_SECURITY_INFORMATION, securityDescriptor)

        def _grantDir(dirpath, securityDescriptor):
            '''Set security on a folder'''
            for dir in pylabs.q.system.fs.listDirsInDir(dirpath):
                _grantDir(dir, securityDescriptor)
            for file in pylabs.q.system.fs.listFilesInDir(dirpath):
                _grantFile(file, securityDescriptor)
            win32security.SetFileSecurity(dirpath, win32security.DACL_SECURITY_INFORMATION, securityDescriptor)

        # create the security descriptor
        sd = win32security.SECURITY_DESCRIPTOR()
        # fill it:
        everyone = win32security.ConvertStringSidToSid('S-1-1-0')
        acl = win32security.ACL(128)
        acl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, everyone)
        sd.SetSecurityDescriptorDacl(1, acl, 0)

        if filepath == "":# it's a dir
            _grantDir(dirpath, sd)
        else:
            _grantFile(os.path.join(dirpath, filepath), sd)



    _isVistaUACEnabled = None
    def isVistaUACEnabled(self):
        """
        Return boolean indicating whether this is a Windows Vista system with
        User Account Control enabled.

        Warning: If modifies the UAC setting but has not yet rebooted,
        this method will return the wrong result.
        """

        if self._isVistaUACEnabled != None:
            return self._isVistaUACEnabled

        if self.getWindowsVersion() != self.VERSION_VISTA:
            return False
        hkey = reg.HKEY_LOCAL_MACHINE
        key = 'Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System'
        value = 'EnableLUA'
        if not self.registryHasValue(hkey, key, value):
            self._isVistaUACEnabled = False
        elif self.getValueFromRegKey(hkey, key, value)==0:
            self._isVistaUACEnabled = False
        else:
            self._isVistaUACEnabled = True
        return self._isVistaUACEnabled

    _userIsAdministrator = None
    def userIsAdministrator(self):
        '''Verifies if the logged on user has administrative rights'''
        if self._userIsAdministrator != None:
            return self._userIsAdministrator
        import win32net, win32netcon
        username = win32api.GetUserName()
        privileges = win32net.NetUserGetInfo(None, username, 1)
        if privileges['priv'] == win32netcon.USER_PRIV_ADMIN:
            self._userIsAdministrator = True
        else:
            self._userIsAdministrator = False
        return self._userIsAdministrator

    def getAppDataPath(self):
        """ Returns the windows "APPDATA" folder in Unicode format. """
        # We retrieve the APPDATA path using the WinAPI in Unicode format.
        # We could read the environment variable "APPDATA" instead, but this variable is encoded in a DOS-style characterset (called "CodePage") depending on the system locale. It's difficult to handle this encoding correctly in Python.
        return shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + os.sep # See http://msdn2.microsoft.com/en-us/library/bb762181(VS.85).aspx for information about this function.

    def getLocalAppDataPath(self):
        """ Returns the windows "APPDATA" folder in Unicode format. """
        # We retrieve the APPDATA path using the WinAPI in Unicode format.
        # We could read the environment variable "APPDATA" instead, but this variable is encoded in a DOS-style characterset (called "CodePage") depending on the system locale. It's difficult to handle this encoding correctly in Python.
        return shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, 0, 0) + os.sep # See http://msdn2.microsoft.com/en-us/library/bb762181(VS.85).aspx for information about this function.

    def getStartMenuProgramsPath(self):
        """ Returns the windows "START MENU/PROGRAMS" folder in Unicode format. """
        return shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, 0, 0) + os.sep # See http://msdn2.microsoft.com/en-us/library/bb762181(VS.85).aspx for information about this function.

    def getStartupPath(self):
        """ Returns the windows "START MENU/STARTUP" folder in Unicode format. """
        return shell.SHGetFolderPath(0, shellcon.CSIDL_STARTUP, 0, 0) + os.sep # See http://msdn2.microsoft.com/en-us/library/bb762181(VS.85).aspx for information about this function.

    def getDesktopPath(self):
        """ Returns the windows "DESKTOP" folder in Unicode format. """
        return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0) + os.sep # See http://msdn2.microsoft.com/en-us/library/bb762181(VS.85).aspx for information about this function.

    def _getHiveAndKey(self, fullKey):
        '''Split a windows registry key in two parts: the hive (hkey) and the registry key
        Eg: "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion" will return: (_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion")
        '''
        str_hkey, str_key = fullKey.split('\\', 1)
        hiveType = WinRegHiveType.getByName(str_hkey.lower())
        return hiveType.hive, str_key

    def _addValuesRecursively(self, regfile, fullKey):
        '''Recursively add all values and subkeys of a given registry key to an IniFile object
        '''
        regfile.addSection(fullKey)
        values = self.enumRegKeyValues(fullKey)
        for value in values: # Add all values from current key
            paramName = "\"%s\""%(value[0])
            paramType = value[2]
            if paramType.exportPrefix:
                paramValue = "%s:%s"%(paramType.exportPrefix, value[1])
            else:
                paramValue = "\"%s\""%(value[1])
            regfile.addParam(fullKey, paramName, paramValue)
        subkeys = self.enumRegKeySubkeys(fullKey)
        for subkey in subkeys: # Recursively go through all subkeys
            self._addValuesRecursively(regfile, "%s\\%s"%(fullKey, subkey))
        regfile.write()

    def importRegKeysFromString(self, string):
        """Imports windows registry keys from a string

        @param string: The string that holds the registry information (Should be in format returned by exportRegKeysToString())
        @type string: string
        """
        strBuffer = StringIO()
        strBuffer.write(string)
        strBuffer.seek(0)
        regfile = IniFile(strBuffer)
        sections = regfile.getSections()
        for section in sections:
            params = regfile.getParams(section)
            for param in params:
                value = regfile.getValue(section, param, True)
                param = param[1:-1] #Remove leading and trailing quote
                valueType = None
                if not value.startswith('"'):
                    prefix, value = value.split(':', 1)
                    valueType = WinRegValueType.findByExportPrefix(prefix)
                    if valueType == WinRegValueType.MULTI_STRING:
                        #convert string representation of an array to a real array
                        value = [eval(item) for item in value[1:-1].split(',')]
                    elif valueType == WinRegValueType.DWORD:
                        value = int(value)
                else:
                    valueType = WinRegValueType.STRING
                    value = value[1:-1] #Remove leading and trailing quote

                # Write the value to the registry
                q.logger.log("Adding '%s' to registry in key '%s' with value '%s' and type '%s'"%(param, section, value, valueType), 6)
                self.setValueFromRegKey(section, param, value, valueType)

    def importRegKeysFromFile(self, path):
        """Imports windows registry keys from a file

        @param path: The path of the file to import
        @type path: string
        """

        fileContent = pylabs.q.system.fs.fileGetContents(path)
        self.importRegKeysFromString(fileContent)

    def exportRegKeysToString(self, key):
        """Exports Windows registry key to a string

        This function exports a Windows registry key to a string (ini-file format).

        @param key: The registry key to export. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        """
        strBuffer = StringIO()
        regfile = IniFile(strBuffer)
        self._addValuesRecursively(regfile, key)
        return regfile.getContent()

    def exportRegKeysToFile(self, key, path):
        """Exports Windows registry key to a file

        This function exports a Windows registry key to an ini-file.

        @param key: The registry key to export. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string

        @param path: The path of the file to export to
        @type path: string
        """
        pylabs.q.system.fs.writeFile(path, self.exportRegKeysToString(key))

    def registryHasKey(self, key):
        """Check if the windows registry has the specified key

        @param key: The registry key to check. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        """
        try:
            hkey, key = self._getHiveAndKey(key)
            aReg = reg.ConnectRegistry(None, hkey)
            aKey = reg.OpenKey(aReg, key)
            return True
        except EnvironmentError:
            return False

    def registryHasValue(self, key, valueName):
        """Check if a certain key in the windows registry has a specified value

        @param key: The registry key to check. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        @param valueName: The name of the value to check for
        @type valueName: string

        """
        try:
            hkey, key = self._getHiveAndKey(key)
            self.getValueFromKey(hkey, key, valueName)
            return True
        except EnvironmentError:
            return False

    def enumRegKeyValues(self, key):
        """List all values of a specified key in the windows registry

        @param key: The registry key to check. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string

        @return: An array of tupples containing the name of each value, the data of the value and it's type
        @rtype: tupple(string, WinRegValueType)
        """
        hkey, key = self._getHiveAndKey(key)
        aReg = reg.ConnectRegistry(None, hkey)
        aKey = reg.OpenKey(aReg, key)
        result = []
        index = 0

        # The function EnumValue() retrieves the name of one subkey each time it is called.
        # It is typically called repeatedly, until an EnvironmentError exception
        # is raised, indicating no more values.
        while True:
            try:
                valueName, valueData, valueType = reg.EnumValue(aKey, index)
                result.append((valueName, valueData, WinRegValueType.findByIntegerValue(valueType)))
                index += 1
            except EnvironmentError:
                return result

    def enumRegKeySubkeys(self, key):
        """List all sub-keys of a specified key in the windows registry

        @param key: The registry key to check. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        """
        hkey, key = self._getHiveAndKey(key)
        aReg = reg.ConnectRegistry(None, hkey)
        aKey = reg.OpenKey(aReg, key)
        result=[]
        index=0

        # The function EnumKey() retrieves the name of one subkey each time it is called.
        # It is typically called repeatedly, until an EnvironmentError exception
        # is raised, indicating no more values.
        while True:
            try:
                subkey = reg.EnumKey(aKey, index)
                result.append(subkey)
                index += 1
            except EnvironmentError:
                return result

    def getValueFromRegKey(self, key, valueName):
        """Retrieves a value for a key

        @param key: The registry key that holds the value to get. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        @param valueName: The name of the value to retrieve
        @type valueName: string
        @return: A tupple containing the data of the value with the specified name and it's type
        @rtype: tupple(string, WinRegValueType)
        """
        hkey, key = self._getHiveAndKey(key)
        aReg = reg.ConnectRegistry(None, hkey)
        aKey = reg.OpenKey(aReg, key)
        value, int_type = reg.QueryValueEx(aKey, valueName)
        return value, WinRegValueType.findByIntegerValue(int_type)

    def deleteRegKey(self, key):
        """Deletes a key from the Windows Registry

        @param key: The registry key that should be deleted. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        """
        hkey, key = self._getHiveAndKey(key)
        aReg = reg.ConnectRegistry(None, hkey)
        reg.DeleteKey(aReg, key)

    def setValueFromRegKey(self, key, valueName, valueData, valueType):
        """Sets a value in a key

        @param key: The registry key that holds the value to set. If the key does not exist, it will be created. The key should include the section. Eg. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
        @type key: string
        @param valueName: The name of the value to set
        @type valueName: string
        @param valueData: The data to assign to the value
        @type valueData: string
        @param valueType: The type of the value
        @type valueType: WinRegValueType
        """
        hkey, key = self._getHiveAndKey(key)
        aReg = reg.ConnectRegistry(None, hkey)
        aKey = reg.CreateKey(aReg, key)
        reg.SetValueEx(aKey, valueName, 0, valueType.type, valueData)

    def addSystemUser(self, userName, password=None):
        """
        Add a system user
        @param userName: name of the user to add
        @param passwd(optional): password of the user
        raise an exception if user already exists
        """
        pylabs.q.logger.log('Adding system user %s'%userName, 6)

        if self.isSystemUser(userName):
            raise ValueError('User %s Already Exist'%userName)

        userDict = {}
        userDict ['name'] = userName

        if password != None:
            userDict['password'] = password

        userDict['priv'] = win32netcon.USER_PRIV_USER

        win32net.NetUserAdd(None, 1, userDict)

        if self.isSystemUser(userName):

            pylabs.q.logger.log('User %s Added successfully'%userName)

    def isSystemUser(self, userName):
        """
        Check if user is valid system User
        @param userName: name of the user
        """
        pylabs.q.logger.log('Checking if user %s exists'%userName, 6)

        if userName in self.listSystemUsers():
            pylabs.q.logger.log('User %s exists'%userName, 6)

            return True

        pylabs.q.logger.log('User %s doesnt exist'%userName, 6)

        return False

    def listSystemUsers (self):
        """
        List system users
        @return: list of system user names
        """
        pylabs.q.logger.log('Listing System Users', 6)

        users = [entry['name'] for entry in win32net.NetUserEnum(None, 0)[0]]

        return users

    def deleteSystemUser(self, userName):
        """
        Delete a system user
        @param userName: name of the user to delete
        """
        pylabs.q.logger.log('Deleting User %s'%userName, 6)

        if self.isSystemUser(userName):
            win32net.NetUserDel(None, userName)

            if not self.isSystemUser(userName):
                pylabs.q.logger.log('User %s deleted successfully'%userName, 6)

                return True

            pylabs.q.logger.log('Failed to delete user %s'%userName, 6)

        else:
            raise RuntimeError("User %s is not a system user"%userName)

    def getSystemUserSid(self, userName):
        """
        Get user security identifier
        @param userName: name of the system user
        @return: security identifier of the user
        @rtype: string
        """
        pylabs.q.logger.log('Getting User %s\'s SID'%userName, 6)

        if self.isSystemUser(userName) or userName == 'everyone':

            info = win32security.LookupAccountName(None, userName)
            pySid = info[0]
            sid = win32security.ConvertSidToStringSid(pySid)

            pylabs.q.logger.log('User\'s SID is %s'%str(sid), 6)

            return sid

        else:
            raise RuntimeError('Failed to Get User %s\'s SID'%userName)

    def createService(self, serviceName, displayName, binPath, args=None):
        """
        Create a service
        @param serviceName: name of the service
        @param displayName: display name of the service
        @param binPath: path to the executable file of the service (has to be an existing file)
        @param args(optional): arguments to the executable file
        e.g creating a service for postgresql
        serviceName = 'pgsql-8.3'
        displayName = serviceName
        binDir = q.system.fs.joinPaths(q.dirs.baseDir, 'apps','postgresql8', 'bin')
        pgDataDir = q.system.fs.joinPathsq.dirs.baseDir, 'apps','postgresql8', 'Data')
        q.system.windows.createService(serviceName, displayName , '%s\\pg_ctl.exe','runservice -W -N %s -D %s'%(serviceName, pgDataDir))
        """
        pylabs.q.logger.log('Creating Service %s'%serviceName, 6)

        if not pylabs.q.system.fs.isFile(binPath):
            raise ValueError('binPath %s is not a valid file'%binPath)

        executableString = binPath

        if args != None:
            executableString = "%s %s"%(executableString, args)

        """
        Open an sc handle to use for creating a service
        @param machineName: The name of the computer, or None
        @param dbName: The name of the service database, or None
        @param desiredAccess: The access desired
        @return: a handle to the service control manager
        """
        hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

        try:
            """
            Create Service
            @param scHandle: handle to service control manager database
            @param name: Name of service
            @param displayName: Display name
            @param desiredAccess: type of access to service
            @param serviceType: type of service
            @param startType: When/how to start service
            @param errorControl: severity if service fails to start
            @param binaryFile: name of binary file
            @param loadOrderGroup: name of load ordering group , or None
            @param bFetchTag: Should the tag be fetched and returned? If TRUE, the result is a tuple of (handle, tag), otherwise just handle.
            @param serviceDeps: sequence of dependency names
            @param acctName: account name of service, or None
            @param password: password for service account , or None
            """
            hs = win32service.CreateService(hscm, serviceName, displayName, win32service.SERVICE_ALL_ACCESS, \
                                            win32service.SERVICE_WIN32_OWN_PROCESS, win32service.SERVICE_DEMAND_START, \
                                            win32service.SERVICE_ERROR_NORMAL, executableString, None, \
                                            0, None, None, None)

            win32service.CloseServiceHandle(hs)

        finally:
            win32service.CloseServiceHandle(hscm)

        if self.isServiceInstalled(serviceName):
            pylabs.q.logger.log('Service %s Created Successfully'%serviceName, 6)
            return True

    def removeService(self, serviceName):
        """
        Remove Service
        Stops the service then starts to remove it
        @param serviceName: name of the service to remove
        """
        if self.isServiceRunning(serviceName):
            self.stopService(serviceName)

        hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

        serviceHandler = win32service.OpenService(hscm, serviceName, win32service.SERVICE_ALL_ACCESS)

        win32service.DeleteService(serviceHandler)

        win32service.CloseServiceHandle(serviceHandler)

        if not self.isServiceInstalled(serviceName):
            pylabs.q.logger.log('Service %s removed Successfully'%serviceName, 6)

            return True

    def isServiceRunning(self, serviceName):
        """
        Check if service is running

        @return: True if service is running
        @rtype: boolean
        """
        isRunning =  win32serviceutil.QueryServiceStatus(serviceName)[1] == win32service.SERVICE_RUNNING
        pylabs.q.logger.log('Service %s isRunning = %s'%(serviceName, isRunning), 3)

        return isRunning


    def isServiceInstalled(self, serviceName):
        """
        Check if service is installed
        @rtype: boolean
        """
        pylabs.q.logger.log('Checking if service %s is installed'%serviceName, 6)

        if serviceName in self.listServices():

            pylabs.q.logger.log('Service %s is installed'%serviceName, 6)

            return True

        pylabs.q.logger.log('Service %s is not installed'%serviceName, 6)

        return False

    def listServices(self):
        """
        List all services installed
        @return: list of service names installed
        """
        pylabs.q.logger.log('Listing services installed', 6)

        services = self._wmi.InstancesOf('Win32_Service')
        serviceNames = [service.Properties_('Name').Value for service in services]

        return serviceNames

    def startService(self, serviceName):
        """
        Start a service.

        @param serviceName: name of the service to start
        @return: True if service started successfully
        @rtype: boolean
        """
        if not self.isServiceRunning(serviceName):
            win32serviceutil.StartService(serviceName)

            time.sleep(1)

            if self.isServiceRunning(serviceName):
                return True

            pylabs.q.logger.log('Failed to start service %s '%serviceName, 1)

        else:
            pylabs.q.logger.log('Service %s is already running'%serviceName, 1)

        return False

    def stopService(self, serviceName):
        """
        Stop a service.

        @param serviceName: name of the service to stop
        @return: True if service stopped successfully
        @rtype: boolean
        Checks if service is running then tries to the service.
        """
        if self.isServiceRunning(serviceName):
            win32serviceutil.StopService(serviceName)

            if not self.isServiceRunning(serviceName):

                return True

            pylabs.q.logger.log('Failed to stop service %s'%serviceName, 1)

        else:
            pylabs.q.logger.log('Service %s is not running'%serviceName, 1)

    def listRunningProcessesIds(self):
        """
        List Running Processes Ids
        @return: list of running processes ids
        """
        pylabs.q.logger.log('Listing Running Processes ids', 6)

        runningProcesses = win32process.EnumProcesses()

        return runningProcesses

    def listRunningProcesses(self):
        """
        List Running Processes names
        @return: list of running processes names
        """
        pylabs.q.logger.log('Listing Running processes names', 6)

        processes = self._wmi.InstancesOf('Win32_Process')
        processesNames = [process.Properties_('Name').Value for process in processes]

        return processesNames

    def isPidAlive(self, pid):
        """
        Checking if Pid is Still Alive
        @param pid: process id to check
        @type: int
        @rtype: boolean
        """
        pylabs.q.logger.log('Checking if pid %s is alive'%pid, 6)

        if pid in self.listRunningProcessesIds():
            pylabs.q.logger.log('Pid %s is alive'%pid, 6)

            return True

        pylabs.q.logger.log('Pid %s is not alive'%pid, 6)

        return False

    def getPidOfProcess(self, process):
        """
        Retreive the pid of a process
        @param pid: process name
        @type: string
        @return: the pid (or None if Failed)
        @rtype: int
        """
        pylabs.q.logger.log('Retreiving the pid of process %s'%process, 6)

        processInfo = self._wmi.ExecQuery('select * from Win32_Process where Name="%s"'%process)

        if len(processInfo) > 0:
            pid = processInfo[0].Properties_('ProcessId').Value
            pylabs.q.logger.log('Process %s\'s id is %d'%(process, pid), 6)

            return pid

        pylabs.q.logger.log('Failed to retreive the pid of process'%process, 6)

        return None

    def checkProcess(self, process, min=1):
        """
        Check if a certain process is running on the system.
        you can specify minimal running processes needed.

        @param process: String with the name of the process we are trying to check
        @param min: (int) minimal threads that should run.
        @return status: (int) when ok, 1 when not ok.
        """
        processInfo = self._wmi.ExecQuery('select * from Win32_Process where Name="%s"'%process)

        if len(processInfo) >= min:
            pylabs.q.logger.log('Process %s is running with %d threads'%(process, min), 6)
            return 0

        elif len(processInfo)  == 0:
            pylabs.q.logger.log('Process %s is not running'%(process), 6)

        else:
            pylabs.q.logger.log('Process %s is running with %d thread(s)'%(process, len(processInfo)), 6)

        return 1

    def checkProcessForPid(self, process, pid):
        """
        Check whether a given pid actually does belong to a given process name.
        @param pid: (int) the pid to check
        @param process: (str) the process that should have the pid
        @return status: (int) 0 when ok, 1 when not ok.
        """
        pylabs.q.logger.log('Check if process %s\'s Id is %d'%(process, pid), 6)

        processInfo = self._wmi.ExecQuery('select * from Win32_Process where Name="%s"'%process)

        if len(processInfo) > 0:
            processesIds = [process.Properties_('ProcessId').Value for process in processInfo]

            for processId in processesIds:

                if processId == pid:
                    return 0

        pylabs.q.logger.log('Process %s\'s Id is %d and not %d'%(process, processId, pid), 6)

        return 1

    def getFileACL(self, filePath):
        """
        Get Access Control List of a file/directory
        @return: PyACL object
        """
        info = win32security.DACL_SECURITY_INFORMATION
        sd = win32security.GetFileSecurity(filePath, info)
        acl = sd.GetSecurityDescriptorDacl()

        return acl

    def grantAccessToDirTree(self,  dirPath, userName='everyone'):
        """
        Allow Permission to userName on a directory tree
        Adds permission to parentDir the walks through all subdirectories and add permissions

        @param dir: path of the dir
        @param userName: name of the user to add to the acl of the dir tree
        """
        pylabs.q.logger.log('Granting access to Dir Tree %s'%dirPath, 6)

        if pylabs.q.system.fs.isDir(dirPath):
            self.grantAccessToFile(dirPath, userName)

            for subDir in pylabs.q.system.fs.WalkExtended(dirPath, recurse=1):
                self.grantAccessToFile(subDir, userName)
        else:
            pylabs.q.logger.log('%s is not a valid directory'%dirPath, 6)
            raise IOError('Directory %s does not exist'%dirPath)

    def grantAccessToFile(self, filePath, userName='everyone'):
        """
        Allow Permission to userName on a file/directory
        @param file: path of the file/dir
        @param userName: name of the user to add to the acl of the file/dir
        """
        pylabs.q.logger.log('Granting access to file %s'%filePath, 6)

        if pylabs.q.system.fs.isFile(filePath) or pylabs.q.system.fs.isDir(filePath):

            info = win32security.DACL_SECURITY_INFORMATION
            sd = win32security.GetFileSecurity(filePath, info)
            acl = self.getFileACL(filePath)
            user, domain, acType = win32security.LookupAccountName ("", userName)

            acl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | con.FILE_DELETE_CHILD | con.DELETE | win32file.FILE_SHARE_DELETE, user)
            sd.SetSecurityDescriptorDacl(1, acl, 0)
            win32security.SetFileSecurity (filePath, win32security.DACL_SECURITY_INFORMATION, sd)

        else:
            pylabs.q.logger.log('File/Directory %s is not valid'%filePath, 6)

            raise IOError('FilePath %s does not exist'%filePath)
    def pm_removeDirTree(self, dirPath, force = False, errorHandler = None):
        """
        Recusrively removes files and folders from a given path
        @param dirPath: path of the dir
        @param force: boolean parameter indicating that folders containing hidden files will also be deleted
        """
        if(pylabs.q.system.fs.exists(dirPath)):
            if pylabs.q.system.fs.isDir(dirPath):
                if force:
                    fileMode = win32file.GetFileAttributesW(dirPath)
                    for file in pylabs.q.system.fs.Walk(dirPath,recurse=1):
                        pylabs.q.logger.log('Changing attributes on %s'%file)
                        win32file.SetFileAttributesW(file, fileMode &  ~win32file.FILE_ATTRIBUTE_HIDDEN)
                if errorHandler != None:
                    shutil.rmtree(dirPath, onerror = errorHandler)
                else:
                    shutil.rmtree(dirPath)
            else:
                raise ValueError("Specified path: %s is not a Directory in System.removeDirTree"% dirPath)