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
 
# This extension is available at q.remote.system
import warnings
warnings.filterwarnings('ignore', r'.*sha.*')
import paramiko, os, socket
from pylabs import q
import signal
import SocketServer, select
import threading
import sys

class InvalidIpAddressError(ValueError):
    pass

class RemoteSystemNotReachableError(RuntimeError):
    pass

class RemoteSystemAuthenticationError(RuntimeError):
    pass

class Exceptions(object):
    RemoteSystemNotReachableError = RemoteSystemNotReachableError
    RemoteSystemAuthenticationError = RemoteSystemAuthenticationError
    InvalidIpAddressError = InvalidIpAddressError

class RemoteSystem(object):
    name = "q.remote.system"
    
    exceptions = Exceptions
        
    
    def connect(self, ip, login, password, timeout=10.0, port=22):
        """Creates a connection object to a remote system via ssh.
        
        @param ip: Ipaddress of the remote system
        @type ip: string
        @param login: Username used for login on remote system
        @type login: string
        @param password: Password used for login on remote system
        @type password: string
        @param timeout: Timeout for the SSH session
        @type timeout: float
        
        @rtype: RemoteSystemConnection
        @return: A connection object to the remote system
        
        @raise InvalidIpAddressError: The IP address was not valid
        @raise RemoteSystemNotReachableError: An error occurred while connecting to the remote system
        @raise RemoteSystemAuthenticationError: Could not authenticate to the remote system
        @raise socket.error: Unhandeld network error
        """
        
        
        if not q.basetype.ipaddress.check(ip):
            raise InvalidIpAddressError("IP address is not a valid IPv4 address")
        
        try:
            remoteConnection = RemoteSystemConnection(ip, login, password, timeout, port)
        except paramiko.AuthenticationException, authEx:
            raise RemoteSystemAuthenticationError(authEx)
        except paramiko.SSHException, sshEx:
            raise RemoteSystemNotReachableError(sshEx)
        except socket.timeout, e:
            raise RemoteSystemNotReachableError(e)
        except socket.error, e:
            reraise = False
            try:
                if e[0] == 146:
                    raise RemoteSystemNotReachableError(e[1])
                else:
                    raise
            except IndexError:
                reraise = True
            if reraise:
                raise
        
        return remoteConnection
    




class RemoteSystemConnection(object):
    
    def __init__(self, ip, login, password, timeout, port):
        self._closed = False
        self._ipaddress = ip
        self._port = port
        self._client= paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(ip, username=login, password=password, timeout=timeout, port=port)
        self._process = None
        self._fs = None
        self._portforward = None
    
    def close(self):
        """Closes the connection to the remote system"""
        self._client.close()
        self._closed = True
    
    def __getattribute__(self, name):
        if object.__getattribute__(self, '_closed'):
            raise RuntimeError('There is no active connection.')
        return object.__getattribute__(self, name)
    
    def _getProcess(self):
        if not self._process:
            self._process = RemoteSystemProcess(self._client)
        return self._process
    
    def _getFs(self):
        if not self._fs:
            self._fs = RemoteSystemFS(self._client)
        return self._fs
    
    def _getIpAddress(self):
        return self._ipaddress
    
    def _getPortForward(self):
        if not self._portforward:
            self._portforward = RemoteSystemPortForward(self._client, self._getProcess())
        
        return self._portforward
    
    process = property(fget=_getProcess)
    
    fs = property(fget=_getFs)
    
    ipaddress = property(fget=_getIpAddress, doc="IP address of the machine you are connected to")
    
    portforward = property(fget = _getPortForward, doc = "Executes remote and local port forwarding using the connecting machine as ssh server")
    
class _remoteSystemObject(object):
    
    def __init__(self, connection, ipaddress=None):
        if not isinstance(connection, paramiko.SSHClient):
            raise TypeError('The connection parameter is not of type paramiko.SSHClient')
        self._connection = connection
        self._ipaddress = ipaddress or connection.get_transport().sock.getpeername()[0]

