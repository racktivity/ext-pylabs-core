## Using the CMDB Classes

In the previous section, you have seen some basic information about the PyLabs BaseClasses. In this section you will get to know some practical information about using the CMDB classes.

### Levels of the CMDB Classes
The CMDB classes are split into several levels: 
* The bottom level is the *BaseCMDBObject* Class. All levels above this class inherit the properties (i.e. _timestampcreated_ and _timestampmodified_).
* One level higher you have the *CMDBObject* Class and the *CMDBSubObject* Class. 
    
    ** CMDBObject Class: besides the properties that are inherited from the BaseCMDBObject Class, this class adds the properties _cmdbtypename, cmdbid, cmdbguid_ and _cmdbinsync_. This class provides also the `save` method to save the configuration (i.e. a CMDBObject) in the CMDB.
    
    ** CMDBSubObject Class: besides the properties that are inherited from the BaseCMDBObject Class, this class adds the properties _rootcmdbtypename, new_ and _deleted_. The property `rootcmdbtypename` indicates the CMDB Object to which it belongs, `new` is a flag indicating if this object is a new object and `deleted` is a flag indicating if this object is logical deleted.

* A level above the CMDBObject Class, you find the *CMDBApplicationObject* Class. This class inherits all properties and methods from the CMDBObject class and adds the propterties _initDone_ (indicates if the application's environment has been initialized) and _pid_ (Process ID, given by an operating system). This class is used for a CMDB object, containing the configuration data of an application.
* As top level you have the *CMDBServerObject* class. This class inherits all properties from the CMDBApplicationObject class and adds the propterties _autoRestart_ and _startAtReboot_. This class is used for a CMDB object, containing the configuration data of a _server application_.

Now that you have seen the levels of the CMDB classes, we will move on with some examples to show you the usages of these classes. Since we only have four top level classes (namely CMDBObject, CMDBSubObject, CMDBApplicationObject and CMDBServerObject), we will only give examples of three of them (CMDBObject, CMDBSubObject and CMDBServerObject), since we do not have applications available.

### VirtualboxHypervisor (CMDBObject)

[[code]]
import re

from pylabs import q
from pylabs.baseclasses.CMDBObject import CMDBObject

from VirtualboxMachine import VirtualboxMachine


class VirtualboxHypervisor(CMDBObject):
    """
    Represents a Virtualbox instance configuration
    """
#add properties to the CMDBObject:

    cmdbtypename = "q.hypervisors.virtualbox"
    machines = q.basetype.dictionary(doc = 'Dict of configured Virtualbox machines', flag_dirty = True)
    machinesFolder = q.basetype.dirpath(doc='Path to the folder where machine  configuration files will be created and saved', flag_dirty = True)
    initDone = q.basetype.boolean(doc='Indicates if the hypervisor object is initialized or not')

#add methods to the class:

    def addMachine(self, name, memory = None, os = q.enumerators.VirtualboxOsType.UNKNOWN):
        """
        Add virtualbox machine

        @param name: unique name for the machine. The name is used to store the configuration on the host filesystem. It should be conform with the filename specifications of the host operating system.
        @param memory: the amount of memory (in MB) allocated to the virtual machine
        @type os: VirtualboxOsType
        @param os: the operating system installed on the virtual machine, one of the values of q.enumerators.VirtualboxOsType
        @return: instance of new VirtualboxMachine
        """

        if not q.system.fs.validateFilename(name):
            raise ValueError('The name has an invalid format. It must be conform to the filename requirements of your operating system.')

        if name in self.machines:
            raise ValueError("A machine with name '%s' already exists.  Name must be unique !"%name)

        vbm = VirtualboxMachine(name, memory, os, self.machinesFolder)
        vbm.created = False
        self.machines[name] = vbm
        self.dirtyProperties.add('machines')
        return vbm


    def removeMachine(self, name):
        """
        Remove virtual machine with the given name

        @param name: name of the machine
        """
        if name not in self.machines:
            raise ValueError("A machine with name '%s' does not exist"%name)

        self.machines[name].removed = True
        self.dirtyProperties.add('machines')
[[/code]]

### VirtualboxDisk (CMDBSubObject)

[[code]]
from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class VirtualboxDisk(CMDBSubObject):
    """
    Virtual hard disks that can be attached to a VM's IDE controller (primary master and slave, and secondary slave; the secondary master is
    always reserved for the virtual CD/DVD drive)
    """

#add properties to the CMDBSubObject:
    name = q.basetype.string(doc = 'Unique friendly name for the disk', flag_dirty = True)
    type = q.basetype.enumeration(q.enumerators.VirtualboxDiskType, doc = 'Type of the Disk, whether it is iscsi disk or hard drive image', flag_dirty = True)
    order = q.basetype.enumeration(q.enumerators.VirtualboxHardDriveType, doc = 'Order of the disk on the machine', flag_dirty = True)
    path = q.basetype.path(doc = 'Path to the disk/image on the host system', allow_none = True, flag_dirty = True)
    removed = q.basetype.boolean(doc = 'Indicates if the object has been removed', default = False, flag_dirty = True)
    uuid = q.basetype.string(doc = 'UUID that identifies a disk in a virtual machine', allow_none = True)


    def __init__(self, name, order, path, type = q.enumerators.VirtualboxDiskType.HARDDISKIMAGE, uuid = None):
        """
        Default constructor

        @param name: unique name for the disk
        @param order: sequence of the disk
        @param path: path to the disk on the host
        @type type: VitualboxDiskType
        @param type: Type of the Disk whether it is iscsi disk or hard drive image, one of the values q.enumerators.VirtualboxDiskType.
        @param uuid:  UUID that identifies a disk in a virtual machine
        """

        CMDBSubObject.__init__(self)
        # Initialize properties
        self.name = name
        self.order = order
        self.type = type
        self.uuid = uuid
        self.path = path
[[/code]]


### PostgresqlServer (CMDBServerObject)

[[code]]
from pylabs import q
from pylabs.baseclasses.CMDBServerObject import CMDBServerObject
from PostgresqlDatabase import PostgresqlDatabase

class PostgresqlServer(CMDBServerObject):

#add properies to the CMDBServerObject:

    cmdbtypename    = 'postgresql8server'
    name = q.basetype.string('postgresql8server')
    configFileDir   = q.basetype.dirpath(doc="Directory containing the configuration files", default=q.system.fs.joinPaths(q.dirs.baseDir, 'apps', "postgresql", "conf"))
    databases       = q.basetype.dictionary()

    # security?
    rootLogin       = q.basetype.string(doc="Root login for the Postgres server", allow_none=True)
    rootPasswd      = q.basetype.string(doc="Password for the root login", allow_none=True)
    initialized     = q.basetype.boolean(doc="Indicates if this Postgres database server was already initialized", default=False)

#initialize the CMDBServerObject:

    def __init__(self):
        CMDBServerObject.__init__(self)

#add other methods to the class

    def addDatabase(self, name, owner=None):
        """
        Adds a database
        @param name: Name of the database to create
        @param owner: Owner of the database to create
        @return: PostgresqlDB object created
        """

        # Confusing -> db already exists
        if name in self.databases:
            return self.databases[name]

        owner = owner or self.rootLogin
        newDB = PostgresqlDatabase(name, owner)
        self.databases[newDB.name] = newDB
        return newDB

    def removeDatabase(self, name):
        """
        Deletes a database by name
        @param name: Name of the database to delete
        """
        q.logger.log("Marking database [%s] for deletion"%name, 5)
        self.databases[name].deleted = True

    def printDatabases(self, name=None,verbose=True):
        """
        Human friendly output of site configuration
        """
        if name:
             q.console.echo(self.databases[name])
        else:
            stringRep = ''
            for db in self.databases.itervalues():
                stringRep += (str(db) if verbose else (db.name + '\n'))

            q.console.echo(stringRep)
[[/code]]