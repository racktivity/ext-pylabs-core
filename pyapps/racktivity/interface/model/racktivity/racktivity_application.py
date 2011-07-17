from enumerations import *
import pymodel as model

# @doc None
class service2resourcegroup(model.Model):

    #@doc guid of the resourcegroup using this service
    resourcegroup = model.GUID(thrift_id=1)

    #@doc remarks on service usage by application
    remark = model.String(thrift_id=2)


# @doc application using a certain service
class service2application(model.Model):

    #@doc guid of the application using this service
    applicationguid = model.GUID(thrift_id=1)

    #@doc remarks on service usage by application
    remark = model.String(thrift_id=2)


# @doc None
class service2device(model.Model):

    #@doc device using this service
    deviceguid = model.GUID(thrift_id=1)

    #@doc remarks
    remark = model.String(thrift_id=2)


# @doc None
class service2networkzone(model.Model):

    #@doc guid of the networkzone using this service
    networkzoneguid = model.GUID(thrift_id=1)

    #@doc None
    remark = model.String(thrift_id=2)


# @doc None
class service2machine(model.Model):

    #@doc guid of the machine using this service
    machineguid = model.GUID(thrift_id=1)

    #@doc remarks on service usage by application
    remark = model.String(thrift_id=2)


# @doc None
class service2clouduser(model.Model):

    #@doc clouduser using this service
    clouduserguid = model.GUID(thrift_id=1)

    #@doc remarks
    remark = model.String(thrift_id=2)


# @doc None
class service2lan(model.Model):

    #@doc guid of the lan using this service  e.g. for portforwarding
    languid = model.GUID(thrift_id=1)

    #@doc None
    remark = model.String(thrift_id=2)


# @doc None
class service2disk(model.Model):

    #@doc disk using this service
    diskguid = model.GUID(thrift_id=1)

    #@doc remarks
    remark = model.String(thrift_id=2)
    
    #@doc partition order (eg for mountpoints)
    partitionorder = model.Integer(thrift_id=3)
    

# @doc service offered by an application. Applications can offer various services, on different ports.
class service(model.Model):

    #@doc flag indicating if the service is enabled
    enabled = model.Boolean(thrift_id=1)

    #@doc remark on service
    description = model.String(thrift_id=2)

    #@doc name of service
    name = model.String(thrift_id=3)

    #@doc list of resourcegroups using this service
    service2resourcegroups = model.List(model.Object(service2resourcegroup),thrift_id=4)

    #@doc list of applications using this service
    service2applications = model.List(model.Object(service2application),thrift_id=5)

    #@doc list of devices using this service
    service2devices = model.List(model.Object(service2device),thrift_id=6)

    #@doc list of networkzones using this service
    service2networkzones = model.List(model.Object(service2networkzone),thrift_id=7)

    #@doc list of machines using this service
    service2machines = model.List(model.Object(service2machine),thrift_id=8)

    #@doc list of cloudusers using this service
    service2cloudusers = model.List(model.Object(service2clouduser),thrift_id=9)

    #@doc list of lan's using this service
    service2lans = model.List(model.Object(service2lan),thrift_id=10)

    #@doc list of disks using this service
    service2disks = model.List(model.Object(service2disk),thrift_id=11)


# @doc None
class networkport(model.Model):

    #@doc property to indicate if the port must be monitored by a monitoring tool (if the service is to be monitored)
    monitor = model.Boolean(thrift_id=1)

    #@doc ip protocol type (TCP/UDP)
    ipprotocoltype = model.Enumeration(applicationipprotocoltype,thrift_id=2)

    #@doc ip address
    ipaddress = model.String(thrift_id=3)

    #@doc TCP or UDP port number
    portnr = model.Integer(thrift_id=4)