class RemoteSystemProcess(_remoteSystemObject):


    def _execute_common(self, command, dieOnNonZeroExitCode=True, timeout=10.0):
        """
        only works on all platforms
        return a tuple of (exitcode, stdout, stderr)
        Execute a command on the SSH server.  Wait till output done.
        @raise SSHException: if the server fails to execute the command
        """
        q.logger.log("Execute ssh command %s on %s" % (command, self._ipaddress))
        #channel = self._connection.get_transport().open_session()
        #ipshell()
        # stdin, channelFileStdOut, channelFileStdErr=self._connection.exec_command(command)

        # Code stolen from self._connection.exec_command(command), it identitical
        bufsize = -1
        chan = self._connection.get_transport().open_session()
        chan.settimeout(timeout)
        chan.exec_command(command)
        chan.makefile('wb', bufsize)
        channelFileStdOut = chan.makefile('rb', bufsize)
        channelFileStdErr = chan.makefile_stderr('rb', bufsize)
        # return stdin, stdout, stderr
    
        myOut = ""
        myErr = ""
        while ((not channelFileStdOut.channel.eof_received) or (not channelFileStdErr.channel.eof_received)):
            rl, wl, xl = select.select([chan],[chan],[chan], timeout)
            if not any([rl, wl, xl]):
                raise socket.timeout("Command %s timedout after %s seconds" % (command, timeout))
            if channelFileStdOut.channel.recv_ready():
                tmp=(channelFileStdOut.channel.recv(1024))
                q.logger.log("ssh %s out:%s" % (self._ipaddress,tmp),3)
                myOut += tmp
            if channelFileStdErr.channel.recv_stderr_ready():
                tmp=(channelFileStdErr.channel.recv_stderr(1024))
                q.logger.log("ssh %s err:%s" % (self._ipaddress,tmp),4)
                myErr += tmp
        tmp=channelFileStdOut.read()
        q.logger.log("ssh %s out:%s" % (self._ipaddress,tmp),3)
        myOut += tmp
        tmp=channelFileStdErr.read()
        q.logger.log("ssh %s err:%s" % (self._ipaddress,tmp),4)
        myErr += tmp

        exitcode = chan.recv_exit_status()

        #print 'Output:'   + myOut
        #print 'Error:'    + myErr
        #print 'ExitCode:' + str(exitcode)

        # Only die if exitcode != 0, error != '' is not enough to conclude that the process went wrong because it may only be warnings!
        if dieOnNonZeroExitCode and exitcode != 0:
            q.eventhandler.raiseCriticalError("Process terminated with non 0 exitcode, got exitcode " + str(exitcode))

        return exitcode, myOut, myErr
    
    # Todo tomorow refactor other methods to use this one
    # For now don't break code

    def execute(self, command, dieOnNonZeroExitCode=True, outputToStdout=True, loglevel=5, ignoreOutput=False, timeout=None, withError=False):
        """Executes a command, returns the exitcode and the output
        
        @param command: command to execute
        @type command: string
        @param dieOnNonZeroExitCode: die if got non zero exitcode
        @type dieOnNonZeroExitCode: bool
        @param outputToStdout (NO LONGER RELEVANT)
        @param ignoreOutput (NO LONGER RELEVANT)
        @param timeout: seconds to wait for a pending read/write operation.  Infinity if omitted
        @type timeout: float
        @param withError: If true the error is also returned
        @type timeout: bool
        
        @rtype: number
        @return: represents the exitcode plus the output and error output (if enabled by withError) of the executed command. If exitcode is not zero then the executed command returned with errors
        """

        #@Todo: outputToStdout, loglevel not used
        # are they usefull are simply there for backwards compatibility?

        if q.platform.has_parent(q.enumerators.PlatformType.UNIX):
            exitcode, output, error = self._executeUnix(command, dieOnNonZeroExitCode, timeout)
        else:
            
            exitcode, output, error = self._execute_common(command, dieOnNonZeroExitCode, timeout)
            
        if not withError:
            # Do things the old way
            if not ignoreOutput:
                return exitcode, output
            else:
                return exitcode
        else:
            # Add error to return tuple
            if not ignoreOutput:
                return exitcode, output, error
            else:
                return exitcode, error

    def _executeUnix(self, command,dieOnError=True, timeout=10.0):
        """
        only works for unix
        Execute a command on the SSH server.  Wait till output done.
        @raise SSHException: if the server fails to execute the command
        """
        command = command + ' ; echo "***EXITCODE***:$?"'
        exitcode, output, error = self._execute_common(command, dieOnNonZeroExitCode=False, timeout=timeout)

        
        # Not correct, many command issue warnings on stderr!
        #if len(error.strip())>0 and dieOnError:
        #    raise RuntimeError("Could not execute %s on %s, output was \n%s\n%s\n" % (command,self._ipaddress,myOut,myErr))

        index = output.find("***EXITCODE***:")
        if index == -1: #Something unknown when wrong, we did not recieve all output
            exitcode = 1000
            # raise RuntimeError("Did not get all output from executing the SSH command %s" % command) ??
        else:
            lenght      = len("***EXITCODE***:")
            exitcodestr = output[index + lenght:]
            exitcode    = int(exitcodestr) # get the exit code
            output      = output[:index]   # clean the output

        if dieOnError and exitcode == 1000:
            q.eventhandler.raiseCriticalError("Process terminated with unknown exitcode!!")

        if dieOnError and exitcode != 0:
            q.eventhandler.raiseCriticalError("Process terminated with non 0 exitcode, got exitcode: " + str(exitcode) +
                                              " and error: " + error +
                                              " and output: " + output)

        return exitcode, output, error
    
    
    def killProcess(self, pid):
        """
        Kills a process using sigterm signal
        
        @param pid: process id of the process to be killed
        @type pid: int
        """
        command = 'kill -%(signum)s %(pid)s'%{'pid': pid, 'signum': signal.SIGTERM}
        exitCode, output = self.execute(command, dieOnNonZeroExitCode = False, outputToStdout = False)
        if exitCode:
            q.console.echo('Failed to execute remote command %s. Reason %s'%(command, output))
        return exitCode, output

