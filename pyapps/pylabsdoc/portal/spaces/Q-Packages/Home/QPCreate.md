@metadata title=Creating a Q-Package
@metadata order=40
@metadata tagstring=create tasklet package

[qptasklets]: /#/Q-Packages/QPTasklets
[qpcreatebinary]: /#/Q-Packages/QPCreatebinary


# Creating a Q-Package

A Q-Package is a package that you install in PyLabs 5.
Each Q-Package is defined by the domain it belongs to, by its name and by its version. A build number further specifies the build of the Q-Package, but no Q-Packages that only differ in the build number can coexist on the same system.

A Q-Package consist of two parts:

* files: can be self-created files (executables, scripts, source files, ...) or files which are stored on a version controlled system, such as Mercurial, Git, Bazaar...
* metadata

Metadata consists of:

* a description
* a configuration file
* tasklets: small pieces of code which execute tasks for easier management of the Q-Package


## Overview Steps of Creating a Q-Package
Below you can find the subsequent steps to create a Q-Package:

1. Create an empty Q-Package in a domain on the system repository (/opt/qbase5/var/qpackages4)
2. Create the necessary tasklets: backup, codemanagement, configure, install, package, startstop, and optionally compile
3. Get the necessary code, and then compile, package, install, and optionally configure the application
    * Get the code or executables for your Q-Package from BitBucket or any other source and if necessary compile it. This is done by running the codemanagement and compile tasklets
    * Put all the executables in the system repository with the package tasklet
    * Install the Q-Package files in PyLabs with the install tasklet, optionally configure the application
4. Update the metadata and publish the Q-Package on the Q-Package Server specified for your domain

    **Important**
    During the complete process of creating a Q-Package, leave the Q-Shell session open!


## Creating a Q-Package
To create a Q-Package on your local workstation:

1. Create a new Q-Package:

    In [1]: i.qp.createNewPackage()
     Please select a domain
        1: pylabs5
        2: pylabs5_test
        3: qpackages5
        Select Nr (1-3): 2
    Please provide a name: testqp
    Please provide a version [1.0]: 
    Please provide a description: test
     Please enumerate the supported platforms
        1: generic
        2: unix
        3: linux
        4: linux32
        5: linux64
        6: win
        7: win32
        8: win64
        9: solaris
        10: solaris32
        11: solaris64
        12: esx
        13: cygwin
        14: darwin
        15: other
        Select Nr, use comma separation if more e.g. "1,4": 1
    lastPackages: [IPackage pylabs5_test testqp 1.0]
    Out[1]: IPackage pylabs5_test testqp 1.0
    
    In [2]:
