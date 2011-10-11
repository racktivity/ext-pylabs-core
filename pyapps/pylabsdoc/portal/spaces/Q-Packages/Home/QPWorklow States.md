@metadata title=Workflows and States
@metadata order=58
@metadata tagstring=update qpackage

[imgQPArch2]: images/images50/qpackages/qp5_architecture_2.png

#Workflows and States
This section explains the overall workflow of the qpackages extension and the internal states that control the workflow.
The sections describe:  
* Overview over files and repositories  
* States of a Q-Package    
* Finding the qpackage locations  



##Overview over files and repositories
The graphs shows a general overview over the flows between the files and repositories.  

![Q-Packages_Architecture][imgQPArch2]


***   

##States of a Q-Package
The Pylabs framework has various internal states that control the flow of an Q-Package. These states are represented in a number of configuration files:  



<table border="1" >
  <tr>
    <th>State File</th>
    <th>File Name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>State Config File</td>
    <td>state/.cfg</td>
    <td>Tracks current status of packages that are installed in the framework.</td>
  </tr>
  <tr>
    <td>Metadata Config File</td>
    <td>qpackage.cfg</td>
    <td>Tracks the status of a particular package that is located in the qpackages folder.</td>
  </tr>
  <tr>
    <td>Code Location Config File</td>
    <td>mercurialconnection.cfg</td>
    <td>Network location and credentials for the code repositories.</td>
  </tr>
  <tr>
    <td>Metadata and Bundle Location Config File</td>
    <td>sources.cfg</td>
    <td>Network location and credentials for both the metadata repositories and the ftp bundles repositories.</td>
  </tr>
</table>


***   

####State Config File   (state/.cfg)
The State Config File keeps track of the various (workflow-) states of the installed packages in the framework. In particular, it tracks the current command execution and the current build numbers of packages.

The State Config File is  located at:
`/opt/qbase5/cfg/qpackages4/state/*.cfg`


######Example  
The example below shows the various states that are contained in the file.

[[code]]
[main]
lastdownloadedbuildnr = 7
lastexpandedbuildnr = 7
lastinstalledbuildnr = 7

prepared = 0
ispendingreconfiguration = 0
retry = 0

lastaction = checkout
currentaction = 

lasttag = codemanagement
currenttag =

lastactiontime = 1317299157
currentactiontime = 1317299161
[[/code]]


######Notes  
*  Note how the various build numbers are tracked in the state file.  They control the flow of the installation.  
*  Internally, this is config file is represented in the `class QPackageStateObject()`. 

***   

####Metadata Config File (qpackage.cfg)
The Metadata Config File keeps track of the state a particular package that is installed and used in the qpackage framework.  In particular, it indicates the build number of the package and its bundles.

The metadata config is located in the metadata location of the application:  
`/opt/qbase5/var/qpackages4/metadata/<domain>/<appname>/<version>/qpackage.cfg`

######Example
The example below shows the various states that are contained in the file.

[[code]]
[checksum]
generic = a63e637247fabcde2a52ce400340ef25714fe92da8e168bd5d47d38e55fc6b24

[main]
supportedplatforms = generic, 
tags = 
buildnr = 7
metanr = 0
bundlenr = 7
guid = 739ce4a9-abcde-412a-8b75-224e279f750e
[[/code]]

######Notes:  
*  Note the build number in this file.  It controls the flow of the installation.    
*  Internally, this is config file is represented in the `classs QPackageObject4()`. In the shell, it is accible through the command  `i.qp.lastPackage.package()`  

***   

####Code Location Config File (mercurialconnection.cfg)
This file contains the network location and credentials for the source code of the package.
This information is provided for each Bitbucket repository.

[[code]]
[https___bitbucket_org_incubaid_pylabs_core_]
url = https://bitbucket.org/incubaid/pylabs-core/
destination = /opt/qbase5/var/mercurial/pylabs-core
login = 
passwd = 
[[/code]]

The file is located at `/opt/qbase5/cfg/qconfig/mercurialconnection.cfg`

***   

####Metadata and Bundle Location  Config File  (sources.cfg)
This file contains the network location and credentials for the Bitbucket Metadata repositories and the bundles on the ftp server.
This information is provided for each domain.

[[code]]
[pylabs5]
metadatabranch = default
metadatafromtgz = 0
metadatafrommercurial = https://<login>:<password>@bitbucket.org/incubaid/qp5_-unstable-_pylabs5/
bundledownload = http://fileserver.incubaid.com/pylabs5/bundles
bundleupload = ftp://fileserver.incubaid.com/fileserver/pylabs5/bundles
[[/code]]

The file is located at `/opt/qbase5/cfg/qpackages4/sources.cfg`.

***  

##Finding the qpackage locations
Q-Packages provides standard functions for identifying the various directories.  These directories are used throughout the workflow of Q-Packages.


<table border="1" width="100%">
    <col width="60%" />
    <col width="40%" />

<tr>
    <th>Example Path</td>
    <th>Parameter call</td>
</tr>
<tr>
    <td>/opt/qbase5/</td>
    <td>q.dirs.baseDir </td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4</td>
    <td>q.dirs.packageDir </td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/bundles</td>
    <td>q.qp.getBundlesPath()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/bundles/pylabs5_test/ sampleapp__0.1.2__739ce4a9-xxx9f750e__18__linux.tgz</td>
    <td>i.qp.lastPackage.qpackage. getPathBundle()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/files/pylabs5_test/sampleapp/</td>
    <td>q.qp.getDataPath() </td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/files/pylabs5_test/sampleapp/0.1.2/</td>
    <td>i.qp.lastPackage.qpackage. getPathFiles()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/files/pylabs5_test/sampleapp/0.1.2</td>
    <td>q.qp.getDataPath() </td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/metadata/pylabs5_test/sampleapp/0.1.2</td>
    <td>i.qp.lastPackage.qpackage. getPathMetadata()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/metadata/pylabs5_test/sampleapp/0.1.2</td>
    <td>q.qp.getMetadataPath()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/qpackages4/metatars/pylabs5_test</td>
    <td>q.qp.getMetaTarPath()</td>
    <td></td>
</tr>
<tr>
    <td>/opt/qbase5/var/src/sampleapp/0.1.2</td>
    <td>i.qp.lastPackage.qpackage. getPathSourceCode()</td>
    <td></td>
</tr>
<tr>
    <td>ftp://fileserver.incubaid.com/fileserver/pylabs5_test/bundles</td>
    <td>domain() _getBundleUpload()</td>
    <td></td>
</tr>
<tr>
    <td>sampleapp__0.1.2__739ce4a9-xxx9f750e__18__linux.tgz</td>
    <td>i.qp.lastPackage.qpackage. getBundleName()</td>
    <td></td>
</tr>
<tr>
    <td>http://fileserver.incubaid.com/pylabs5_test/bundles</td>
    <td>domain() _getBundleDownload()</td>
    <td></td>
</tr>
<tr>
    <td>https://<user>:<password>@bitbucket.org/incubaid/qp5_-unst</td>
    <td>domain() _getMetadataFromMercurial()</td>
    <td></td>
</tr>

</table>