class RemoteSystemFS(_remoteSystemObject):
    
    def uploadFile(self, localpath, remotepath):
        """Copy a local file (localpath) to the remote system as remotepath
        
        @param localpath: the local file to copy
        @type localpath: string
        
        @param remotepath: the destination path on the remote system
        @type remotepath: string
        
        @raise TypeError: localpath or remotepath is None
        """
        
        if localpath is None:
            raise TypeError('Local path is None in remotesystem.fs.uploadFile')
        if remotepath is None:
            raise TypeError('Remote path is None in remotesystem.fs.uploadFile')
        
        sf = self._connection.open_sftp()
        try:
            sf.put(localpath, remotepath)
            q.logger.log('Uploaded file %s to %s' % (localpath, remotepath))
        finally:
            sf.close()
    
    def fileGetContents(self, filename):
        """Read a file and get contents of that file
        
        @param filename: filename to open for reading
        @type filename: string
        
        @rtype: string 
        @return: representing the file contents
        
        @raise TypeError: filename is None
        """
        
        if filename is None:
            raise TypeError('File name is None in remotesystem.fs.fileGetContents')
        
        localfile = q.system.fs.getTempFileName()
        
        sf = self._connection.open_sftp()
        
        try:
            q.logger.log('Opened SFTP connection to receive file %s' % filename)
            try:
                sf.get(filename, localfile)
                q.logger.log('Saved %s file to %s' % (filename, localfile))
                return q.system.fs.fileGetContents(localfile)
            finally:
                q.system.fs.remove(localfile)
        finally:
            sf.close()
    
    def writeFile(self, filename, contents):
        """Open a file and write file contents, close file afterwards
        
        @param filename: filename to open for writing
        @type filename: string
        @param contents: file contents to be written
        @type contents: string
        
        @raise TypeError: filename or contents passed are None
        @raise ValueError: filename should be a full path
        """
        
        if (filename is None) or (contents is None):
            raise TypeError('Passed None parameters in remotesystem.fs.writeFile')
        
        if not filename.startswith('/'):
            raise ValueError('Filename should be a full path!')
        
        localfile = q.system.fs.getTempFileName()
        
        try:
            # Don't bother copying the file first - we're going to clobber it anyway
            q.system.fs.writeFile(localfile, contents)
            sf = self._connection.open_sftp()
            
            try:
                q.logger.log('Opened SFTP connection to send %s to %s' % (localfile, filename))
                sf.put(localfile, filename)
            finally:
                sf.close()
        finally:
            q.system.fs.remove(localfile)
            

    def exists(self, path):
        """Check if the specified path exists
        @param path: string
        @rtype: boolean (True if path refers to an existing path, False for broken symcolic links)
        
        """
        if path is None:
            raise TypeError('Path is not passed in remote.system.fs.exists')

        sf = self._connection.open_sftp()
        try:
            sf.stat(path)
        except IOError, e:
            if e.errno == 2:
                q.logger.log('path %s does not exit' % str(path.encode("utf-8")), 8)
                return False
            else:
                raise 
        except:
            raise 
        finally:
            sf.close()
        q.logger.log('path %s exists' % str(path.encode("utf-8")), 8)
        return True

    def isDir(self, path):
        """Check if the specified Directory path exists
        @param path: string
        @rtype: boolean (True if directory exists)
        
        @raise TypeError: path is empty
        """
        if ( path is None):
            raise TypeError('Directory path is None in system.fs.isDir')
        sf = self._connection.open_sftp()
        try:
            sf.listdir(path)
        except IOError, e:
            if e.errno == 2:
                q.logger.log('path [%s] is not a directory' % path.encode("utf-8"), 8)
                return False
            else:
                raise
        finally:
            q.logger.log('path [%s] is a directory' % path.encode("utf-8"), 8)
            sf.close()
        return True

    def createDir(self, newdir):
        """Create new Directory
        @param newdir: string (Directory path/name)
        if newdir was only given as a directory name, the new directory will be created on the default path,
        if newdir was given as a complete path with the directory name, the new directory will be created in the specified path
        
        @raise TypeError: newdir parameter is empty
        @raise RuntimeError: failed to create directory
        """
        q.logger.log('Creating directory if not exists %s' % newdir.encode("utf-8"),8)
        if newdir == '' or newdir == None:
            raise TypeError('The newdir-parameter of system.fs.createDir() is None or an empty string.')
        try:
            if self.exists(newdir):
                q.logger.log('Directory trying to create: [%s] already exists'%newdir.encode("utf-8"),8)
                pass
            else:
                head, tail = os.path.split(newdir)
                if head and not self.isDir(head):
                    self.createDir(head)
                if tail:
                    sf = self._connection.open_sftp()
                    try:
                        sf.mkdir(newdir)
                    finally:
                        sf.close()
                q.logger.log('Created the directory [%s]' % newdir.encode("utf-8"),8)
        except:
            raise RuntimeError("Failed to create the directory [%s]" % newdir.encode("utf-8"))

    def copyDirTree(self, src, dst, keepsymlinks = False):
        """Recursively copy an entire directory tree rooted at src
        
        The dst directory may already exist; if not,
        it will be created as well as missing parent directories
        
        @param src: string (source of directory tree to be copied)
        @param dst: string (path directory to be copied to...should not already exist)
        @param keepsymlinks: bool (True keeps symlinks instead of copying the content of the file)
        
        @raise TypeError: src or dst is empty
        """
        if ((src is None) or (dst is None)):
            raise TypeError('Not enough parameters passed in system.fs.copyDirTree to copy directory from %s to %s '% (src, dst))
        stdin, stdout, stderr = self._connection.exec_command('uname -s')
        solaris = False
        for line in stdout:
            if line.startswith('SunOS'):
                q.logger.log("Solaris", 5)
                solaris = True
        if solaris:
            if keepsymlinks:
                symlinks = '-P'
            else:
                symlinks = ''
        else:
            q.logger.log("No solaris", 5)
            if keepsymlinks:
                symlinks = '-L'
            else:
                symlinks = '-P'
        
        if self.isDir(src):
            if not self.exists(dst):
                self.createDir(dst)
            cmd = 'cp -rf %s %s/* %s' % (symlinks, src, dst)
            q.logger.log("Executing [%s]" % cmd, 5)
            self._connection.exec_command(cmd)
        else:
            raise RuntimeError('Source path %s in remote.system.fs.copyDirTree is not a directory'% src)

    def copyDirTreeLocalRemote(self,source, destination="",removeNonRelevantFiles=False):
        """
        Recursively copy an entire directory tree rooted at source.
        The destination directory may already exist; if not, it will be created
    
        Parameters:        
        - source: string (source of directory tree to be copied)
        - destination: string (path directory to be copied to...should not already exist)
          if destination no specified will use same location as source
        """
        #@todo check and fix
        raise RuntimeError("not fully implemented yet")
        if destination=="":
            destination=source        
        dirs={}
        self.executewait("mkdir -p %s" % destination)   
        ftp=self.getSFtpConnection()
        if removeNonRelevantFiles:
            self._removeRedundantFiles(source)       
        files=q.system.fs.listFilesInDir(source,recursive=True)                 
        q.logger.log("Coppy %s files from %s to %s" % (len(files),source,destination),2)
        for filepath in files:            
            dest=q.system.fs.joinPaths (destination,q.system.fs.pathRemoveDirPart(filepath,source))            
            destdir=q.system.fs.getDirName(dest)            
            if not dirs.has_key(destdir):
                q.logger.log("Create dir %s" % (destdir))    
                #ftp.mkdir(destdir)
                self.executewait("mkdir -p %s" % destdir)
                dirs[destdir]=1
            q.logger.log("put %s to %s" % (filepath,dest))
            ftp.put(filepath,dest)        
        
    def moveFile(self, source, destination):
        """Move a file from source path to destination path
        
        @param source: Source file path
        @type source: string
        @param destination: Destination path the file should be moved to 
        @type destination: string
        
        @raise TypeError: source or destin is empty
        @raise RuntimeError: Specified source / destination does not exist
        @raise RuntimeError: file could not be moved
        """
        
        q.logger.log('Move file from %s to %s'% (source, destination),6)
        if not source or not destination:
            raise ValueError("Not enough parameters given to remote.system.fs.moveFile: move from %s, to %s" % (source, destination))
        try:
            if(self.isFile(source)):
                if(self.isDir(destination)):
                    self.copyFile(source, destination)
                    self.removeFile(source)
                else:
                    raise RuntimeError("The specified destination path in system.fs.moveFile does not exist: %s" % destination)
            else:
                raise RuntimeError("The specified source path in system.fs.moveFile does not exist: %s" % source)
        except:
            raise RuntimeError("File could not be moved...in remote.system.fs.moveFile: from %s to %s " % (source, destination))
    
    def isFile(self, name):
        """Check if the specified file exists for the given path
        
        @param name: string
        @rtype: boolean (True if file exists for the given path)
        
        @raise TypeError: name is empty
        """
        q.logger.log("isfile:%s" % name, 8)
        if ( name is None):
            raise TypeError('File name is None in remote.system.fs.isFile')
        sf = self._connection.open_sftp()
        if self.exists(name):
            try:
                sf.listdir(name)
            except IOError, e:
                if e.errno == 2:
                    q.logger.log('[%s] is a file' % name.encode("utf-8"), 8)
                    return True
                else:
                    raise
            finally:
                q.logger.log('[%s] is not a file' % name.encode("utf-8"), 8)
                sf.close()
        return False

    def removeFile(self, path):
        """Remove a file
        
        @param path: File path required to be removed
        @type path: string
        
        @raise TypeError: path is empty
        """
        
        q.logger.log('Removing file with path: %s'%path,6)
        if not path:
            raise TypeError('Not enough parameters passed to system.fs.removeFile: %s'%path)
        if(self.exists(path)):
            if(self.isFile(path)):
                sf = self._connection.open_sftp()
                try:
                    sf.remove(path)
                    q.logger.log('Done removing file with path: %s'%path)
                except:
                    raise RuntimeError("File with path: %s could not be removed\nDetails: %s"%(path, sys.exc_type))
                finally:
                    sf.close()
            else:
                raise RuntimeError("Path: %s is not a file in remote.system.fs.removeFile"%path)
        else:
            raise RuntimeError("Path: %s does not exist in remote.system.fs.removeFile"%path)

    def copyFile(self, fileFrom, fileTo):
        """Copy file

        Copies the file from C{fileFrom} to the file or directory C{to}.
        If C{to} is a directory, a file with the same basename as C{fileFrom} is 
        created (or overwritten) in the directory specified.
        Permission bits are copied.

        @param fileFrom: Source file path name
        @type fileFrom: string
        @param fileTo: Destination file or folder path name
        @type fileTo: string
        
        @raise TypeError: fileFrom or to is empty
        @raise RuntimeError: Cannot copy file
        """
        
        q.logger.log("Copy file from %s to %s" % (fileFrom,fileTo),6)
        if not fileFrom or not fileTo:
            raise TypeError("No parameters given to system.fs.copyFile from %s, to %s" % (fileFrom, fileTo))
        try:
            if self.isFile(fileFrom):
                cmd = 'cp %s %s' % (fileFrom, fileTo)
                self._connection.exec_command(cmd)
            else:
                raise RuntimeError("Cannot copy file, file: %s does not exist in system.fs.copyFile" % fileFrom)
        except:
            raise RuntimeError("Failed to copy file from %s to %s" % (fileFrom, fileTo))

    def isEmptyDir(self, path):
        """Check whether a directory is empty

        @param path: Directory to check
        @type path: string"""

        if not path:
            raise TypeError('Not enough parameters passed to system.fs.isEmptyDir: %s'%path)
        if not self.exists(path):
            raise RuntimeError('Remote path %s does not exist' % path)
        if not self.isDir(path):
            raise RuntimeError('Remote path %s is not a directory' % path)

        sf = self._connection.open_sftp()
        try:
            subcount = sf.listdir(path)
            if len(subcount) == 0:
                return True
            else:
                return False
        finally:
            sf.close()
