A server extension that mounts a VFS using pylabs_vfs and exposes
the services of the VFS over the network using the python-gevent
networking library 

example application which
* Mounts a VFS on a specified metadata and root directories
* Starts listening to client connections
* Returns results in a dictionary of a 'content' and 'version' format

example application in 
https://bitbucket.org/incubaid/pylabs-core/src/tip/examples/pylabsvfsserver

