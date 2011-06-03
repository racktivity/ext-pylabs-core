[imgdocSpace]: images/images50/installation/docSpace.png


# PyLabs 5 Installation Guide

PyLabs 5 has an installation script that automatically downloads and installs the necessary packages. This section covers preparing for installation, running the installation script itself, and the steps to install a PyLabs 5 sample application, called 'sampleapp'. 


## Prerequisites

* Ubuntu 10.10 64-bit (Maverick Meerkat) - Desktop/Server Edition
* Internet Connection


## Installing PyLabs 5

To install PyLabs 5 only, follow the steps as described below:

1. Get root privileges: `sudo su`\\ \\
2. Launch the installer: `curl http://fileserver.incubaid.com/pylabs5/pylabs5-installer.sh | sh`\\ \\

    curl http://fileserver.incubaid.com/pylabs5/pylabs5-installer.sh | sh
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  2481  100  2481    0     0  19258      0 --:--:-- --:--:-- --:--:-- 20170
    test: 115: xxterm: unexpected operator
    -e Checking if your system version is Ubuntu 10.10 Maverick
    test: 115: xxterm: unexpected operator
    -e Your system is Ubuntu 10.10 Maverick. The install can continue.
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 2384k  100 2384k    0     0  4311k      0 --:--:-- --:--:-- --:--:-- 4439k
    test: 116: xxterm: unexpected operator
    -e Installing ipython python-pkg-resources mercurial python-apt
    Ignoring install-info called from maintainer script
    The package global should be rebuilt with new debhelper to get trigger support
    
    Creating config file /etc/mercurial/hgrc.d/hgext.rc with new version
    test: 116: xxterm: unexpected operator
    -e Adding sitecustomize to system python
    test: 116: xxterm: unexpected operator
    -e Updating Q-Package metadata
     Update metadata information for qpackages domain pylabs5
     * updateqpackage metadata for domain pylabs5                DONE
     Update metadata information for qpackages domain pylabs5_test
     * updateqpackage metadata for domain pylabs5_test           DONE
     Update metadata information for qpackages domain qpackages5
     * updateqpackage metadata for domain qpackages5             DONE
    test: 116: xxterm: unexpected operator
    -e Installing Q-Package pylabs
    lastPackages: [IPackage pylabs5 pylabs 5]
     * Installing QPackage pylabs5 pylabs 5                      RUNNING
     *  Downloading QPackage pylabs5 pylabs 5                    DONE
     * Installing QPackage pylabs5 pylabs 5                      FINISHED
    test: 116: xxterm: unexpected operator
    -e Configuring Q-Packages
    test: 120: xxterm: unexpected operator
    -e Installing Q-Package pyapps_framework
    lastPackages: [IPackage pylabs5 pyapps_framework 0.5]
     * Installing QPackage pylabs5 pyapps_framework 0.5          RUNNING
     *  Installing QPackage pylabs5 alkira 0.5                   RUNNING
     *   Installing QPackage qpackages5 python-pygraphviz
     *    0.99.1                                                 RUNNING
     *    Downloading QPackage qpackages5 python-pygraphviz
     *     0.99.1                                                DONE
    Selecting previously deselected package libcdt4.
    (Reading database ... 146055 files and directories currently installed.)
    Unpacking libcdt4 (from .../libcdt4_2.26.3-4_amd64.deb) ...
    Selecting previously deselected package libcgraph5.
    Unpacking libcgraph5 (from .../libcgraph5_2.26.3-4_amd64.deb) ...
    Selecting previously deselected package libgraph4.
    Unpacking libgraph4 (from .../libgraph4_2.26.3-4_amd64.deb) ...
    Selecting previously deselected package libpathplan4.
    Unpacking libpathplan4 (from .../libpathplan4_2.26.3-4_amd64.deb) ...
   
    ...

    Setting up python-pygresql (1:4.0-2) ...
    Processing triggers for libc-bin ...
    ldconfig deferred processing now taking place
    Processing triggers for python-central ...
      *   Installing QPackage qpackages5 python-pygresql 4.0      DONE
      *   Downloading QPackage qpackages5 postgresql_extension
      *    0.5                                                    DONE
      *  Installing QPackage qpackages5 postgresql_extension 0.5  DONE
      *  Downloading QPackage pylabs5 pyapps_framework 0.5        DONE
      * Installing QPackage pylabs5 pyapps_framework 0.5          FINISHED
    Configuring Q-Packages
      * Configuring QPackage pylabs5 arakoon_client 0.10          DONE
      * Configuring QPackage pylabs5 workflowengine 0.5           DONE
      * Configuring QPackage pylabs5 pyapps_framework 0.5 Writing changes to cmdb
      Writing new configuration to disk
      Cleaning up nginx config
      Cleanup done
              DONE

PyLabs is now installed on your system. In the next section you will see how to install the PyLabs 5 sample application.


## Installing the SampleApp

PyLabs 5 has created a sample PyLabs application (PyApp), called '**sampleapp**'. This is a very basic CRM application, just to show the power of PyLabs.
To install this sample application:

1. Go to the PyLabs root directory: `cd /opt/qbase5/` 
2. Start the Q-Shell: `./qshell` 
3. Find and install the sample application: `i.qp.find('sampleapp').install()` 
4. Make the application available in PyLabs 5: `p.application.install('sampleapp')`

     * Generating base services                                  DONE
     * Generating API for sampleapp application                  RUNNING
     *  Generating action API                                    DONE
     *  Generating actor API                                     DONE
     * Generating API for sampleapp application                  FINISHED
     Writing new configuration to disk
     Cleaning up nginx config
    
    ...
    
     Nginx is starting...
     Nginx started successfully.
     Nginx started successfully
    Starting the workflowengine.
     Waiting for initialization
    Workflowengine started
    
    In [3]:

The sample application is now installed on your system. To access the application, open a web browser and go to:

**http://IpAddress/sampleapp**

where '<ip address>' is the IP address of the machine on which you installed the sample application. If you installed it on a Desktop version, you can go to localhost/sampleapp.


## About the Sample Application
The sample application contains documentation about creating your own PyLabs application. To open the documentation, browse to the sample application.
By default, the '*crm*' space is displayed. Switch the space to '*doc*' to get the PyLabs Application documentation.

![docSpace][imgdocSpace]

Enjoy the power of *PyLabs 5*!
