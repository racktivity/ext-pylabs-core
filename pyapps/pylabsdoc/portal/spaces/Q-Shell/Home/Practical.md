@metadata title=Using Q-Shell
@metadata order=20
@metadata tagstring=practical usage qshell script file system directories network

[fswalker]: #/Scripting/UsingPyLabs

#Using the Q-Shell
In the previous sections you have learned how to work with the Q-Shell and what the principles are.
In this section you will get some more practical examples to use the Q-Shell.

Q-Shell can interact with the OS which hosts PyLabs. For example you can create new directories, copy files, and various other file system commands.
All operating system commands are located under `q.system.` in the Q-Shell. 
* file system commands:`q.system.fs`, for example copy files, create directories, ...
* OS process commands:`q.system.process`, for example check if process is alive, kill processes, ...
* networking commands: `q.system.net`, for example ping a machine, get MAC address, ...
* unix commands: `q.system.unix`, for example create users, create groups, ...
* file system walker: `q.system.fswalker`, for example browse through directories and list specific files while browsing


##Working with Files and Directories
Below you find various Q-Shell commands and its output. More examples can be found in the [Scripting chapter][fswalker].

**Copy File**

[[code]]
    $ ls /opt
    code  pylabs5-installer.sh  qbase5
    
    $ ls
    apps  bin  cfg  lib  libexec  pyapps  qshell  test.py  utils  var  www
    
    In [1]: q.system.fs.copyFile(?
    Definition: q.system.fs.copyFile(self, fileFrom, to)
    Documentation:
        Copy file
        
        Copies the file from fileFrom to the file or directory to.
        If to is a directory, a file with the same basename as fileFrom is
        created (or overwritten) in the directory specified.
        Permission bits are copied.
        
        
        Parameters:
        
        - fileFrom: Source file path name
        - to: Destination file or folder path name
    
    
    In [2]: q.system.fs.copyFile('test.py', '/opt')
    
    $ ls /opt
    code  pylabs5-installer.sh  qbase5  test.py
[[/code]]


**Copy Full Directory**

[[code]]
    $ ls /opt
    code  pylabs5-installer.sh  qbase5  test.py
    
    $ ls pyapps/
    __init.py__  sampleapp
    
    
    In [1]: q.system.fs.copyDirTree(?
    Definition: q.system.fs.copyDirTree(self, src, dst, keepsymlinks=False, overwriteDestination=False)
    Documentation:
        Recursively copy an entire directory tree rooted at src.
        The dst directory may already exist; if not,
        it will be created as well as missing parent directories
        
        Parameters:
        
        - src: string (source of directory tree to be copied)
        - dst: string (path directory to be copied to...should not already exist)
        - keepsymlinks: bool (True keeps symlinks instead of copying the content of the file)
        - overwriteDestination: bool (Set to True if you want to overwrite destination first, be carefull, this can erase directories)
    
    
    In [2]: q.system.fs.copyDirTree('pyapps', '/opt')
    
    $ ls /opt
    code  __init.py__  pylabs5-installer.sh  qbase5  sampleapp  test.py
[[/code]]

The content of the `pyapps` directory (`__init.py__` and `sampleapp` directory) is copied to `/opt`.


**Working with Directories**
In the `q.dirs` name space you can get the paths to default PyLabs system directories, for example the `bin` or `pyapps` directory.

[[code]]
    In [9]: q.dirs.binDir
    Out[9]: '/opt/qbase5/bin'
    
    In [10]: q.dirs.pyAppsDir
    Out[10]: '/opt/qbase5/pyapps'
[[/code]]

With these functions it is easy to create new directories or copy files to PyLabs system directories.

To create a new directory names to combine various names, use the `q.system.fs.joinPaths` function:

[[code]]
    In [11]: q.system.fs.joinPaths(?
    Definition: q.system.fs.joinPaths(self, *args)
    Documentation:
        Join one or more path components.
        If any component is an absolute path, all previous components are thrown away, and joining continues.
        
        Parameters:
        
        - path1: string
        - path2: string
        - path3: string
        - ....: : string
[[/code]]

In the next example we create a new directory `test` in the `pyapps` directory:

[[code]]
    In [12]: newDir = q.system.fs.joinPaths(q.dirs.pyAppsDir,'test')
    
    In [13]: q.system.fs.createDir(?
    Definition: q.system.fs.createDir(self, newdir)
    Documentation:
        Create new Directory
        
        Parameters:
        
        - newdir: string (Directory path/name)
        
    In [14]: q.system.fs.createDir(newDir)
    
    $ ls pyapps
    __init__.py  sampleapp  test
[[/code]]

**Find Files Recursively
Q-Shell contains the function, `fswalker`, which looks up files in a recursive way. You only need to enter the path from which the function must start. As a result you get a list of all the files.
To this function you can add several options to include or exclude files.

[[code]]
    In [8]: q.system.fswalker.find(?
    Definition: q.system.fswalker.find(root, recursive=True, includeFolders=False, pathRegexIncludes=['.*'], pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[], depths=[])
[[/code]]

Instead of just looking up the files, the `fswalker` can also execute an action on the retrieved files.

[[code]]
    In [15]: q.system.fswalker.walk(?
    Definition: q.system.fswalker.walk(root, callback, arg='', recursive=True, includeFolders=False, pathRegexIncludes=['.*'], pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[], depths=[], followlinks=True)
    Documentation:
        Walk through filesystem and execute a method per file
        
        Walk through all files and folders starting at root, recursive by
        default, calling a given callback with a provided argument and file
        path for every file we could find.
        
        If includeFolders is True, the callback will be called for every
        folder we found as well.
        
            Parameters:
        
        - root: Filesystem root to crawl (string)
        - callback: Callable to call for every file found, func(arg, path) (callable)
        - arg: First argument to pass to callback
        - recursive: Walk recursive or not (bool)
        - includeFolders: Whether to call callable for folders as well (bool)
        - pathRegexIncludes: / Excludes  match paths to array of regex expressions (array(strings))
        - contentRegexIncludes: / Excludes match content of files to array of regex expressions (array(strings))
        - depths: array of depth values e.g. only return depth 0 & 1 (would mean first dir depth and then 1 more deep) (array(int))
[[/code]]

See [the Scripting Chapter][fswalker] for examples of this function.


##Some Other OS Examples

**Networking**
Ping a machine:

[[code]]
    In [3]: q.system.net.pingMachine('192.168.16.213')
    Out[3]: True
[[/code]]
    
Get the default gateway:

[[code]]
    In [5]: q.system.net.getDefaultRouter()
    Out[5]: '192.168.16.254'
[[/code]]
    
Show available network interfaces and their type:

[code]]
    In [1]: nics = q.system.net.getNics()
    
    In [2]: for nic in nics:
       ...:     print "%s - %s"%(nic, q.system.net.getNicType(nic))
       ...:     
       ...:     
    lo - VIRTUAL
    vboxnet0 - VIRTUAL
    eth1 - ETHERNET_GB
    eth0 - ETHERNET_GB
[[/code]]
    
**Unix**
Available actions for Unix systems:

[[code]]
    In [6]: q.system.unix.
    q.system.unix.addCronJob(           q.system.unix.executeDaemonAsUser(
    q.system.unix.addSystemGroup(       q.system.unix.getBashEnvFromFile(
    q.system.unix.addSystemUser(        q.system.unix.getMachineInfo(
    q.system.unix.chmod(                q.system.unix.killGroup(
    q.system.unix.chown(                q.system.unix.removeUnixUser(
    q.system.unix.chroot(               q.system.unix.setUnixUserPassword(
    q.system.unix.daemonize(            q.system.unix.unixGroupExists(
    q.system.unix.disableUnixUser(      q.system.unix.unixUserExists(
    q.system.unix.enableUnixUser(       q.system.unix.unixUserIsInGroup(
    q.system.unix.executeAsUser(
[[/code]]


**Unix Processes**
Available process actions:

[[code]]
    In [6]: q.system.process.
    q.system.net.checkListenPort(
    q.system.process.checkProcess(
    q.system.process.checkProcessForPid(
    q.system.process.execute(
    q.system.process.executeAsync(
    q.system.process.executeInSandbox(
    q.system.process.executeScript(
    q.system.process.executeWithoutPipe(
    q.system.process.getProcessByPort(
    q.system.process.isPidAlive(
    q.system.process.kill(
    q.system.process.run(
    q.system.process.runDaemon(
    q.system.process.runScript(
    q.system.process.setEnvironmentVariable(
[/code]]

For example check if a port is opened:

[[code]]
    In [7]: q.system.net.checkListenPort(?
    Definition: q.system.net.checkListenPort(self, port)
    Documentation:
        Check if a certain port is listening on the system.
        
        
        Parameters:
        
        - port: sets the port number to check
        
        Returns: status: True if running False if not running
        
    In [8]: q.system.net.checkListenPort(22)
    Out[8]: True
[[/code]]
    
More practical information can be found in the examples of creating scripts.    
