[importpylabs]: /pylabsdoc/#/HowTo/ImportPyLabs
[importextension]: /pylabsdoc/#/HowTo/ImportExtensionClass
[baseclass]: /pylabsdoc/#/ExtendingPyLabs/BaseClasses
[contribute]: /pylabsdoc/#/PyLabs50/Contributing
[testdata]: /pylabsdoc/#/ExtendingPyLabs/CmdbTestData


# CMDB Application Specifications

The CMDB Application specifications must specify which properties the application must have and which methods the module must contain to configure the application.

## Content of the Specification File

* Import the required modules. Check How to Import PyLabs][importpylabs] and [How to Import Classes from Extensions][importextension].
* Add a Class that inherits from the base class [CMDBApplicationObject][baseclass].
* Add all methods of the class.
* Add PyDocs for *each* method that gives its full explanation, see the *DocString* section in the [Contributing in Style][contribute] page.
* Add fake data, see [CMDB Test Data][testdata].


## Advantages

* The developer has immediately all modules that he has to use.
* The developer no longer has to take care of the documentation of the methods.
* The developer can immediately use the extension in the Q-Shell.
* The developer sees what the methods must do and what they should return.


## Example

[[code]]
#import the necessary modules
from pylabs import q

from ProFTPDACE import ProFTPDACE, ProFTPDACERight

#define the class
class ProFTPDShare(CMDBApplicationObject):

    def __init__(self, name, path = None):
        """
        Default constructor
        
        @param name: unique name for the share
        @param path: path to the folder to share
        """
        # Initialize properties
        self.__init_properties__(name, path = path)
        
    def addACE(self, name, right = None):
        """
        Add an entry to the acl
        
        @param name: name of the user to add to the acl
        @param right: ProFTPDACERight to assign to the user
        """
        pass

    def removeACE(self, name):
        """
        Remove an entry from the acl
        
        @param name: name of the user to remove from the acl
        """
        pass
        
    def __fake_data__(self):
        """
        Fill object with fake data if 'fakeData' var is set
        """      
        
        if not q.vars.getVar('fakeData'):
            return
        
        self.isDirty = False
        
        self.path = q.system.fs.joinPaths(q.dirs.varDir, 'shares', self.name)
        
        import uuid
        
        for i in range(0, 3):
            name = 'fake-%s' % uuid.uuid4()
            entry = ProFTPDACE(name)
            self.acl[entry.name] = entry
[[/code]]