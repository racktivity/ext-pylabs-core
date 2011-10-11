@metadata title=Details of Main Functions
@metadata order=60
@metadata tagstring=update qpackage








#Details of the main functions
This section explains in detail the main functions of the Q-Package extension that are used in the typical workflows.  In addition, it explains the states that control the workflow.  
The sections describe:  
* Main functions for working with Q-Packages     
* Related functions

***   

##Main Functions for working with Q-Packages
This section explains in details the most important functions of the Q-Package extension.
These functions are: 
  
Initial step:  
`updateMetaDataAll()`  

Create new version:  
`prepareForUpdatingFiles()`  
`checkout()`    
`package()`  
`publishAll()`  

Install the new version:  
`install()`  

***  

####updateMetaDataAll()

######Related Function
`updateMetaDataForDomain()`

######Function
Updates all files in the Metadata directory of the framework with the head revision of the Bitbucket repo.
`/opt/qpabase/var/qpackages4/metadata/`

######Input  
Uses connection information and credentials for Bitbucket and ftp server in:
`/opt/qbase/cfg/qpackages/sources.cfg`

Uses connection information and credentials for Bitbucket in:
`/opt/qbase/cfg/qconfig/mercurialconnection.cfg`

Note: These files may get modified when executing this function.

######Actions
* Update the metadata directory from the head revision from the Bitbucket repo.  
* Try to handle local changes in the metadata repository (merge, etc.) but this may fail in some non-standard cases. 
* May perform a local commit if there are local changes or merges.  This commit is NOT pushed to the repo.

***  

####prepareForUpdatingFiles()
######Function
This puts the package in a state where it can be updated within the sandback by the developer
The files can be updated "manually" in the qpackages-file directory:
`/opt/qpabase/var/qpackages4/files`

######Output
* sets the parameter in the State Config file  `prepared = 1`
* creates the qpackage file directory if it is not yet existing:   
`/opt/qbase5/var/qpackages4/files/<domain>/<appname>/<version>/`
* generates the standard tasklets

Note: 
* Unexpectedly, this function also updates  the State Config File with the latest build numbers
`lastdownloadedbuildnr` and `lastexpandedbuildnr`.  This compensates a little inconsistency in the publishDomain() function (_compress,_upload) where these numbers are not updated.

***  

####checkout()
######Function
Pulls the code files from the Bitbucket package repository to the source files location (`getPathSourceCode()`).
`/opt/qbase5/var/src/`

######Input
The function prevents double execution by checking the parameter `lastaction` in the State Config File.

Uses connection information and credentials for Bitbucket in:
`/opt/qbase/cfg/qpackages/sources.cfg`

Uses connection information and credentials for Bitbucket in:    (to be confirmed)
`/opt/qbase/cfg/qconfig/mercurialconnection.cfg`

The checkout uses the recipe.json file.

######Action
This function executes the `Codemanagement` tasklet, typically using the recipe.json file.

First, it performs an Mercurial checkout/update into  `/opt/qbase5/var/mercurial/<reponame>`.
Second, it copies the files to the source file location `/opt/qbase5/var/src`  (existing folders are deleted).

Note: This function does NOT copy files to the qpackage file directory nor to the target location in the framework.

######Output
The files are placed to the source files location.

Note: The build number remains unchanged.

***  

####package()
######Function
Copies files to the qpackage file location by calling the ´package´ tasklet.

######Input
* Checks if the parameter in the State Config file `prepared = 1`  . Otherwise the function does not execute.

######Action
Typically, the tasklet is configured to remove the old files in the qpackage file folder (`getPathFiles()`) and copies to this location the new files from the source location (`getPathSourceCode()`).

######Output
Files are at the new qpackage file location.

Note: The build number remains unchanged.

***  

####publishAll()

######Related Function
`publishDomain()`

######Function
Makes all packages available for general use by updating the Bitbucket metadata repositories and loading the packages (bundle) to the ftp server.
This command works on all packages of a domain, either on a specified domain or on all domains.
A domain can be changed in the following ways: a new package is created in it, a package in it is modified, a package in it is deleted.