class RemotePortForwardHander(object):
    
    def __init__(self):    
        # Keep  trac of registered forwards forwards[(server_addr, server_port)] = (local_addr, local_port)
        self.forwards = {}
        
    def accept(self, channel, (origin_addr, origin_port), (server_addr, server_port)):
        q.logger.log('port_forward_handler:accept  New connection: "%s" %s" "%s" "%s" "%s" "%s"' % (id(self), id(channel), origin_addr, origin_port, server_addr, server_port))
        q.logger.log('port_forward_handler:accept  channel.fileno: %s' % channel.fileno())
        
        if not self.forwards.has_key((server_addr, server_port)):
            raise ValueError('Failed to handle RemoteForward: No forward registered for %s.\nRegistered forwards: %s' % (str((server_addr, server_port)), self.forwards))
        
        local_address, local_port = self.forwards[(server_addr, server_port)]
        
        handler_thread = threading.Thread(target = self.handle, args=(channel, local_address, local_port))
        handler_thread.setDaemon(True)
        handler_thread.start()
        
        
    def handle(self, channel, local_address, local_port):
        '''
        Is called from a different thread whenever a forwarded connection arrives.
        '''
        #q.logger.log('port_forward_handler: New connection: "%s" "%s" "%s" "%s" "%s"' % (id(channel), origin_addr, origin_port, server_addr, server_port))
        
        sock = socket.socket()
        try:
            sock.connect((local_address, local_port))
        except Exception, e:
            q.logger.log('port_forward_handler:handle Forwarding request to %s:%d failed: %r' % (local_address, local_port, e), 5)
            return
        
        q.logger.log('port_forward_handler:handle Connected!  Tunnel open %r -> %r' % 
                     (channel.getpeername(), (local_address, local_port)), 5)
        
        while True:
            r, w, x = select.select([sock, channel], [], [])
            if sock in r:
                data = sock.recv(1024)
                if len(data) == 0:
                    break
                channel.send(data)
            if channel in r:
                data = channel.recv(1024)
                if len(data) == 0:
                    break
                sock.send(data)
                
        q.logger.log('port_forward_handler:handle Tunnel closed from %r to %s' % (channel.getpeername(), (local_address, local_port)), 5)

        channel.close()
        sock.close()
        
