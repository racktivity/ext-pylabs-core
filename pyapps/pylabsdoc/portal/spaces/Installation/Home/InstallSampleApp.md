@metadata title=Installing the SampleApp
@metadata order=10
@metadata tagstring=install sampleapp


[imgdocSpace]: images/images51/installation/docSpace.png


# Installing the SampleApp

Pylabs 5 has created a sample Pylabs application (PyApp), called '**sampleapp**'. This is a very basic CRM application, just to show the power of Pylabs.
To install this sample application:

1. Go to the Pylabs root directory: `cd /opt/qbase5/` 
2. Start the Q-Shell: `./qshell` 
3. Find and install the sample application: `i.qp.find('sampleapp').install()` 
4. Make the application available in Pylabs 5: `p.application.install('sampleapp')`

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
The sample application contains documentation about creating your own Pylabs application. To open the documentation, browse to the sample application.
By default, the '*crm*' space is displayed. Switch the space to '*doc*' to get the Pylabs Application documentation.

![docSpace][imgdocSpace]
