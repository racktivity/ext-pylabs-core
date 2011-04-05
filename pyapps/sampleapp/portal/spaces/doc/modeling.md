#Modeling Root Objects

After the process of designing your PyLabs Application (PyApp), it is time that you define the different Root Objects of your PyApp. Each model of a root object is a `.py`-file and stored in its proper directory.

See the [PyApps Directory Structure] (sampleapp.md/) for more information about the location of the files.

##What is a Root Object
A Root Object is a logical entity of the PyApp, stored in the PyLabs DRP, and more specific in [Arakoon](http://www.arakoon.org). A root object consists of properties, and references to other root objects.

##File Structure
The file name is always `rootobject.py`, where rootobject is the Root Object name, using only lowercase characters, possibly using underscores.
The file content is always structured as follows:

    import libs

    #@doc some doc about enumeration
    class enumeration(BaseEnumeration):
        @classmethod
        def _initItems(cls):
            enumerationvalue1
            enumerationvalue2
            ....

    #@doc some doc about the root object
    class rootobject(model.RootObjectModel):
        #@doc some doc about RO property
        property1 = model.<value type>(thrift_id=1)
        

##File Details

###Importing Libraries
You always need to import at least one library, `pymodel`, which is a key component of the PyLabs framework.
If you need custom enumerators, you also need to import the BaseEnumeration library.

    from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
    import pymodel as model

###Creating Custom Enumerators
Besides the default PyLabs enumerators, such as AppStatusType and MessageType, you can create your own enumerator.
Each custom enumerator is a custom class that inherits from teh BaseEnumeration base class.
Always add a short description of the enumerator with `#@doc your doc here`. This documentation is used in the API documentation of the PyApp.

    #@doc my first enumerator
    class MyFirstEnum(BaseEnumeration):
        @classmethod
        def _initItems(cls):
            cls.registerItem('OPTION1')
            cls.registerItem('OPTION2')
            cls.finishItemRegistration()

A first line in the class is a [decorator] (http://wiki.python.org/moin/PythonDecorators). The `@classmethod` form is a function decorator. It is used to make the defined items available on the class and not via the instance of the class. More information about this decorator can be found [here] (http://docs.python.org/library/functions.html#classmethod).

The next line is the start of the method, it is always as shown in the example above.

Then you start registering the items, make sure that each item is capitalized.

To finish the enumeration, call the `finishItemRegistration` function.

###Modeling the Root Object
The definition of a Root Object is comprised in a class that inherits from `pymodel.RootObjectModel`, but since `pymodel` is imported as `model`, this becomes `model.RootObjectModel`.
In this class you define the properties of the Root Object. A property is defined as follows:

    property_name = model.<property_type>(thrift_id=x)

where x is a sequential integer and where <property_type> can be one of the following types (case-sensitive):
* Boolean
* DateTime
* Dict 
* Enumeration
* Float
* GUID
* Integer
* List
* String

The `thrift_id` is a required argument. It is a unique identifier for the object and must remain unique over time. PyLabs uses the [thrift] (http://thrift.apache.org/) framework for serializing and deserializing objects. Where PyLabs itself uses the property_name in the application, the underlying thrift framework uses this `thrift_id`.

In case the property is an Enumeration-type, you have to add the enumerator as argument. The enumerator can be a default PyLabs enumerator, or a custom enumerator.

As last point, do not forget to add documentation to the object and its properties. 

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

Whenever you add or update a property, make sure that you do not reuse the `thrift_id`. For example, assume that in a next version the `streetnumber` property is split in two properties, `street` and `number`. 
You could change the name of the `streetnumber` property to just `street` and create a new property `number`, however, do not apply the change this way. Create two new properties and comment the obsolete property instead.
Since thrift works by id, existing objects will provide values with street and number when calling their new property `street`.
In the example given, if you change the property `streetnumber` to `street`, all existing root objects in the database still contain the values of `streetnumber`, where newly created objects will only have a street name. This may result in erroneous values when retrieving old root objects.
If you put the old property in a comment line and create two new properties, you will no longer be able to retrieve the old value of the commented property. Therefore be careful when you make properties inactive.


##How to Use the Model
In the above sections you have learned how you can model the Root Objects of your PyApp. This step in fact only creates the model, which you can consider to be the schema of your Root Object, similar to XML schemas for XML documents. The model is used in your PyApp for the actual creation of Root Objects, which are stored in the DRP [Arakoon] (http://www.arakoon.org) data store.

##What's Next?
After defining a Root Object, you have to define the different actions that can be executed on a Root Object. That step too is only a modeling phase. You define the possible actions, their arguments, and what the action must return as result.
