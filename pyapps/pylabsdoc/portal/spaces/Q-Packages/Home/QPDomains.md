[qparchitecture]: /pylabsdoc/#/Q-Packages/QPackageArchitecture

## Q-Package Domains

Q-Packages are gathered per domain to keep their management easy. PyLabs 5 has by default three domains:

* **pylabs5**: the core packages of PyLabs 5
* **pylabs5_test**: domain for testing purposes
* **qpackages5**: domain that contains Q-Packages that are created from open-source packages

The Q-Package domains are defined in the file `sources.cfg`, located in `/opt/qbase5/cfg/qpackages4`.

    # Usernames can be represented as $username_i$ where i is 1 or 2 or 3 .. 9
    # Passwords can be represented as $password_i$ where i is 1 or 2 or 3 .. 9
    
    
    [pylabs5]
    metadatabranch = default
    metadatafromtgz = 0
    metadatafrommercurial = https://bitbucket.org/incubaid/qp5_-unstable-_pylabs5/
    bundledownload = http://fileserver.incubaid.com/pylabs5/bundles
    bundleupload = ftp://fileserver.incubaid.com/fileserver/pylabs5/bundles
    
    [pylabs5_test]
    metadatabranch = default
    metadatafromtgz = 0
    metadatafrommercurial = https://bitbucket.org/incubaid/qp5_-unstable-_pylabs5_test/
    bundledownload = http://fileserver.incubaid.com/pylabs5_test/bundles
    bundleupload = ftp://fileserver.incubaid.com/fileserver/pylabs5_test/bundles
    
    [qpackages5]
    metadatabranch = default
    metadatafromtgz = 0
    metadatafrommercurial = https://bitbucket.org/incubaid/qp5_-unstable-_qpackages5/
    bundledownload = http://fileserver.incubaid.com/qpackages5/bundles
    bundleupload = ftp://fileserver.incubaid.com/fileserver/qpackages5/bundles


#### Domain Details
Let's take `pylabs5` as example to provide more details about a domain.

* **metadatabranch**: the branch for the metadata of the Q-Packages
* **metadatafromtgz**: indicates if the metadata is uncompressed (value: 0) or compressed to a `.tgz` file (value: 1)
* **metadatafrommercurial**: location of the Q-Package metadata in the Mercurial versioning system
* **bundledownload**: location from which the Q-Package bundles are downloaded
* **bundleupload**: location to which the Q-Packages bundles are uploaded when publishing a domain

See the [Q-Packages Architecture][qparchitecture] page for more details about the metadata.
