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
from pylabs.Shell import *
import sys
import os
import os.path
import hashlib
import re
import fnmatch
import time
import shutil
import errno
import tempfile
import codecs
import cPickle as pickle
from stat import ST_MTIME


# We import only pylabs as the q.system.fs is used before pylabs is initialized. Thus the q cannot be imported yet

import pylabs
from pylabs.decorators import deprecated

# We do not use the q.platform here nor do we import the PlatformType as this would
# lead to circular imports and raise an exception

if not sys.platform.startswith('win'):
    try:
        import fcntl
    except ImportError:
        pass

_LOCKDICTIONARY = dict()

class LockException(Exception):
    def __init__(self, message='Failed to get lock', innerException=None):
        if innerException:
            message += '\nProblem caused by:\n%s' % innerException
        Exception.__init__(self, message)
        self.innerException = innerException

class LockTimeoutException(LockException):
    def __init__(self, message='Lock request timed out', innerException=None):
        LockException.__init__(self, message, innerException)

class Exceptions:
    LockException = LockException
    LockTimeoutException = LockTimeoutException


def cleanupString(string, replacewith="_", regex="([^A-Za-z0-9])"):
    '''Remove all non-numeric or alphanumeric characters'''
    # Please don't use the logging system here. The logging system
    # needs this method, using the logging system here would
    # introduce a circular dependency. Be careful not to call other
    # functions that use the logging system.
    return re.sub(regex, replacewith, string)

def lock(lockname, locktimeout=60):
    '''Take a system-wide interprocess exclusive lock. Default timeout is 60 seconds'''
    pylabs.q.logger.log('Lock with name: %s'% lockname,6)
    try:
        result = lock_(lockname, locktimeout)
    except Exception, e:
        raise LockException(innerException=e)
    else:
        if not result:
            raise LockTimeoutException(message="Cannot acquire lock [%s]" % (lockname))
        else:
            return result

def lock_(lockname, locktimeout=60):
    '''Take a system-wide interprocess exclusive lock.

    Works similar to q.system.fs.lock but uses return values to denote lock
    success instead of raising fatal errors.

    This refactoring was mainly done to make the lock implementation easier
    to unit-test.
    '''
    #TODO This no longer uses fnctl on Unix, why?
    LOCKPATH = os.path.join(pylabs.q.dirs.tmpDir, 'run')
    lockfile = os.path.join(LOCKPATH, cleanupString(lockname))

    if not islocked(lockname):
        if not pylabs.q.system.fs.exists(LOCKPATH):
            pylabs.q.system.fs.createDir(LOCKPATH)

        pylabs.q.system.fs.writeFile(lockfile, str(os.getpid()))
        return True
    else:
        locked = False
        for i in xrange(locktimeout + 1):
            locked = islocked(lockname)
            if not locked:
                break
            else:
                pylabs.q.console.echo('waiting for lock... (%s)'%i)
                time.sleep(1)

        if not locked:
            return lock_(lockname)
        else:
            return False

def islocked(lockname):
    '''Check if a system-wide interprocess exclusive lock is set'''
    isLocked = True
    LOCKPATH = os.path.join(pylabs.q.dirs.tmpDir, 'run')
    lockfile = os.path.join(LOCKPATH, cleanupString(lockname))

    try:
        # read the pid from the lockfile
        if pylabs.q.system.fs.exists(lockfile):
            pid = open(lockfile,'rb').read()
        else:
            return False

    except (OSError, IOError), e:
        # failed to read the lockfile
        if e.errno != errno.ENOENT: # exception is not 'file or directory not found' -> file probably locked
            raise
    else:
        # open succeeded without exceptions, continue
        # check if a process with pid is still running
        if pylabs.q.system.fs.exists(lockfile) and (not pid or not (pid.isdigit() and pylabs.q.system.process.isPidAlive(int(pid)))):
            #cleanup system, pid not active, remove the lockfile
            pylabs.q.system.fs.removeFile(lockfile)
            isLocked = False

    return isLocked

def unlock(lockname):
    """Unlock system-wide interprocess lock"""
    pylabs.q.logger.log('UNLock with name: %s'% lockname,6)
    try:
        unlock_(lockname)
    except Exception, msg:
        raise RuntimeError("Cannot unlock [%s] with ERROR: %s" % (lockname, str(msg)))

def unlock_(lockname):
    '''Unlock system-wide interprocess lock

    Works similar to q.system.fs.unlock but uses return values to denote unlock
    success instead of raising fatal errors.

    This refactoring was mainly done to make the lock implementation easier
    to unit-test.
    '''
    LOCKPATH = os.path.join(pylabs.q.dirs.tmpDir, 'run')
    lockfile = os.path.join(LOCKPATH, cleanupString(lockname))

    # read the pid from the lockfile
    if pylabs.q.system.fs.exists(lockfile):
        try:
            pid = open(lockfile,'rb').read()
        except:
            return
        if int(pid) != os.getpid():
            pylabs.q.errorconditionhandler.raiseWarning("Lock %r not owned by this process" %lockname)
            return

        pylabs.q.system.fs.removeFile(lockfile)
    else:
        pylabs.q.console.echo("Lock %r not found"%lockname)


class FileLock(object):
    '''Context manager for file-based locks

    Context managers were introduced in Python 2.5, see the documentation on the
    'with' statement for more information:

     * http://www.python.org/dev/peps/pep-0343/
     * http://pyref.infogami.com/with

    @see: L{lock}
    @see: L{unlock}
    '''
    def __init__(self, lock_name):
        self.lock_name = lock_name

    def __enter__(self):
        lock(self.lock_name)

    def __exit__(self, *exc_info):
        unlock(self.lock_name)


