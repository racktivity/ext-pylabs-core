@metadata title=Modeling Root Objects
@metadata order=20
@metadata tagstring=model root object ro

[pyappdir]: /#/PyLabsApps/Introduction
[drp]: /#/PyLabs50/Architecture
[arakoon]: http://www.arakoon.org
[decorator]: http://wiki.python.org/moin/PythonDecorators
[classmethod]: http://docs.python.org/library/functions.html#classmethod
[enums]: /#/ExtendingPyLabs/CreateEnumerators
[thrift]: http://thrift.apache.org/


#Modeling Root Objects

After the process of designing your PyLabs Application (PyApp), it is time that you define the different Root Objects of your PyApp. Each model of a root object is a `.py`-file and stored in its proper directory.

See the [PyApps Directory Structure][pyappdir] for more information about the location of the files.

##What is a Root Object
A Root Object is a logical entity of the PyApp, stored in the PyLabs [DRP][drp] (Datacenter Resource Planning), and more specific in [Arakoon][arakoon]. A Root Object consists of properties, complex properties, and references to other Root Objects.
A complex property, also referred to as 'model object', is for example a contact person in a company. The contact on its turn has its own properties.
For example a customer can have a name and address as properties, contacts as model objects, and references to other customers.


##File Structure
The file name is always `<rootobject>.py`, where rootobject is the Root Object name, using only lower-case characters, possibly using underscores.
The file content is always structured as follows:

[[code]]
import python libs

#@doc some doc about enumeration
class enumeration(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        enumerationvalue1
        enumerationvalue2
        ....

#@doc some doc about the root object
class RO(model.RootObjectModel):
    #@doc some doc about RO property
    property1 = model.valuetype(thrift_id=1)
[[/code]]    
        

##File Details

###Importing Libraries
You always need to import at least one library, `pymodel`, which is a key component of the PyLabs framework.
If you need custom enumerators, you also need to import the BaseEnumeration library.

[[code]]
from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
[[/code]]

###Creating Custom Enumerators
Besides the default PyLabs enumerators, such as AppStatusType and MessageType, you can create your own enumerator.
Each custom enumerator is a custom class that inherits from the BaseEnumeration base class.
Always add a short description of the enumerator with `#@doc your doc here`. This documentation is used in the API documentation of the PyApp.

[[code]]
#@doc my first enumerator
class MyFirstEnum(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('OPTION1')
        cls.registerItem('OPTION2')
        cls.finishItemRegistration()
[[/code]]        

A first line in the class is a [decorator][]. The `@classmethod` form is a function decorator. It is used to make the defined items available on the class and not via the instance of the class. More information about this decorator can be found [here][classmethod].

The next line is the start of the method, it is always as shown in the example above.

Then you start registering the items, make sure that each item is capitalized.

To finish the enumeration, call the `finishItemRegistration` function.

See also the [Extending PyLabs][enums] chapter for more information about PyLabs Enumerators.


###Modeling the Root Object
The definition of a Root Object is comprised in a class that inherits from `pymodel.RootObjectModel`, but since `pymodel` is imported as `model`, this becomes `model.RootObjectModel`.
In this class you define the properties of the Root Object. A property is defined as follows:

[[code]]
property_name = model.property_type(thrift_id=x)
[[/code]]

where x is a sequential integer and where `property_type` can be one of the following types (case-sensitive):

* Boolean
* DateTime
* Dict 
* Enumeration
* Float
* GUID
* Integer
* List
* Object
* String

The `thrift_id` is a required argument. It is a unique identifier for the object and must remain unique over time. PyLabs uses the [thrift][] framework for serializing and deserializing objects. Where PyLabs itself uses the property_name in the application, the underlying thrift framework uses this `thrift_id`.

In case the property is an Enumeration-type, you have to add the enumerator as argument. The enumerator can be a default PyLabs enumerator, or a custom enumerator.

As last point, do not forget to add documentation to the object and its properties. 

[[code]]
#@doc Model of Root Object
class MyRootObject(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc street and number of object
    streetnumber = model.String(thrift_id=2)

    #@doc is person parent
    isparent = model.Boolean(thrift_id=3)

    #@doc show custom enumerator
    customenum = model.Enumeration(MyFirstEnum, thrift_id=4)
[[/code]]    

Whenever you add or update a property, make sure that you do not reuse the `thrift_id`. For example, assume that in a next version the `streetnumber` property is split in two properties, `street` and `number`. 
You could change the name of the `streetnumber` property to just `street` and create a new property `number`. However, do not apply the change this way. Create two new properties and comment the obsolete property instead.
Since thrift works by id, existing objects will provide values with street and number when calling their new property `street`.
In the example given, if you change the property `streetnumber` to `street`, all existing Root Objects in the database still contain the values of `streetnumber`, where newly created objects will only have a street name. This may result in erroneous values when retrieving old Root Objects.
If you put the old property in a comment line and create two new properties, you will no longer be able to retrieve the old value of the commented property. Therefore be careful when you make properties inactive.


##How to Use the Model
In the above sections you have learned how you can model the Root Objects of your PyApp. This step in fact only creates the model, which you can consider to be the schema of your Root Object, similar to XML schemas for XML documents. The model is used in your PyApp for the actual creation of Root Objects, which are stored in the DRP [Arakoon][arakoon] data store.

[[information]]
**Information**

When you want to make the new model available in the Q-Shell, you have to install you PyApp again, using `p.application.install('yourPyApp')`.
[[/information]]

##What's Next?
After defining a Root Object, you have to define the different actions that can be executed on a Root Object. That step too is only a modeling phase. You define the possible actions, their arguments, and what the action must return as result.