######Input
Check that metadata is comming from repository (and not from tgz).  
Check that the bundleUpload ftp server location is specified.

######Actions
1. Check if the metadata or the files have been modified, added or deleted.
2. Display the results, and confirm interactively if the actions should continue.
3. Update metadata from repository.
4. Increments the build number.  (This is the only place that the build number is incremented).
5. Compresses the package and uploads the resulting bundle to the ftp server.
6. Publishes the metadata.
7. Resets the parameter `prepared` in the State Config file to `prepared = 0`.
8. Handling of branches other than `default`.


######Output
This function results in major modifications in the file systems and the repositories (see Actions).

***  

####install()
######Function   
This function identifies the (latest) build number of the package metadata and takes all steps necessary to install this version in the framework.
For this, it may download and expand the tar from the ftp server.

######Preconditions
If the package is installed, it is assumed that the dependent packages are also already installed (This needs to be considered if there are updates of the dependent packages).   
The install function requires that the metadata have been published (with `publishAll()`).  Otherwise, install will not perform any actions.

######Actions
* Download file from ftp to the bundle directory.  
* Expand the bundle to the qpackage directory.  
* Copy the application to the target location in the framework.  
* Update the status in the State Config file (e.g. build numbers).  

######Prevention of Re-install
The system prevents repeated execution of an install.  It remembers the buildnumber after each install and checks if the new buildnumber is actually higher than the one that is already installed.  Otherwise, no action is performed.

For this purposes it stores the following values in the State Config file.
[[code]]
lastdownloadedbuildnr = 7
lastexpandedbuildnr = 7
lastinstalledbuildnr = 7
lastaction = install
[[/code]]

(See also `reinstall()` below).

######Notes
* In the State Config File, the parameter `current actions` needs to be empty. Otherwise the system is in an inconsistent state and the install will not execute.
* The user can overwrite the standard behaviour by using the following function:  
`q.qp.lastpackage.qpackage.install(dependencies = True/False,  download = True/False,  reinstall = True/False)`  
The parameters may force the loading of dependent packages or block the downloading of already existing bundles.

***   

##Related Functions

####reinstall()
######Function
Installs the package even if the build numbers already match.
This is done by overwriting the standard ´install()´ function with an extra parameter `install(reinstall=True)`.

Note:
Internally, the qpackage function is called with a modified `reinstall` parameter: `q.qp.lastpackage.qpackage.install(reinstall=True)`

***   

####copyFiles() in qpackage object
######Function
Copies the files from the qpackages file directory to the target location in the framework.

This function is aware of the system platform `q.platform` and selects the installed files accordingly.

This function is typically called by the `install()` tasklet.

***   


####updateAll()
######Function
Downloads and installs the latest versions (i.e. build numbers) of all installed packages.

######Actions
* execute updateMetaDataAll()   
* selects all installed packags and versions, based on the qpackages metadata repository
* performs an install on all packages

* Note: (Re-)Install of already installed build numbers is routinely prevented by the standard `install()` function.  This functions compares the installed build number with the latest build number from the metadata.  If they already match, no actions are performed.

######Notes
In case multiple versions of the same package are installed, each version is updated to its latest build number.

***   

####quickPackage()
######Function
Performs als steps needed to create a new build for an already existing package.  It gets the code files from the Bitbucket repositories and places them in the qpackages files folder.

######Input
The function uses the metadata information.  For that reason, the command `updateMetaDataAll()` should be used in advance.

######Actions
`* prepareForUpdatingFiles()`  
`* checkout()`
`* compile()`
`* package()`

######Output
The code from the repository is located in the qpackages files directory.

#####Note
After this command, it is necessary to run a `publishDomain()`. Otherwise the metadata is not updated and the subseqent `install()` will not perform any actions.

***   

####printConfig()
Prints the content of the configuration file _Metadata and Bunle Location Config File_ (see above).

The file is located at `/opt/qbase5/cfg/qpackages4/sources.cfg`.


