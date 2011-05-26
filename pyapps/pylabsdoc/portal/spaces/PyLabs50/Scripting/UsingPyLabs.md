[qshell]: /pylabsdoc/#/PyLabs50/Practical


##Using PyLabs
In the introduction you have seen a first example of a PyLabs script, by means of printing 'Hello World!' on your screen. In this section you find some more practical examples of PyLabs scripts.

[[tip]]
Remember that you can simulate everything in the Q-Shell and call the help function with the question mark
[[/tip]]


###Working with Files and Directories
In the [Q-Shell chapter][qshell] you have seen the basics of file system manipulations via the Q-Shell. Below you can find some more examples.

**Create `tar.gz` File**
Compress a directory (recursively) to a `.tar.gz` file

[[code]]
q.system.fs.targzCompress(?
Definition: q.system.fs.targzCompress(self, sourcedirpath, destinationpath, followlinks=False, destInTar='', pathRegexIncludes=['.[a-zA-Z0-9]*'], pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[], depths=[], extrafiles=[])
Documentation:
    Parameters:
    
    - source_dir: Source directory name.
    - destination: Destination filename.
    - followlinks: do not tar the links, follow the link and add that file or content of directory to the tar
    - pathRegexIncludes: / Excludes  match paths to array of regex expressions (array(strings))
    - contentRegexIncludes: / Excludes match content of files to array of regex expressions (array(strings))
    - depths: array of depth values e.g. only return depth 0 & 1 (would mean first dir depth and then 1 more deep) (array(int))        
    - destInTar: when not specified the dirs, files under sourcedirpath will be added to root of 
    - extrafiles: is array of array [[source,destpath],[source,destpath],...]  adds extra files to tar

q.system.fs.targzCompress('/foo', '/foo/bar.tar.gz')
[[/code]]

The function works in a recursive way.

**Extract `.tar.gz` File**
Extract a `tar.gz` archive to a destination directory:

[[code]]
q.system.fs.targzUncompress(?
Definition: q.system.fs.targzUncompress(self, sourceFile, destinationdir, removeDestinationdir=True)
Documentation:
    compress dirname recursive
    
    Parameters:
    
    - sourceFile: file to uncompress
    - destinationpath: path of to destiniation dir, sourcefile will end up uncompressed in destination dir

q.system.fs.targzUncompress('/foo/bar.tar.gz', '/home/user/Documents')
[[/code]]

**Calculate `md5`**
Calculate the `md5` checksum of a file:

[[code]]
q.system.fs.md5sum(?
Definition: q.system.fs.md5sum(self, filename)
Documentation:
    Return the hex digest of a file without loading it all into memory
    
    Parameters:
    
    - filename: string (filename to get the hex digest of it)

In [77]: q.system.fs.md5sum('/foo/bar.tar.gz')
Out[77]: 'cc37263f7e3139ed178d87ea393d92eb'
[[/code]]

**Get Subdirectories**
Get the list subdirectories in a given directory (non-recursive):

[[code]]
In [92]: q.system.fs.listDirsInDir('/opt/qbase5')
Out[92]: 
['/opt/qbase5/www',
 '/opt/qbase5/utils',
 '/opt/qbase5/var',
 '/opt/qbase5/pyapps',
 '/opt/qbase5/cfg',
 '/opt/qbase5/lib',
 '/opt/qbase5/libexec',
 '/opt/qbase5/bin',
 '/opt/qbase5/apps']
[[/code]]


###File System Walker
In this paragraph we will give you two examples of working with the `fswalker.walk` function. This allows you to recursively walk through a directory and execute commands on the files.

Below you find an example to look up the files with a file size larger than 1MB. Therefore we need to create a function (callback function)

[[code]]
from pylabs.InitBase import *
import os
 
q.application.appname="exampleApp"
q.application.start()
 
def mySpecialDirListLargeFiles(minimumFileSize, filePath):
    if os.path.getsize(filePath) > minimumFileSize:
       print filePath
 
q.system.fswalker.walk('/foo', mySpecialDirListLargeFiles, 1000000)
 
q.application.stop()
[[/code]]

Instead of just showing the files, you can immediately execute commands on the files, for example deleting them. In the example below we will look up all `.pdf` files and delete them.

[[code]]
from pylabs.InitBase import *
import os
 
q.application.appname="deletePdf"
q.application.start()
 
def deletePdf(extension, filePath):
    if os.path.splitext(filePath)[1] == extension:
       q.system.fs.remove(filePath)
 
q.system.fswalker.walk('/foo', deletePdf, '.pdf')
 
q.application.stop()
[[/code]]


###Network Functions
So far we have focused on the PyLabs file system functions. In this paragraph we will show some network functionalities.

**Download Files**
Download a file from an URI or local file path. The supported protocols are `http`, `https`, `ftp`, and `file`.

[[code]]
q.system.net.download('http://foo/bar.tar.gz')
[[/code]]

**Check if a Machine is Online**
A simple test to check if a machine is online, is to ping it:

[[code]]
In [100]: q.system.net.pingMachine('192.168.1.1')
Out[100]: True
[[/code]]

**Get a MAC Address**
PyLabs gives you the possibility to easily retrieve the MAC address of a network interface:

[[code]]
In [101]: q.system.net.getMacAddress('eth0')
Out[101]: 'f0:4d:a2:66:f0:98'
[[/code]]

You can even get the MAC address linked to an IP address:

[[code]]
In [106]: q.system.net.getMacAddressForIp('192.168.16.199')
Out[106]: '08:00:27:d6:30:1a'
[[/code]]

**Check if a Port is Open**
Some services require a TCP/IP port to be open, for example SSH. To check this, you can verify if the port is listening to incoming calls:

[[code]]
In [108]: q.system.process.checkListenPort(?
Definition: q.system.process.checkListenPort(self, port)
Documentation:
    Check if a certain port is listening on the system.
    
    
    Parameters:
    
    - port: sets the port number to check
    
    Returns: status: 0 if running 1 if not running


In [109]: q.system.process.checkListenPort(22)
Out[109]: 0
[[/code]]