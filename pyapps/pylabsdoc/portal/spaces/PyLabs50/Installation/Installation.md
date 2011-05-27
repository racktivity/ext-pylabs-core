[imgdocSpace]: images/images50/installation/docSpace.png


# PyLabs 5 Installation Guide

PyLabs 5 has an installation script that automatically downloads and installs the necessary packages. This section covers preparing for installation, running the installation script itself, and the steps to install a PyLabs 5 sample application, called 'sampleapp'. 


## Prerequisites

* Ubuntu 10.10 64-bit (Maverick Meerkat) - Desktop/Server Edition
* Internet Connection


## Installing PyLabs 5

To install PyLabs 5 only, follow the steps as described below:

1. In shell: `wget http://fileserver.incubaid.com/pylabs5/pylabs5-installer.sh`
2. Get root privileges: `sudo su`\\ \\
3. Update the properties of the installer to make it executable: `chmod a+x pylabs5-installer.sh` \\ \\
4. Launch the installer: `./pylabs5-installer.sh`\\ \\

    Checking if your system version is Ubuntu 10.10 Maverick
    Your system is Ubuntu 10.10 Maverick. The install can continue.
    Exctracting base layout
    Installing ipython python-pkg-resources mercurial python-apt
    Adding sitecustomize to system python
    Updating Q-Package metadata
    Update metadata information for qpackages domain pylabs5
    * updateqpackage metadata for domain pylabs5hg clone 'https://bitbucket.org/incubaid/qp5_-unstable-_pylabs5/' . -r default
                    DONE

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
