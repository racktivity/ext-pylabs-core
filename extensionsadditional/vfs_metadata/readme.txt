filesystem part of virtual filesystem
stores all metadata in keyvalue store
has functions for walk, compare, read from filesystem, ...

example application which
* reads normal filesystem into the vfs metadata store
* does some operations on vfs metadata like search
* change some files to filesystem
* and build new vfs metadata store out of changed filesystem
* compare vfs metadata store 2 with metadata store 1, see what changed files are

example application in 
https://bitbucket.org/incubaid/pylabs-core/src/tip/examples/vfsmetadata