2. Check in your PyLabs directory if the new package is created:

    /opt/qbase5/var/qpackages4/files/pylabs5_test/testqp/1.0
    /opt/qbase5/var/qpackages4/metadata/pylabs5_test/testqp# tree
    .
    `-- 1.0
        |-- description.wiki
        |-- qpackage.cfg
        `-- tasklets
            |-- backup.py
            |-- codemanagement.py
            |-- configure.py
            |-- install.py
            |-- package.py
            `-- startstop.py
    
    2 directories, 8 files
3. If your application needs other Q-Packages for correct functioning, you can add dependencies. The Q-Packages that you define, will be installed automatically when you install this new Q-Package:

    In [2]: i.qp.lastPackage.addDependency()
     Please select a domain
        1: pylabs5
        2: pylabs5_test
        3: qpackages5
        Select Nr (1-3): 2
    Please provide a name for the dependency: test2
     Please provide a comma separated list of supported platforms
        1: generic
        2: unix
        3: linux
        4: linux32
        5: linux64
        6: win
        7: win32
        8: win64
        9: solaris
        10: solaris32
        11: solaris64
        12: esx
        13: cygwin
        14: darwin
        15: other
        Select Nr, use comma separation if more e.g. "1,4": 1
    Please provide a minimum version, eg: 1.2: 1.0
    Please provide a maximum version, eg: 2.5: 3.0
     Please select a dependencytype
        1: build
        2: runtime
        Select Nr (1-2): 1
    
    In [3]:


The last question when adding a dependency sets a dependency type:

* *build*: indicates that the selected Q-Package is only needed to build your Q-Package
* *runtime*: indicates that the selected Q-Package is required to make your Q-Package functional, and thus must be installed together with your Q-Package


## Create the necessary tasklets
Default tasklets have been generated when the Q-Package was created. Now is the time to customize the appropriate tasklets.
For more info see [Q-Package Tasklets][qptasklets].


## Building the Q-Package

Make sure that you have correctly created the [codemanagement][qptasklets] tasklet. To execute the `codemanagement` tasklet, call the `checkout` method on your new Q-Package object:

    i.qp.lastPackage.checkout()
     Username for mercurial connection: your_username
    Password for mercurial connection: your_password
    Destination folder to clone repository [/opt/qbase5/var/mercurial/pylabs-core]: 

The destination folder of the cloned repository is very important for the further creation of the Q-Package. In the `package` tasklet you will have to refer to this folder.


[[tip]]
**Tip**

Most of the generated tasklets start with the line `qpackage = params['qpackage']`. If you want to simulate this `qpackage` object in your Q-Shell session, execute this line in the Q-Shell:

	In [1]: qpackage = i.qp.find("packagename").qpackage
	lastPackages: [IPackage <package domain> <package name> <package version>]

or if you have stored your new Q-Package object in a variable:

	In [1]: newQPackage = i.qp.createNewPackage()
	
	In [2]: newQPackage = newQPackage.qpackage
[[/tip]]

Instead of calling this `checkout` method, you can also manipulate the Q-Package directories, by creating your own directory-structure and putting your files in the proper directories.

If you need to compile your code against the PyLabs framework, make sure that you have correctly created the [compile][qptasklets] tasklet. The compile tasklet is mainly used for [binary Q-Packages][qpcreatebinary].
To execute the `compile` tasklet, call the `compile` method on your Q-Package object:


    i.qp.lastPackage.compile()

In a last step, you have to put all the files from the source directories (via the `checkout`) to the proper location in the PyLabs sandbox. Therefore you have to execute the [package][qptasklets] tasklet by calling the `package` method on the Q-Package object:

    i.qp.lastPackage.package()

[[tip]]
**Tip**

These three above described steps (checkout, compile, and package) are all automated in one method, `quickPackage()`.
[[/tip]]


## Publishing the Q-Package
In the previous sections you have learned to create a Q-Package. A last step is to publish the new Q-Package in the domain, in order to become available to other users.

To publish a new Q-Package you publish a domain. This action executes the following steps:

1. detect new Q-Package(s) in the domain
2. create a bundle of the of the Q-Package(s)
3. upload the metadata of the Q-Package(s) to the Mercurial servers (configured in `/opt/qbase5/cfg/qpackages4/sources.cfg`)
4. upload the bundle(s) to the Q-Packages FTP server (configured in `/opt/qbase5/cfg/qpackages4/sources.cfg`)

To publish the domain:

    i.qp.publishDomain('<domain name>', commitMessage='<your commitmessage here>')

    #for example
    In [5]: i.qp.publishDomain('pylabs5_test', commitMessage='demo package')
     Publish metadata for qpackage domain: pylabs5_test 
     The following packages will be published:
     publishing packages for domain pylabs5_test:
         domain:        name:          version:       metachanged:   fileschanged:  status:        
         pylabs5_test   testqp         1.0            True           True           NEW            
    continue? (y/n):y
     1) Updating buildNumbers in metadata and uploading files
     * updateqpackage metadata for domain pylabs5_test 
     
     Found files not added yet to repo or deleted from filesystem
     Nottracked/Ignored: pylabsdoc/5.0/description.wiki
     Nottracked/Ignored: pylabsdoc/5.0/qpackage.cfg
     Nottracked/Ignored: pylabsdoc/5.0/recipe.json
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/backup.py
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/codemanagement.py
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/configure.py
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/install.py
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/package.py
     Nottracked/Ignored: pylabsdoc/5.0/tasklets/startstop.py
     
     \Above files are not added yet to repo but on filesystem
     What do you want to do with these files
        1: RemoveTheseFiles
        2: AddRemove
        3: Abort
        Select Nr (1-3): 2
     
     Found modified, added, deleted files not committed yet
     Added:    pylabsdoc/5.0/description.wiki
     Added:    pylabsdoc/5.0/qpackage.cfg
     Added:    pylabsdoc/5.0/recipe.json
     Added:    pylabsdoc/5.0/tasklets/backup.py
     Added:    pylabsdoc/5.0/tasklets/codemanagement.py
     Added:    pylabsdoc/5.0/tasklets/configure.py
     Added:    pylabsdoc/5.0/tasklets/install.py
     Added:    pylabsdoc/5.0/tasklets/package.py
     Added:    pylabsdoc/5.0/tasklets/startstop.py
      
    Do you want to commit the files? (y/n):y
    user: your_username
    password: your_password

