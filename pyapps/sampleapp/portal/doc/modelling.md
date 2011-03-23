#Modelling Root Objects

This is just some very quick info about how to model a root object for a pyapp

Root Object: logical entity of the pyapp
\#@doc: documentation line that will be used when api documentation is generated
use pymodel to model RO

##Import libs
from pylabs.baseclasses.BaseEnumeration import BaseEnumeration --> to create your proper enumerators
import pymodel as model --> to model the root object


##Enumeration
@todo insert: what is enumerator and its purpose
Always same way to create an enumerator

1. set documentation of the enumerator
2. create class that inherits from BaseEnumeration
3. create method to initialize the items
4. register the possible enum values
5. finish item registration


    \# @doc Activity type enumeration
    class activitytype(BaseEnumeration):
        @classmethod
        def _initItems(cls):
            cls.registerItem('CALL')
            cls.registerItem('MEETING')
            cls.finishItemRegistration()
            
##Modelling the Root Object
create class that inherits from model.RootObjectModel
define the parameters of the RO
possible thrift\_id
enumerator
add doc for each parameter