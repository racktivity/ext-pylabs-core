python fuse implementation which uses
- vfs metadata store (see vfs_metadata extension)

create example app
https://bitbucket.org/incubaid/pylabs-core/src/tip/examples/vfs_fuse_example

* mount an empty filesystem over fuse
* all files writen to fuse filesystem go to small & large file filestore
* all metadata goes to vfs_metadata extension
* goal: people can use standard linux tools to add,remove,modify files on top of the fuse