class RemoteSystemPortForward(_remoteSystemObject):
    
    def __init__(self, client, process):
        """
        Initialize a Remote Port forward system
        """
        
        _remoteSystemObject.__init__(self, client)
        self.process = process
        self.remote_forward_handler = RemotePortForwardHander()
    
    def forwardRemotePort(self, serverPort, remoteHost, remotePort, serverHost='', inThread=False):
        """
        Set up a reverse forwarding tunnel across an SSH server
        
        @param serverPort: port on server to forward (0 to let server assign port)
        @param remoteHost: remote host to forward to
        @param remotePort: remote port to forward to
        @param serverHost: host on the server to bind to
        @param inThread: should we run the forward in a separate thread
        
        @return:            Port number used on ther server
        @rtype:             int
        """
        transport = self._connection.get_transport()
      
        serverPort = transport.request_port_forward(serverHost, serverPort, handler=self.remote_forward_handler.accept)
        
        self.remote_forward_handler.forwards[(serverHost, serverPort)] = (remoteHost, remotePort)
        
        if not inThread:
            while transport.isAlive():
                transport.join(60)
        else:
            return serverPort
    
    def forwardLocalPort(self, localPort, remoteHost, remotePort, inThread=False):
        """
        Set up a forward tunnel across an SSH server
        
        @param localPort: local port to forward
        @param remoteHost: remote host to forward to
        @param remotePort: remote port to forward to
        @param inThread: should we run the forward in a separate thread
        """
        transport = self._connection.get_transport()
        # this is a little convoluted, but lets me configure things for the Handler
        # object.  (SocketServer doesn't give Handlers any way to access the outer
        # server normally.)
        class SubHandler (LocalPortForwardHandler):
            chain_host = remoteHost
            chain_port = remotePort
            ssh_transport = transport
        
        if inThread:
            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            # @todo: Find a way to stop the forward without havinf to stop the process
            server_thread = threading.Thread(target=LocalForwardServer(('', localPort), SubHandler).serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.setDaemon(True)
            server_thread.start()
        else:
            LocalForwardServer(('', localPort), SubHandler).serve_forever()
            
        
        
    
    def cancelForwardRemotePort(self, serverPort):
        """
        Stops any connections from being forwarded using the ssh server on the remote sever port
        
        @param serverPort: the remote port on the server that needs to be canceled
        """
#        transport = self._connection.get_transport()
#        transport.cancel_port_forward('', serverPort)
        pid, output = self.process.getPidForPort(serverPort)
        q.logger.log('PID IS %s and output is %s'%(pid, output))
        if pid != -1:
            exitCode, output = self.process.killProcess(pid)
            if exitCode:
                raise RuntimeError('Failed to cancel remote port forwarding for remote port %s. Reason: %s'%(serverPort, output))
            return True
        raise RuntimeError('Failed to cancel remote port forwarding for remote port %s. Reason: %s'%(serverPort, output))
            
        
    
        
class LocalForwardServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True
            

class LocalPortForwardHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            requestPeername = self.request.getpeername()
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   requestPeername)
        except Exception, e:
            q.logger.log('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                              self.chain_port,
                                                              repr(e)), 5)
            return
        if chan is None:
            q.logger.log('Incoming request to %s:%d was rejected by the SSH server.' %
                    (self.chain_host, self.chain_port), 5)
            return
 
        q.logger.log('Connected!  Tunnel open %r -> %r -> %r' % (requestPeername,
                                                            chan.getpeername(), (self.chain_host, self.chain_port)), 5)
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)
        chan.close()
        self.request.close()
        q.logger.log('Tunnel closed from %r' % (requestPeername,), 5)