# @doc networkservice offered by an application. Applications can offer various services, on different udp or tcp ports.
class networkservice(model.Model):

    #@doc remark on service
    description = model.String(thrift_id=1)

    #@doc name of service
    name = model.String(thrift_id=2)

    #@doc flag indicating if the service is enabled
    enabled = model.Boolean(thrift_id=3)

    #@doc service must be monitored using a port check on the ports which have monitor == True
    monitor = model.Boolean(thrift_id=4)

    #@doc ip addresses linked to this service only, null if not specific to this service, link to guid of ip address as used in machine
    ipaddressguids = model.List(model.GUID(),thrift_id=5)

    #@doc list of ports on which this service is available
    ports = model.List(model.Object(networkport),thrift_id=6)


# @doc None
class account(model.Model):

    #@doc login of an account for an application
    login = model.String(thrift_id=1)

    #@doc password of an account for an application
    passwd = model.String(thrift_id=2)

    #@doc type of the account
    accounttype = model.Enumeration(applicationaccounttype,thrift_id=3)

# @doc None
class qpackage(model.Model):
    #@doc package name
    qpackagename = model.String(thrift_id=1)
    
    qpackagedomain = model.String(thrift_id=2)
    
    qpackageversion = model.String(thrift_id=3)
    
class configuration(model.Model):
    #@doc set mode to READONLY/READWRITE/WRITEONLY
    mode = model.Enumeration(applicationmodetype,thrift_id=1)
    
    #@doc limit installation of multiple instances
    installlimitation = model.Enumeration(applicationinstalllimitationtype,thrift_id=2)

from acl import acl

class racktivity_application(model.RootObjectModel):

    #@doc application name, is free text defined in template e.g. kvm, virtualboxhypervisor, xenhypervisor, sshserver, backupserver, ...
    name = model.String(thrift_id=1)

    #@doc additional remarks on application
    description = model.String(thrift_id=2)

    #@doc qpackages
    qpackages = model.List(model.Object(qpackage),thrift_id=3)

    #@doc status of the application
    status = model.Enumeration(applicationstatustype,thrift_id=4)

    #@doc is template, when template used as example for an application
    template = model.Boolean(thrift_id=5)

    #@doc tells from which machine template this machine object originates (can be null if no template used)
    applicationtemplateguid = model.GUID(thrift_id=6)

    #@doc guid of the machine on which the application is installed / running, optional
    machineguid = model.GUID(thrift_id=7)

    #@doc guid of the application which uses this application e.g. dssstore uses dssstoragedaemon, dssstoragedaemon is linked to a machine
    parentapplicationguids = model.List(model.GUID(),thrift_id=8)

    #@doc guid of the space to which this application belongs
    cloudspaceguid = model.GUID(thrift_id=9)

    #@doc custom settings and configuration of application, is XML
    customsettings = model.String(thrift_id=10)

    #@doc list of accounts available in this application (e.g. management accounts)
    accounts = model.List(model.Object(account),thrift_id=11)

    #@doc list of networkservices e.g. http, ...
    networkservices = model.List(model.Object(networkservice),thrift_id=12)

    #@doc group of cloudservices on which this cloudservice is dependant upon, e.g. drp requires postgresql
    requirescloudserviceguids = model.List(model.GUID(),thrift_id=15)

    #@doc list of services offered by this application to another object
    services = model.List(model.Object(service),thrift_id=16)
    
    #@doc flags whether application can be restarted automatically (eg when monitoring detects a problem
    autorestart = model.Boolean(thrift_id=17)

    #@doc system
    system = model.Boolean(thrift_id=18)
    
    #@doc customer
    customer = model.Boolean(thrift_id=19)
    
    #@doc application configuration
    configuration = model.Object(configuration,thrift_id=20)
    
    #@doc monitor the application
    monitor = model.Boolean(thrift_id=21)
    
    #@doc guid of the meteringdevice
    meteringdeviceguid = model.GUID(thrift_id=22)
    
    #@doc series of tags format
    tags = model.String(thrift_id=23)
    #@doc cloudusergroupactions

    #@doc access control list
    acl = model.Object(acl,thrift_id=24)