class SystemFS:
    exceptions = Exceptions

    def copyFile(self, fileFrom, to ):
        """Copy file

        Copies the file from C{fileFrom} to the file or directory C{to}.
        If C{to} is a directory, a file with the same basename as C{fileFrom} is
        created (or overwritten) in the directory specified.
        Permission bits are copied.

        @param fileFrom: Source file path name
        @type fileFrom: string
        @param to: Destination file or folder path name
        @type to: string
        """
        pylabs.q.logger.log("Copy file from %s to %s" % (fileFrom,to),6)
        if ((fileFrom is None) or (to is None)):
            raise TypeError("No parameters given to system.fs.copyFile from %s, to %s" % (fileFrom, to))
        #try:
        if pylabs.q.system.fs.isFile(fileFrom):
            # Create target folder first, otherwise copy fails
            target_folder = os.path.dirname(to)
            self.createDir(target_folder)
            shutil.copy(fileFrom, to)
            return
        
        else:
            
            raise RuntimeError("Can not copy file, file: %s does not exist in system.fs.copyFile" % ( fileFrom ) )
        #except:
        #    raise RuntimeError("Failed to copy the file from %s to %s" % (fileFrom, to))

    def moveFile(self, source, destin):
        """Move a  File from source path to destination path
        @param source: string (Source file path)
        @param destination: string (Destination path the file should be moved to )
        """
        pylabs.q.logger.log('Move file from %s to %s'% (source, destin),6)
        if ((source is None) or (destin is None)):
            raise TypeError("Not enough parameters given to system.fs.moveFile: move from %s, to %s" % (source, destin))
        try:
            if(pylabs.q.system.fs.isFile(source)):
                pylabs.q.system.fs.move(source, destin)
            else:
                raise RuntimeError("The specified source path in system.fs.moveFile does not exist: %s" % source)
        except:
            raise RuntimeError("File could not be moved...in system.fs.moveFile: from %s to %s " % (source, destin))

    def renameFile(self, filePath, new_name):
        """Rename File
        @param filePath: string (Original file path)
        @param new_name: string (New file path)
        """
        pylabs.q.logger.log('Rename file of path: %s to new name: %s'%(filePath, new_name),6)
        if filePath == new_name:
            return
        if ((filePath is None) or (new_name is None)):
            #@todo samaa:1 : urgent check all traperrors on right syntax
            raise TypeError('Not enough parameters passed to system.fs.renameFile from %s to %s'% (filePath, new_name))
        try:
            if(pylabs.q.system.fs.exists(filePath)):
                if(pylabs.q.system.fs.isFile(filePath)):
                    os.rename(filePath, new_name)
                else:
                    raise RuntimeError("The specified Path specified in system.fs.renameFile is not a File: %s"% (filePath, new_name))
            else:
                raise RuntimeError("Path %s does not exist in system.fs.renameFile"% (filePath, new_name))
        except:
            raise RuntimeError("File could not be renamed from %s to %s"% (filePath, new_name))
            # raise RuntimeError("File could not be renamed from %s to %s"% (filePath, new_name))
            # don't hide the exception!

    def removeFile(self, path):
        """Remove a File
        @param path: string (File path required to be removed
        """
        pylabs.q.logger.log('Removing file with path: %s'%path,6)
        if path is None:
            raise TypeError('Not enough parameters passed to system.fs.removeFile: %s'%path)
        try:
            if(pylabs.q.system.fs.exists(path)):
                if(pylabs.q.system.fs.isFile(path)):
                    os.remove(path)
                    pylabs.q.logger.log('Done removing file with path: %s'%path)
                else:
                    raise RuntimeError("Path: %s is not a file in system.fs.removeFile"%path)
            else:
                raise RuntimeError("Path: %s does not exist in system.fs.removeFile"%path)
        except:
            raise RuntimeError("File with path: %s could not be removed\nDetails: %s"%(path, sys.exc_type))

    def remove(self, path,onlyIfExists=False):
        """Remove a File
        @param path: string (File path required to be removed
        """
        pylabs.q.logger.log('Removing file with path: %s'%path,6)
        if path is None:
            raise TypeError('Not enough parameters passed to system.fs.removeFile: %s'%path)
        if not pylabs.q.system.fs.exists(path):
            if onlyIfExists==False:
                raise RuntimeError("Path: %s does not exist in system.fs.removeFile"%path)
        else:
            try:
                os.remove(path)
                pylabs.q.logger.log('Done removing file with path: %s'%path)
            except:
                raise RuntimeError("File with path: %s could not be removed\nDetails: %s"%(path, sys.exc_type))

    def createEmptyFile(self, filename):
        """Create an empty file
        @param filename: string (file path name to be created)
        """
        pylabs.q.logger.log('creating an empty file with name & path: %s'%filename,9)
        if filename is None:
            raise ArithmeticError('Not enough parameters passed to system.fs.createEmptyFile: %s'%filename)
        try:
            open(filename, "w").close()
            pylabs.q.logger.log('Empty file %s has been successfully created'%filename)
        except Exception:
            raise RuntimeError("Failed to create an empty file with the specified filename: %s"%filename)

    def createDir(self, newdir):
        """Create new Directory
        @param newdir: string (Directory path/name)
        if newdir was only given as a directory name, the new directory will be created on the default path,
        if newdir was given as a complete path with the directory name, the new directory will be created in the specified path
        """
        pylabs.q.logger.log('Creating directory if not exists %s' % newdir.encode("utf-8"),8)
        if newdir == '' or newdir == None:
            raise TypeError('The newdir-parameter of system.fs.createDir() is None or an empty string.')
        try:
            if pylabs.q.system.fs.isDir(newdir):
                pylabs.q.logger.log('Directory trying to create: [%s] already exists'%newdir.encode("utf-8"),8)
                pass
            else:
                head, tail = os.path.split(newdir)
                if head and not pylabs.q.system.fs.isDir(head):
                    pylabs.q.system.fs.createDir(head)
                if tail:
                    try:
                        newDir = os.mkdir(newdir)
                    except OSError, e:
                        if e.errno != os.errno.EEXIST: #File exists
                            raise
                pylabs.q.logger.log('Created the directory [%s]' % newdir.encode("utf-8"),8)
        except:
            raise RuntimeError("Failed to create the directory [%s]" % newdir.encode("utf-8"))

    def copyDirTree(self, src, dst, keepsymlinks = False, overwriteDestination = False):
        """Recursively copy an entire directory tree rooted at src.
        The dst directory may already exist; if not,
        it will be created as well as missing parent directories
        @param src: string (source of directory tree to be copied)
        @param dst: string (path directory to be copied to...should not already exist)
        @param keepsymlinks: bool (True keeps symlinks instead of copying the content of the file)
        @param overwriteDestination: bool (Set to True if you want to overwrite destination first, be carefull, this can erase directories)
        """
        pylabs.q.logger.log('Copy directory tree from %s to %s'% (src, dst),6)
        if ((src is None) or (dst is None)):
            raise TypeError('Not enough parameters passed in system.fs.copyDirTree to copy directory from %s to %s '% (src, dst))
        if pylabs.q.system.fs.isDir(src):
            names = os.listdir(src)
            if not pylabs.q.system.fs.exists(dst):
                pylabs.q.system.fs.createDir(dst)
                    
            errors = []
            for name in names:
                srcname = pylabs.q.system.fs.joinPaths(src, name)
                dstname = pylabs.q.system.fs.joinPaths(dst, name)
                try:
                    if self.exists( dstname ):
                        if overwriteDestination :
                            if self.isDir( dstname , False ) : 
                                self.removeDirTree( dstname )
                            else :
                                self.unlink( dstname )
                        else :
                            # Only exception is if the destination and source both are directories
                            if not ( self.isDir( srcname , keepsymlinks) and self.isDir( dstname, False ) ) :
                                continue
                                
                            
                    if keepsymlinks and pylabs.q.system.fs.isLink(srcname):
                        linkto = pylabs.q.system.fs.readlink(srcname)
                        pylabs.q.system.fs.symlink(linkto, dstname, overwriteDestination)
                    elif pylabs.q.system.fs.isDir(srcname):
                        pylabs.q.system.fs.copyDirTree(srcname, dstname, keepsymlinks, overwriteDestination)
                    else:
                        shutil.copy2(srcname, dstname)
                       
                    # XXX What about devices, sockets etc.?
                except (IOError, os.error), why:
                    errors.append((srcname, dstname, why))
                # catch the Error from the recursive copytree so that we can
                # continue with other files
                #except Error, err:
                    #   errors.extend(err.args[0])
            if errors:
                raise Exception (errors)
        else:
            raise RuntimeError('Source path %s in system.fs.copyDirTree is not a directory'% src)

    def removeDirTree(self, path, onlyLogWarningOnRemoveError = False):
        """Recursively delete a directory tree.
            @param path: the path to be removed
        """
        pylabs.q.logger.log('Removing directory tree with path: %s'%path,6)
        if path is None:
            raise ValueError('Path is None in system.fs.removeDir')
        try:
            if(pylabs.q.system.fs.exists(path)):
                if(self.isDir(path)):
                    if onlyLogWarningOnRemoveError:
                        def errorHandler(shutilFunc, shutilPath, shutilExc_info):
                            pylabs.q.logger.log('WARNING: could not remove %s while recursively deleting %s' % (shutilPath, path), 2)
                        if pylabs.q.platform.isWindows():
                            pylabs.q.system.windows.pm_removeDirTree(path, True, errorHandler)
                        else:
                            pylabs.q.logger.log('Trying to remove Directory tree with path: %s (warn on errors)'%path)
                            shutil.rmtree(path, onerror = errorHandler)
                    else:
                        if pylabs.q.platform.isWindows():
                            pylabs.q.system.windows.pm_removeDirTree(path, True)
                        else:
                            pylabs.q.logger.log('Trying to remove Directory tree with path: %s'%path)
                            shutil.rmtree(path)

                    pylabs.q.logger.log('Directory tree with path: %s is successfully removed'%path)
                else:
                    raise ValueError("Specified path: %s is not a Directory in system.fs.removeDirTree"%path)
        except Exception, e:
            raise RuntimeError("Failed to remove the directory: %(path)s. ERROR : %(error)s"%{"path":path,"error":e})

    def removeDir(self, path):
        """Remove a Directory
        @param path: string (Directory path that should be removed)
        """
        pylabs.q.logger.log('Removing the directory with path: %s'%path,6)
        if path is None:
            raise TypeError('Path is None in system.fs.removeDir')
        try:
            if(pylabs.q.system.fs.exists(path)):
                if(pylabs.q.system.fs.isDir(path)):
                    os.rmdir(path)
                    pylabs.q.logger.log('Directory with path: %s is successfully removed'%path)
                else:
                    raise ValueError("Path: %s is not a Directory in system.fs.removeDir"% path)
            else:
                raise RuntimeError("Path: %s does not exist in system.fs.removeDir"% path)
        except:
            raise RuntimeError("Failed to remove the directory: %s"% path)

    def changeDir(self, path):
        """Changes Current Directory
        @param path: string (Directory path to be changed to)
        """
        pylabs.q.logger.log('Changing directory to: %s'%path,6)
        if path is None:
            raise TypeError('Path is not given in system.fs.changeDir')
        try:
            if(pylabs.q.system.fs.exists(path)):
                if(pylabs.q.system.fs.isDir(path)):
                    os.chdir(path)
                    newcurrentPath = os.getcwd()
                    pylabs.q.logger.log('Directory successfully changed to %s'%path)
                    return newcurrentPath
                else:
                    raise ValueError("Path: %s in system.fs.changeDir is not a Directory"% path)
            else:
                raise RuntimeError("Path: %s in system.fs.changeDir does not exist"% path)
        except:
            raise RuntimeError("Could not change current working directory to this directory: %s"% path)

    def moveDir(self, source, destin):
        """Move Directory from source to destination
        @param source: string (Source path where the directory should be removed from)
        @param destin: string (Destination path where the directory should be moved into)
        """
        pylabs.q.logger.log('Moving directory from %s to %s'% (source, destin),6)
        if ((source is None) or (destin is None)):
            raise TypeError('Not enough passed parameters to moveDirectory from %s to %s in system.fs.moveDir '% (source, destin))
        try:
            if(pylabs.q.system.fs.isDir(source)):
                pylabs.q.system.fs.move(source, destin)
                pylabs.q.logger.log('Directory is successfully moved from %s to %s'% (source, destin))
            else:
                raise RuntimeError("Specified Source path: %s does not exist in system.fs.moveDir"% source)
        except:
            raise RuntimeError("Directory could not be moved from %s to %s"% (source, destin))

    def joinPaths(self,*args):
        """Join one or more path components.
        If any component is an absolute path, all previous components are thrown away, and joining continues.
        @param path1: string
        @param path2: string
        @param path3: string
        @param .... : string
        @rtype: Concatenation of path1, and optionally path2, etc...,
        with exactly one directory separator (os.sep) inserted between components, unless path2 is empty.
        """
        pylabs.q.logger.log('Join paths %s'%(str(args)),9)
        if args is None:
            raise TypeError('Not enough parameters %s'%(str(args)))
        try:
            return os.path.join(*args)
        except:
            raise RuntimeError('Failed to join paths: %s'%(str(args)))

    def getDirName(self, path,lastOnly=False,levelsUp=None):
        """
        Return a directory name from pathname path.
        @param path the path to find a directory within
        @param lastOnly means only the last part of the path which is a dir (overrides levelsUp to 0)
        @param levelsUp means, return the parent dir levelsUp levels up
         e.g. ...getDirName("/opt/qbase/bin/something/test.py", levelsUp=0) would return something
         e.g. ...getDirName("/opt/qbase/bin/something/test.py", levelsUp=1) would return bin
         e.g. ...getDirName("/opt/qbase/bin/something/test.py", levelsUp=10) would raise an error
        """
        pylabs.q.logger.log('Get directory name of path: %s' % path,9)
        if path is None:
            raise TypeError('Path is not passed in system.fs.getDirName')
        #try:
        dname=os.path.dirname(path)
        dname=dname.replace("/",os.sep)
        dname=dname.replace("//",os.sep)
        dname=dname.replace("\\",os.sep)
        if lastOnly:
            dname=dname.split(os.sep)[-1]
            return dname
        if levelsUp<>None:
            parts=dname.split(os.sep)
            if len(parts)-levelsUp>0:
                return parts[len(parts)-levelsUp-1]
            else:
                raise RuntimeError ("Cannot find part of dir %s levels up, path %s is not long enough" % (levelsUp,path))
        return dname+os.sep
        #except:
            #raise RuntimeError('Failed to get directory name of the given path: %s'% path)


    def getBaseName(self, path):
        """Return the base name of pathname path."""
        pylabs.q.logger.log('Get basename for path: %s'%path,9)
        if path is None:
            raise TypeError('Path is not passed in system.fs.getDirName')
        try:
            return os.path.basename(path)
        except:
            raise RuntimeError('Failed to get base name of the given path: %s'% path)

    def pathShorten(self, path):
        """
        Clean path (change /var/www/../lib to /var/lib). On Windows, if the
        path exists, the short path name is returned.

        @param path: Path to clean
        @type path: string
        @return: Cleaned (short) path
        @rtype: string
        """
        cleanedPath = os.path.normpath(path)
        if pylabs.q.platform.isWindows() and self.exists(cleanedPath):
            # Only execute on existing paths, otherwise an error will be raised
            import win32api
            cleanedPath = win32api.GetShortPathName(cleanedPath)
            # Re-add '\' if original path had one
            sep = os.path.sep
            if path and path[-1] == sep and cleanedPath[-1] != sep:
                cleanedPath = "%s%s" % (cleanedPath, sep)
        return cleanedPath

    def pathClean(self,path):
        """
        goal is to get a equal representation in / & \ in relation to os.sep
        """
        path=path.replace("/",os.sep)
        path=path.replace("//",os.sep)
        path=path.replace("\\",os.sep)
        path=path.replace("\\\\",os.sep)
        path=path.strip()
        return path

    def pathDirClean(self,path):
        path=path+os.sep
        return self.pathClean(path)

    def dirEqual(self,path1,path2):
        return self.pathDirClean(path1)==self.pathDirClean(path1)

    def pathNormalize(self, path):
        """
        Wrapper around os.path.normpath.
        Normalizes a path eliminating double slashes
        @param path: path to normalize
        """
        return os.path.normpath(path)

    def pathRemoveDirPart(self,path,toremove,removeTrailingSlash=False):
        """
        goal remove dirparts of a dirpath e,g, a basepath which is not needed
        will look for part to remove in full path but only full dirs
        """
        path = self.pathNormalize(path)
        toremove = self.pathNormalize(toremove)

        if self.pathClean(toremove)==self.pathClean(path):
            return ""
        path=self.pathClean(path)
        path=path.replace(self.pathDirClean(toremove),"")
        if removeTrailingSlash:
            if path[0]==os.sep:
                path=path[1:]
        path=self.pathClean(path)
        return path

    def getParentDirName(self,path):
        """
        returns parent of path (only for dirs)
        returns empty string when there is no parent
        """
        path=self.pathDirClean(path)
        if len(path.split(os.sep))>2:
            return pylabs.q.system.fs.getDirName(path,lastOnly=True,levelsUp=1) #go 1 level up to find name of parent
        else:
            return ""

    def getParent(self, path):
        """
        Returns the parent of the path:
        /dir1/dir2/file_or_dir -> /dir1/dir2/
        /dir1/dir2/            -> /dir1/
        """
        parts = path.split(os.sep)
        if parts[-1] == '':
            parts=parts[:-1]
        parts=parts[:-1]
        if parts==['']:
            return os.sep
        return os.sep.join(parts)


    def parsePath(self,path, baseDir="",existCheck=True, checkIsFile=False):
        """
        parse paths of form /root/tmp/33_adoc.doc into the path, priority which is numbers before _ at beginning of path
        also returns filename
        checks if path can be found, if not will fail
        when filename="" then is directory which has been parsed
        if basedir specified that part of path will be removed

        example:
        q.system.fs.parsePath("/opt/qbase3/apps/specs/myspecs/definitions/cloud/datacenter.txt","/opt/qbase3/apps/specs/myspecs/",existCheck=False)
        @param path is existing path to a file
        @param baseDir, is the absolute part of the path not required
        @return list of dirpath,filename,extension,priority
             priority = 0 if not specified
        """
        #make sure only clean path is left and the filename is out
        if existCheck and not self.exists(path):
            raise RuntimeError("Cannot find file %s when importing" % path)
        if checkIsFile and not self.isFile(path):
            raise RuntimeError("Path %s should be a file (not e.g. a dir), error when importing" % path)
        extension=""
        if self.isDir(path):
            name=""
            path=self.pathClean(path)
        else:
            name=self.getBaseName(path)
            path=self.pathClean(path)
            #make sure only clean path is left and the filename is out
            path=self.getDirName(path)
            #find extension
            regexToFindExt="\.\w*$"
            if pylabs.q.codetools.regex.match(regexToFindExt,name):
                extension=pylabs.q.codetools.regex.findOne(regexToFindExt,name).replace(".","")
                #remove extension from name
                name=pylabs.q.codetools.regex.replace(regexToFindExt,regexFindsubsetToReplace=regexToFindExt, replaceWith="", text=name)

        if baseDir<>"":
            path=self.pathRemoveDirPart(path,baseDir)

        if name=="":
            dirOrFilename=pylabs.q.system.fs.getDirName(path,lastOnly=True)
        else:
            dirOrFilename=name
        #check for priority
        regexToFindPriority="^\d*_"
        if pylabs.q.codetools.regex.match(regexToFindPriority,dirOrFilename):
            #found priority in path
            priority=pylabs.q.codetools.regex.findOne(regexToFindPriority,dirOrFilename).replace("_","")
            #remove priority from path
            name=pylabs.q.codetools.regex.replace(regexToFindPriority,regexFindsubsetToReplace=regexToFindPriority, replaceWith="", text=name)
        else:
            priority=0

        return path,name,extension,priority            #if name =="" then is dir


    def getcwd(self):
        """get current working directory
        @rtype: string (current working directory path)
        """
        pylabs.q.logger.log('Get current working directory',9)
        try:
            return os.getcwd()
        except Exception, e:
            raise RuntimeError('Failed to get current working directory')

    def readlink(self, path):
        """Works only for unix
        Return a string representing the path to which the symbolic link points.
        """
        pylabs.q.logger.log('Read link with path: %s'%path,8)
        if path is None:
            raise TypeError('Path is not passed in system.fs.readLink')
        try:
            if pylabs.q.platform.isUnix():
                return os.readlink(path)
            elif pylabs.q.platform.isWindows():
                raise RuntimeError('Cannot readLink on windows')
        except Exception, e:
            raise RuntimeError('Falied to read link with path: %s \nERROR: %s'%(path, str(e)))

    def _listInDir(self, path,followSymlinks=True):
        """returns array with dirs & files in directory
        @param path: string (Directory path to list contents under)
        """
        if path is None:
            raise TypeError('Path is not passed in system.fs.listDir')
        try:
            if(pylabs.q.system.fs.exists(path)):
                if(pylabs.q.system.fs.isDir(path)) or (followSymlinks and self.checkDirOrLink(path)):
                    names = os.listdir(path)
                    return names
                else:
                    raise ValueError("Specified path: %s is not a Directory in system.fs.listDir"% path)
            else:
                raise RuntimeError("Specified path: %s does not exist in system.fs.listDir"% path)
        except:
            raise RuntimeError("Could not display the contents of the directory: %s"% path)

    def listFilesInDir(self, path, recursive=False, filter=None, minmtime=None, maxmtime=None):
        """Retrieves list of files found in the specified directory
        @param path:       directory path to search in
        @type  path:       string
        @param recursive:  recursively look in all subdirs
        @type  recursive:  boolean
        @param filter:     unix-style wildcard (e.g. *.py) - this is not a regular expression
        @type  filter:     string
        @param minmtime:   if not None, only return files whose last modification time > minmtime (epoch in seconds)
        @type  minmtime:   integer
        @param maxmtime:   if not None, only return files whose last modification time < maxmtime (epoch in seconds)
        @type  maxmtime:   integer
        @rtype: list
        """

        pylabs.q.logger.log('List files in directory with path: %s' % path,9)
        dircontent = self._listInDir(path)
        filesreturn = []
        for direntry in dircontent:

            fullpath = self.joinPaths(path, direntry)

            if self.isFile(fullpath):
                includeFile = False
                if (filter is None) or fnmatch.fnmatch(direntry, filter):
                    if (minmtime is not None) or (maxmtime is not None):
                        mymtime = os.stat(fullpath)[ST_MTIME]
                        if (minmtime is None) or (mymtime > minmtime):
                            if (maxmtime is None) or (mymtime < maxmtime):
                                includeFile = True
                    else:
                        includeFile = True
                if includeFile:
                    filesreturn.append(fullpath)

            elif recursive and self.isDir(fullpath):
                r = self.listFilesInDir(fullpath, recursive, filter, minmtime, maxmtime)
                if len(r) > 0:
                    filesreturn.extend(r)

        return filesreturn


    def checkDirOrLink(self,fullpath):
        """
        check if path is dir or link to a dir
        """
        if(pylabs.q.system.fs.isDir(fullpath)):
            return True
        if pylabs.q.system.fs.isLink(fullpath):
            link=pylabs.q.system.fs.readlink(fullpath)
            if pylabs.q.system.fs.isDir(link):
                return True
        return False

    def listDirsInDir(self,path,recursive=False,dirNameOnly=False,findDirectorySymlinks=True):
        """ Retrieves list of directories found in the specified directory
        @param path: string represents directory path to search in
        @rtype: list
        """
        pylabs.q.logger.log('List directories in directory with path: %s, recursive = %s' % (path, str(recursive)),9)

        #if recursive:
            #if not pylabs.q.system.fs.exists(path):
                #raise ValueError('Specified path: %s does not exist' % path)
            #if not pylabs.q.system.fs.isDir(path):
                #raise ValueError('Specified path: %s is not a directory' % path)
            #result = []
            #os.path.walk(path, lambda a, d, f: a.append('%s%s' % (d, os.path.sep)), result)
            #return result

        files=self._listInDir(path,followSymlinks=True)
        filesreturn=[]
        for file in files:
            fullpath=os.path.join(path,file)
            if (findDirectorySymlinks and self.checkDirOrLink(fullpath)) or self.isDir(fullpath):
                if dirNameOnly:
                    filesreturn.append(file)
                else:
                    filesreturn.append(fullpath)
                if recursive:
                    filesreturn.extend(self.listDirsInDir(fullpath,recursive,dirNameOnly,findDirectorySymlinks))
        return filesreturn

    def listPyScriptsInDir(self, path,recursive=True, filter="*.py"):
        """ Retrieves list of python scripts (with extension .py) in the specified directory
        @param path: string represents the directory path to search in
        @rtype: list
        """
        result = []
        for file in pylabs.q.system.fs.listFilesInDir(path,recursive=recursive, filter=filter):
            if file.endswith(".py"):
                filename = file.split(os.sep)[-1]
                scriptname = filename.rsplit(".", 1)[0]
                result.append(scriptname)
        return result

    def move(self, source, destin):
        """Main Move function
        @param source: string (If the specified source is a File....Calls moveFile function)
        (If the specified source is a Directory....Calls moveDir function)
        """
        if not pylabs.q.system.fs.exists(source):
            raise IOError('%s does not exist'%source)
        shutil.move(source, destin)

    def exists(self, path):
        """Check if the specified path exists
        @param path: string
        @rtype: boolean (True if path refers to an existing path, False for broken symcolic links)
        """
        if path is None:
            raise TypeError('Path is not passed in system.fs.exists')

        if(os.path.exists(path)):
            pylabs.q.logger.log('path %s exists' % str(path.encode("utf-8")),8)
            return True
        pylabs.q.logger.log('path %s does not exist' % str(path.encode("utf-8")),8)
        return False


    def symlink(self, path, target, overwriteTarget=False):
        """Create a symbolic link
        @param path: source path desired to create a symbolic link for
        @param target: destination path required to create the symbolic link at
        @param overwriteTarget: boolean indicating whether target can be overwritten
        """
        pylabs.q.logger.log('Getting symlink for path: %s to target %s'% (path, target),7)
        if ( path is None):
            raise TypeError('Path is None in system.fs.symlink')
        
        if target[-1]=="/":
                target=target[:-1]
                
        # if (overwriteTarget and self.isLink(target)):
        if overwriteTarget and self.exists(target):
            if self.isLink(target):
                self.unlink(target)
            elif self.isDir(target):
                self.removeDirTree(target)
            else:
                self.removeFile(target)

        dir = pylabs.q.system.fs.getDirName(target)
        if not pylabs.q.system.fs.exists(dir):
            pylabs.q.system.fs.createDir(dir)
            
        if pylabs.q.platform.isUnix():
            pylabs.q.logger.log(  "Creating link from %s to %s" %( path, target) )
            os.symlink(path, target)
        elif pylabs.q.platform.isWindows():
            raise RuntimeError('Cannot create a symbolic link on windows')

    def hardlinkFile(self, source, destin):
        """Create a hard link pointing to source named destin. Availability: Unix.
        @param source: string
        @param destin: string
        @rtype: concatenation of dirname, and optionally linkname, etc.
        with exactly one directory separator (os.sep) inserted between components, unless path2 is empty
        """
        pylabs.q.logger.log('Create a hard link pointing to %s named %s'% (source, destin),7)
        if (source is None):
            raise TypeError('Source path is not passed in system.fs.hardlinkFile')
        try:
            if pylabs.q.platform.isUnix():
                return os.link(source, destin)
            else:
                raise RuntimeError('Cannot create a hard link on windows')
        except:
            raise RuntimeError('Failed to hardLinkFile from %s to %s'% (source, destin))

    def checkDirParam(self,path):
        if(path.strip()==""):
            raise TypeError("path parameter cannot be empty.")
        path=path.replace("//","/")
        path=path.replace("\\\\","/")
        path=path.replace("\\","/")
        if path[-1]<>"/":
            path=path+"/"
        path=path.replace("/",os.sep)
        return path


    def isDir(self, path, followSoftlink=True):
        """Check if the specified Directory path exists
        @param path: string
        @param followSoftlink: boolean 
        @rtype: boolean (True if directory exists)
        """
        if ( path is None):
            raise TypeError('Directory path is None in system.fs.isDir')
        
        if not followSoftlink and self.isLink( path ) :
            return False
        
        if(os.path.isdir(path)):
            return True
        pylabs.q.logger.log('path [%s] is not a directory' % path.encode("utf-8"),8)
        return False

    def isEmptyDir(self, path):
        """Check if the specified directory path is empty
        @param path: string
        @rtype: boolean (True if directory is empty)
        """
        if ( path is None):
            raise TypeError('Directory path is None in system.fs.isEmptyDir')
        try:
            if(self._listInDir(path) == []):
                pylabs.q.logger.log('path %s is an empty directory'%path,9)
                return True
            pylabs.q.logger.log('path %s is not an empty directory'%path,9)
            return False
        except:
            raise RuntimeError('Failed to check if the specified path: %s is an empty directory...in system.fs.isEmptyDir'% path)

    def isFile(self, path, followSoftlink = True):
        """Check if the specified file exists for the given path
        @param path: string
        @param followSoftlink: boolean 
        @rtype: boolean (True if file exists for the given path)
        """
        pylabs.q.logger.log("isfile:%s" % path,8)
        
        
        if ( path is None):
            raise TypeError('File path is None in system.fs.isFile')
        try:
            if not followSoftlink and self.isLink( path ) :
                pylabs.q.logger.log('path %s is a file'%path,8)
                return True
            
            if(os.path.isfile(path)):
                pylabs.q.logger.log('path %s is a file'%path,8)
                return True
            
            pylabs.q.logger.log('path %s is not a file'%path,8)
            return False
        except:
            raise RuntimeError('Failed to check if the specified path: %s is a file...in system.fs.isFile'% path)

    def isLink(self, path):
        """Check if the specified path is a link
        @param path: string
        @rtype: boolean (True if the specified path is a link)
        """
        if ( path is None):
            raise TypeError('Link path is None in system.fs.isLink')
        try:
            if(os.path.islink(path)):
                pylabs.q.logger.log('path %s is a link'%path,8)
                return True
            pylabs.q.logger.log('path %s is not a link'%path,8)
            return False
        except:
            raise RuntimeError('Failed to check if the specified path: %s is a link...in system.fs.isDir'% path)

    def isMount(self, path):
        """Return true if pathname path is a mount point:
        A point in a file system where a different file system has been mounted.
        """
        pylabs.q.logger.log('Check if path %s is a mount point'%path,8)
        if path is None:
            raise TypeError('Path is passed null in system.fs.isMount')
        try:
            return os.path.ismount(path)
        except:
            raise RuntimeError('Failed to check if the path: %s is a mount point...in system.fs.isMount'%path)

    def statPath(self, path):
        """Perform a stat() system call on the given path
        @rtype: object whose attributes correspond to the members of the stat structure
        """
        if path is None:
            raise TypeError('Path is None in system.fs.statPath')
        try:
            return os.stat(path)
        except:
            raise OSError('Failed to perform stat system call on the specific path: %s in system.fs.statPath' % (path))

    def renameDir(self, dirname, newname):
        """Rename Directory from dirname to newname
        @param dirname: string (Directory original name)
        @param newname: string (Directory new name to be changed to)
        """
        pylabs.q.logger.log('Renaming directory %s to %s'% (dirname, newname),7)
        if dirname == newname:
            return
        if ((dirname is None) or (newname is None)):
            raise TypeError('Not enough parameters passed to system.fs.renameDir...[%s, %s]'%(dirname, newname))
        try:
            if(self.isDir(dirname)):
                os.rename(dirname, newname)
            else:
                raise ValueError('Path: %s is not a directory in system.fs.renameDir'%dirname)
        except:
            raise RuntimeError('Failed to rename the specified directory from %s to %s'% (dirname, newname))

    def unlinkFile(self, filename):
        """Remove the file path (only for files, not for symlinks)
        @param filename: File path to be removed
        """
        pylabs.q.logger.log('Unlink file with path: %s'%filename, 6)

        if (filename is None):
            raise TypeError('File name is None in QSstem.unlinkFile')
        try:
            if(self.isFile(filename)):
                os.unlink(filename)
        except:
            raise OSError('Failed to unlink the specified file path: %s in system.fs.unlinkFile'% filename)

    def unlink(self, filename):
        '''Remove the given file if it's a file or a symlink

        @param filename: File path to be removed
        @type filename: string
        '''
        pylabs.q.logger.log('Unlink path: %s' % filename, 6)

        if not filename:
            raise TypeError('File name is None in system.fs.unlink')
        try:
            os.unlink(filename)
        except:
            raise OSError('Failed to unlink the specified file path: [%s] in system.ds.unlink' % filename)

    def fileGetContents(self, filename):
        """Read a file and get contents of that file
        @param filename: string (filename to open for reading )
        @rtype: string representing the file contents
        """
        if filename is None:
            raise TypeError('File name is None in system.fs.fileGetContents')
        pylabs.q.logger.log('Opened file %s for reading'% filename,6)
        fp = open(filename,"r")
        try:
            pylabs.q.logger.log('Reading file %s'% filename,9)
            data = fp.read()
            # replace BOM characters from utf files
            if data and data[0] in (unicode(codecs.BOM_UTF8, "utf8"), codecs.BOM_UTF8): data = data[1:]

        finally:
            pylabs.q.logger.log('File %s is closed after reading'%filename,9)
            fp.close()
        return data

    def writeFile(self,filename, contents, append=False):
        """
        Open a file and write file contents, close file afterwards
        @param contents: string (file contents to be written)
        """
        if (filename is None) or (contents is None):
            raise TypeError('Passed None parameters in system.fs.writeFile')
        pylabs.q.logger.log('Opened file %s for writing'% filename,6)
        if append==False:
            fp = open(filename,"wb")
        else:
            fp = open(filename,"ab")
        try:
            pylabs.q.logger.log('Writing contents in file %s'%filename,9)
            #if filename.find("avahi")<>-1:
            #    ipshell()
            fp.write(contents)
        finally:
            fp.close()

    def fileSize(self, filename):
        """Get Filesize of file in bytes
        @param filename: the file u want to know the filesize of
        @return: int representing file size
        """
        pylabs.q.logger.log('Getting filesize of file: %s'%filename,8)
        if not self.exists(filename):
            raise RuntimeError("Specified file: %s does not exist"% filename)
        try:
            return os.path.getsize(filename)
        except Exception, e:
            raise OSError("Could not get filesize of %s\nError: %s"%(filename,str(e)))


    def writeObjectToFile(self,filelocation,obj):
        """
        Write a object to a file(pickle format)
        @param filelocation: location of the file to which we write
        @param obj: object to pickle and write to a file
        """
        if not filelocation or not obj:
            raise ValueError("You should provide a filelocation or a object as parameters")
        pylabs.q.logger.log("Creating pickle and write it to file: %s" % filelocation,6)
        try:
            pcl = pickle.dumps(obj)
        except Exception, e:
            raise Exception("Could not create pickle from the object \nError: %s" %(str(e)))
        pylabs.q.system.fs.writeFile(filelocation,pcl)
        if not self.exists(filelocation):
            raise Exception("File isn't written to the filesystem")

    def readObjectFromFile(self,filelocation):
        """
        Read a object from a file(file contents in pickle format)
        @param filelocation: location of the file
        @return: object
        """
        if not filelocation:
            raise ValueError("You should provide a filelocation as a parameter")
        pylabs.q.logger.log("Opening file %s for reading" % filelocation,6)
        contents = pylabs.q.system.fs.fileGetContents(filelocation)
        try:
            pylabs.q.logger.log("creating object",9)
            obj = pickle.loads(contents)
        except Exception, e:
            raise Exception("Could not create the object from the file contents \n Error: %s" %(str(e)))
        return obj

    def md5sum(self, filename):
        """Return the hex digest of a file without loading it all into memory
        @param filename: string (filename to get the hex digest of it)
        @rtype: md5 of the file
        """
        pylabs.q.logger.log('Get the hex digest of file %s without loading it all into memory'%filename,8)
        if filename is None:
            raise('File name is None in system.fs.md5sum')
        try:
            try:
                fh = open(filename)
                digest = hashlib.md5()
                while 1:
                    buf = fh.read(4096)
                    if buf == "":
                        break
                    digest.update(buf)
            finally:
                fh.close()
            return digest.hexdigest()
        except:
            raise RuntimeError('Failed to get the hex digest of the file %sin system.fs.md5sum' % filename)


    def walkExtended(self, root, recurse=0, dirPattern='*' , filePattern='*', followSoftLinks = True ):
        """
        Extended Walk version: seperate dir and file pattern
        """
        pylabs.q.logger.log('Scanning directory (walk) %s'%root,6)
        result = []
        try:
            names = os.listdir(root)
        except os.error:
            return result

        dirPattern = dirPattern or '*'
        dirPatList = dirPattern.split(';')
        filePattern = filePattern or '*'
        filePatList = filePattern.split(';')

        for name in names:
            fullname = os.path.normpath(os.path.join(root, name))
            if self.isFile(fullname, followSoftLinks):
                fileOK = False
                dirOK = False
                for fPat in filePatList:
                    if (fnmatch.fnmatch(name,fPat)):
                        fileOK = True
                for dPat in dirPatList:
                    if (fnmatch.fnmatch(os.path.dirname(fullname),dPat)):
                        dirOK = True
                if fileOK and dirOK:
                    result.append(fullname)
            if self.isDir(fullname, followSoftLinks):
                for dPat in dirPatList:
                    if (fnmatch.fnmatch(name,dPat)):
                        result.append(fullname)
            if recurse:
                result = result + self.WalkExtended(fullname,recurse,dirPattern,filePattern, followSoftLinks)

        return result

    WalkExtended = deprecated('q.system.fs.WalkExtended',
                              'q.system.fs.walkExtended', '3.2')(walkExtended)

    def walk(self, root, recurse=0, pattern='*', return_folders=0, return_files=1, followSoftlinks = True ):
        """This is to provide ScanDir similar function
        It is going to be used wherever some one wants to list all files and subfolders
        under one given directlry with specific or none matchers
        """
        pylabs.q.logger.log('Scanning directory (walk)%s'%root,6)
        # initialize
        result = []

        # must have at least root folder
        try:
            names = os.listdir(root)
        except os.error:
            return result

        # expand pattern
        pattern = pattern or '*'
        pat_list = pattern.split(';')

        # check each file
        for name in names:
            fullname = os.path.normpath(os.path.join(root, name))

            # grab if it matches our pattern and entry type
            for pat in pat_list:
                if (fnmatch.fnmatch(name, pat)):
                    
                    if ( self.isFile(fullname, followSoftlinks) and return_files ) or (return_folders and self.isDir(fullname, followSoftlinks)):
                        result.append(fullname)
                    continue

            # recursively scan other folders, appending results
            if recurse:
                if self.isDir(fullname) and not self.isLink(fullname):
                    result = result + self.walk( fullname, recurse, pattern, return_folders, return_files, followSoftlinks )
        return result

    Walk = deprecated('q.system.fs.Walk', 'q.system.fs.walk', '3.2')(walk)

    def getTmpFilePath(self,cygwin=False):
        """Generate a temp file path
        Located in temp dir of QDirs
        @rtype: string representing the path of the temp file generated
        """
        #return tempfile.mktemp())
        tmpdir=pylabs.q.dirs.tmpDir
        fd, path = tempfile.mkstemp(dir=tmpdir)
        try:
            real_fd = os.fdopen(fd)
            real_fd.close()
        except (IOError, OSError):
            pass
        if cygwin:
            path=path.replace("\\","/")
            path=path.replace("//","/")
        return path

    def getTempFileName(self, dir=None, prefix=''):
        """Generates a temp file for the directory specified
        @param dir: Directory to generate the temp file
        @param prefix: string to start the generated name with
        @rtype: string representing the generated temp file path
        """
        dir = dir or pylabs.q.dirs.tmpDir
        return tempfile.mktemp('', prefix, dir)

    def isAsciiFile(self, filename, checksize=4096):
        """Read the first <checksize> bytes of <filename>.
           Validate that only valid ascii characters (32-126), \r, \t, \n are
           present in the file"""
        BLOCKSIZE = 4096
        dataread = 0
        if checksize == 0:
            checksize = BLOCKSIZE
        fp = open(filename,"r")
        isAscii = True
        while dataread < checksize:
            data = fp.read(BLOCKSIZE)
            if not data:
                break
            dataread += len(data)
            for x in data:
                if not ((ord(x)>=32 and ord(x)<=126) or x=='\r' or x=='\n' or x=='\t'):
                    isAscii = False
                    break
            if not isAscii:
                break
        fp.close()
        return isAscii

    def isBinaryFile(self, filename, checksize=4096):
        return not self.isAsciiFile(filename, checksize)

    lock = staticmethod(lock)
    lock_ = staticmethod(lock_)
    islocked = staticmethod(islocked)
    unlock = staticmethod(unlock)
    unlock_ = staticmethod(unlock_)

    def validateFilename(self, filename, platform=None):
        '''Validate a filename for a given (or current) platform

        Check whether a given filename is valid on a given platform, or the
        current platform if no platform is specified.

        Rules
        =====
        Generic
        -------
        Zero-length filenames are not allowed

        Unix
        ----
        Filenames can contain any character except 0x00. We also disallow a
        forward slash ('/') in filenames.

        Filenames can be up to 255 characters long.

        Windows
        -------
        Filenames should not contain any character in the 0x00-0x1F range, '<',
        '>', ':', '"', '/', '\', '|', '?' or '*'. Names should not end with a
        dot ('.') or a space (' ').

        Several basenames are not allowed, including CON, PRN, AUX, CLOCK$,
        NUL, COM[1-9] and LPT[1-9].

        Filenames can be up to 255 characters long.

        Information sources
        ===================
        Restrictions are based on information found at these URLs:

         * http://en.wikipedia.org/wiki/Filename
         * http://msdn.microsoft.com/en-us/library/aa365247.aspx
         * http://www.boost.org/doc/libs/1_35_0/libs/filesystem/doc/portability_guide.htm
         * http://blogs.msdn.com/brian_dewey/archive/2004/01/19/60263.aspx

        @param filename: Filename to check
        @type filename: string
        @param platform: Platform to validate against
        @type platform: L{PlatformType}

        @returns: Whether the filename is valid on the given platform
        @rtype: bool
        '''
        from pylabs.enumerators import PlatformType
        platform = platform or PlatformType.findPlatformType()

        if not filename:
            return False

        #When adding more restrictions to check_unix or check_windows, please
        #update the validateFilename documentation accordingly

        def check_unix(filename):
            if len(filename) > 255:
                return False

            if '\0' in filename or '/' in filename:
                return False

            return True

        def check_windows(filename):
            if len(filename) > 255:
                return False

            if os.path.splitext(filename)[0] in ('CON', 'PRN', 'AUX', 'CLOCK$', 'NUL'):
                return False

            if os.path.splitext(filename)[0] in ('COM%d' % i for i in xrange(1, 9)):
                return False

            if os.path.splitext(filename)[0] in ('LPT%d' % i for i in xrange(1, 9)):
                return False

            #ASCII characters 0x00 - 0x1F are invalid in a Windows filename
            #We loop from 0x00 to 0x20 (xrange is [a, b[), and check whether
            #the corresponding ASCII character (which we get through the chr(i)
            #function) is in the filename
            for c in xrange(0x00, 0x20):
                if chr(c) in filename:
                    return False

            for c in ('<', '>', ':', '"', '/', '\\', '|', '?', '*'):
                if c in filename:
                    return False

            if filename.endswith((' ', '.', )):
                return False

            return True

        if platform.isWindows():
            return check_windows(filename)

        if platform.isUnix():
            return check_unix(filename)

        raise NotImplementedError('Filename validation on given platform not supported')

    def fileConvertLineEndingCRLF(self,file):
        '''Convert CRLF line-endings in a file to LF-only endings (\r\n -> \n)

        @param file: File to convert
        @type file: string
        '''
        pylabs.q.logger.log("fileConvertLineEndingCRLF "+file, 8)
        content=pylabs.q.system.fs.fileGetContents(file)
        lines=content.split("\n")
        out=""
        for line in lines:
            line=line.replace("\n","")
            line=line.replace("\r","")
            out=out+line+"\n"
        self.writeFile(file,out)

    def find(self, startDir,fileregex):
        """Search for files or folders matching a given pattern
        this is a very weard function, don't use is better to use the list functions
        make sure you do changedir to the starting dir first
        example: find("*.pyc")
        @param fileregex: The regex pattern to match
        @type fileregex: string
        """
        pylabs.q.system.fs.changeDir(startDir)
        import glob
        return glob.glob(fileregex)

    def grep(self, fileregex, lineregex):
        """Search for lines matching a given regex in all files matching a regex

        @param fileregex: Files to search in
        @type fileregex: string
        @param lineregex: Regex pattern to search for in each file
        @type lineregex: string
        """
        import glob, re, os
        for filename in glob.glob(fileregex):
            if os.path.isfile(filename):
                f = open(filename, 'r')
                for line in f.xreadlines():
                    if re.match(lineregex, line):
                        print "%s: %s" % (filename, line)

    cleanupString = staticmethod(cleanupString)

    def constructDirPathFromArray(self,array):
        path=""
        for item in array:
            path=path+os.sep+item
        path=path+os.sep
        if pylabs.q.platform.isUnix():
            path=path.replace("//","/")
            path=path.replace("//","/")
        return path

    def constructFilePathFromArray(self,array):
        path=self.constructDirPathFromArray(array)
        if path[-1]=="/":
            path=path[0:-1]
        return path

    def pathToUnicode(self, path):
        """
        Convert path to unicode. Use the local filesystem encoding. Will return
        path unmodified if path already is unicode.

        Use this to convert paths you received from the os module to unicode.

        @param path: path to convert to unicode
        @type path: basestring
        @return: unicode path
        @rtype: unicode
        """
        from pylabs import Dirs
        return Dirs.pathToUnicode(path)

    def targzCompress(self, sourcedirpath, destinationpath,followlinks=False,destInTar="",pathRegexIncludes=['.[a-zA-Z0-9]*'], \
                      pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[], depths=[],\
                      extrafiles=[]):
        """
        @param source_dir: Source directory name.
        @param destination: Destination filename.
        @param followlinks: do not tar the links, follow the link and add that file or content of directory to the tar
        @param pathRegexIncludes: / Excludes  match paths to array of regex expressions (array(strings))
        @param contentRegexIncludes: / Excludes match content of files to array of regex expressions (array(strings))
        @param depths: array of depth values e.g. only return depth 0 & 1 (would mean first dir depth and then 1 more deep) (array(int))        
        @param destInTar when not specified the dirs, files under sourcedirpath will be added to root of 
                  tar.gz with this param can put something in front e.g. /qbase3/ prefix to dest in tgz
        @param extrafiles is array of array [[source,destpath],[source,destpath],...]  adds extra files to tar
        (TAR-GZ-Archive *.tar.gz)
        """
        import os.path
        import tarfile
        

        pylabs.q.logger.log("Compressing directory %s to %s"%(sourcedirpath, destinationpath))
        if not pylabs.q.system.fs.exists(pylabs.q.system.fs.getDirName(destinationpath)):
            pylabs.q.system.fs.createDir(pylabs.q.system.fs.getDirName(destinationpath))
        t = tarfile.open(name = destinationpath, mode = 'w:gz')
        if not(followlinks<>False or destInTar<>"" or pathRegexIncludes<>['.*'] or pathRegexExcludes<>[] or contentRegexIncludes<>[] or contentRegexExcludes<>[] or depths<>[]):
            t.add(sourcedirpath, "/")
        else:
            def addToTar(params,path):
                tarfile=params["t"]
                destInTar=params["destintar"]
                destpath=pylabs.q.system.fs.joinPaths(destInTar,pylabs.q.system.fs.pathRemoveDirPart(path, sourcedirpath))
                if pylabs.q.system.fs.isLink(path) and followlinks:
                    path=pylabs.q.system.fs.readlink('/opt/test/apps/hg')
                pylabs.q.logger.log("fstar: add file %s to tar" % path,7)
                tarfile.add(path,destpath)
            params={}
            params["t"]=t
            params["destintar"]=destInTar
            pylabs.q.system.fswalker.walk(sourcedirpath, addToTar, params,\
                                True, False, \
                                pathRegexIncludes, pathRegexExcludes, contentRegexIncludes, \
                                contentRegexExcludes, depths)
            if extrafiles<>[]:
                for extrafile in extrafiles:
                    source=extrafile[0]
                    destpath=extrafile[1]
                    t.add(source,pylabs.q.system.fs.joinPaths(destInTar,destpath))
                    
        t.close()

    def targzUncompress(self,sourceFile,destinationdir,removeDestinationdir=True):
        """
        compress dirname recursive
        @param sourceFile: file to uncompress
        @param destinationpath: path of to destiniation dir, sourcefile will end up uncompressed in destination dir
        """
        if removeDestinationdir:
            pylabs.q.system.fs.removeDirTree(destinationdir)
        if not pylabs.q.system.fs.exists(destinationdir):
            pylabs.q.system.fs.createDir(destinationdir)
        import tarfile
        if not pylabs.q.system.fs.exists(destinationdir):
            pylabs.q.system.fs.createDir(destinationdir)

        # The tar of python does not create empty directories.. this causes manny problem while installing so we choose to use the linux tar here
        # tar = tarfile.open(sourceFile)
        # tar.extractall(destinationdir)
        # tar.close()
        cmd = "tar xzf '%s' -C '%s'" % (sourceFile, destinationdir)
        pylabs.q.system.process.execute(cmd)
