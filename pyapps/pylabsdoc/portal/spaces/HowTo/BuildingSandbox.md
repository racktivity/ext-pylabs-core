@todo this content is not up to date, ask Egypte to fix it (look for @todo in page)


## HOWTO Build the sandboxes

Building the sandboxes is still some manual work.
The biggest part is fully automated, but afterward(the cleanup step, is still some manual work)
We have two kind of buildscripts, solaris, linux.
The linux supports normally only 32 and 64 bit, but at this "only 32 bit is tested and used".
Also probably there are a lot of improvements possible.

Before you start you should now the difference between the linux and solaris sandboxes.
The linux contains a full glibc and a gcc compiled with the new glibc, its almost fully sandboxed so every library or application should only be linked against libraries in the sandbox!
Its totally different for solaris, because solaris is one fixed platform(not like linux with different distributions).


### Get the Build Scripts

Create a BUILD directory somewhere on your system(be sure you have enough disk space free).

    mkdir /opt/BUILD

@todo
Export the files with git from

http://staging.pymonkey.org/projects/pymonkey/repos/trunk/trees/master/scripts/sandboxbuildscripts

Be sure there is no old sandbox installed.

    rm -rf /opt/qbase5


### Start Compiling!

The scripts contains for every application and library a build scripts(e.g. bld_sed.sh)
Also a general configuring script is used, to sed the location of the sandbox(e.g `/opt/qbase5`) or set some compile paths.
Its called bld_funcs.
Every build script start loading the bld_funcs script.
To start the build proces run:

    ./bld_all.sh

Start watching a couple of movies, go home or start a other task because this runs for a couple of hours.
Probably you better use a screen session or run the script in the background.


### Cleaning up the Sandbox.

Every install step of a application is installing to much files in the sandbox, afterwards we need to remove some files.

* Static libraries
* c header files (should only be used in the qbase_extra qpackage)
* man/info/... files


### Installing Extra Files in the Sandbox

@todo: check links
* qshell bash script: http://staging.pymonkey.org/projects/pymonkey/repos/trunk/trees/master/scripts/sandboxdefaultcontents/qshell in /opt/qbase5
* ipython initialization script: http://staging.pymonkey.org/projects/pymonkey/repos/trunk/trees/master/scripts/sandboxdefaultcontents/init /opt/qbase5/init
* init_bootstrap script: http://staging.pymonkey.org/projects/pymonkey/repos/trunk/trees/master/scripts/sandboxdefaultcontents/bin/init-bootstrap.sh /opt/qbase5/bin
* utils: http://staging.pymonkey.org/projects/pymonkey/repos/trunk/trees/master/utils in utils/
* config directory: create a directory cfg/qconfig/, create a new file main.cfg, which contains following entries

    [main]
    autonomous_installation = False
    logserver_loglevel = 6
    logserver_port = 9998
    logserver_ip = 127.0.0.1
    qshell_firstrun = True

* pymonkey, latest pymonkey egg should be installed in /opt/qbase3/lib/pymonkey/core/ 
* sitecustomze.py should be saved in /opt/qbase3/lib/python2.5/ and can be found in http://staging.pymonkey.org/projects/pymonkey/repos/trunk/blobs/master/scripts/sitecustomize.py


### Package the Sandbox

Create a tar file of the sandbox contents:

    tar -cvzf qbaseSandbox_3.0-small-linux.tar.gz qbase3

