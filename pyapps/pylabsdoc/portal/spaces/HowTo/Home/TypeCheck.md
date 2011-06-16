@metadata title=Perform Type Check
@metadata tagstring=type check typeless


# How to Perform Type Checks
The PyLabs Type System has been introduced since Python itself is a typeless language.
The typeless language means that a variable can change from type, just by assigning another value to the variable. By creating the PyLabs Type System, we make it only easier to add property-style attributes to classes, which have strict assignment checks.
The PyLabs Type System contains several predefined types, collected in several classes: PrimitiveTypes, CollectionTypes, GenericTypes. Checks are performed if a certain variable is of the correct type.
Besides the predefined types, the PyLabs Type System contains also custom types, collected in the module Custom Types. For example in the module Custom Types, you can find the type 'IP address'. This allows you to check the validity of a variable to which an IP address is assigned. For example, an IP of 10.100.355.254 results in an error.
The PyLabs predefined and custom types are all exposed in the name space `q.basetype.*`. All types inherit from one common base class BaseType, `pylabs.pmtypes.base.BaseType`.

The PyLabs framework has a useful extension to check if data comply with a given type.

For example if a user must enter an IP address, the PyLabs type check checks if the entered data is a valid IP address.

    In [22]: q.basetype.ipaddress.check('255.255.255.0')
    Out[22]: True
    
    In [23]: q.basetype.ipaddress.check('255.255.256.0')
    Out[23]: False

You can check on all basetypes that are available in PyLabs:

    q.basetype.boolean          q.basetype.ipport
    q.basetype.dictionary       q.basetype.list
    q.basetype.dirpath          q.basetype.object(
    q.basetype.duration         q.basetype.path
    q.basetype.enumeration(     q.basetype.set
    q.basetype.filepath         q.basetype.string
    q.basetype.float            q.basetype.unixdirpath
    q.basetype.guid             q.basetype.unixfilepath
    q.basetype.integer          q.basetype.windowsdirpath
    q.basetype.ipaddress        q.basetype.windowsfilepath
    q.basetype.ipaddressrange