@metadata title=Q-Package Architecture
@metadata order=20
@metadata tagstring=architecture q-package package

[Confluence]: http://www.atlassian.com/software/confluence/
[imgQPArch]: images/qpackages/qp5_architecture.gif


# Q-Packages Architecture

The Q-Package framework consists of different components as shown in the image below:

![Q-Packages_Architecture][imgQPArch]

The core of the Q-Package framework is `qbase`, which is logical since the Q-Package framework is part of the PyLabs 5 framework.
As input for a Q-Package, you have source code repositories, here displayed as `mercurial`. 

A `mercurial` instance exists in the Q-Package framework as Q-Package metadata repository. In the framework there is a special Q-Package directory structure from where you can publish or install the Q-Packages.


## Q-Package Directory Structure

    /opt/qbase5/var/qpackages4/
    |
    |-- bundles
    |   |-- domain1
    |   |   |-- bundle1.tgz
    |   |   |
    |   |   |-- <...>
    |   |   |
    |   |   `-- bundleX.tgz
    |   |
    |   |-- <...>
    |   |
    |   `-- domainX
    |
    |-- files
    |   |-- domain1
    |   |   |-- package1
    |   |   |   `-- <version>
    |   |   |       `-- <platform>
    |   |   |           `-- <application dir structure>
    |   |   |
    |   |   |-- <...>
    |   |   |
    |   |   `-- packageX
    |   |
    |   |-- <...>
    |   |
    |   `-- domainX
    |
    `-- metadata
        |-- domain1
        |   |-- package1
        |   |   `-- <version>
        |   |       |-- description.wiki
        |   |       |-- qpackage.cfg
        |   |       `-- tasklets
        |   |           |-- backup.py
        |   |           |-- codemanagement.py
        |   |           |-- configure.py
        |   |           |-- install.py
        |   |           |-- package.py
        |   |           `-- startstop.py
        |   |
        |   |-- <...>
        |   |
        |   `-- packageX
        |
        |-- <...>
        |
        `-- domainX


## What's in the Directories?
In the above schema, you see the complete directory structure, related to Q-Packages. In this section you find the details of the different directories and files, also with their relationship with the components of the framework overview image.

* *bundles*: the bundles directory contains the applications in an archived format. The archives are published on an FTP server.
** *domain*: the domain to which the Q-Package belongs

* *files*: matches with the `qpackagesfiles directory` in the framework overview image. This directory contains the different domains, hosted for PyLabs 5
** *domain*: the domain to which the Q-Package belongs
** *package*: name of the Q-Package, mainly this is identical to the name of the application it comprises
** *version*: version of the Q-Package, sometimes replaced by the version of an open-source package
** *platform*: name of the platform on which the package will be installed

In the `platform` directory you create the directory-structure of your application as it should be deployed in the base directory of PyLabs 5, `/opt/qbase5`.

* *metadata*: matches with the `metadatarepository` in the framework overview images. This directory contains the configuration and installation files of the Q-Package
** *domain*: the domain to which the Q-Package belongs
** *package*: name of the Q-Package, mainly this is identical to the name of the application it comprises
** *version*: version of the Q-Package, sometimes replaced by the version of an open-source package
** *description.wiki*: [Confluence][] wiki file containing a brief description of the Q-Package
** *qpackage.cfg*: configuration file of the Q-Package, containing general Q-Package information and dependencies to other Q-Packages
** *tasklets*: this directory contains the tasklets that configures and manages the Q-Package