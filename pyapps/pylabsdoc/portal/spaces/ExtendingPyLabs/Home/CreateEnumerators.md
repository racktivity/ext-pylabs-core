@metadata title=Custom Enumerators
@metadata order=30
@metadata tagstring=custom enumerator create

#Creating Custom Enumerators

An enumerator is a static/constant collection of instances of a specific type. It is accessible as attribute on the class of this type. In most situations you only want to allow some specific instances to exist (enumeration items) and disallow an external consumer to create extra type instances.
Enumerator classes are ordinary classes which have always the `BaseEnumeration` class as base. The `BaseEnumeration` class itself provides not much functionality, next to basic implementations of `__str__` and `__repr__`, a check method which checks whether a given variable is a valid enumeration item (alike check methods on other _pmtype_ classes), and a generic `getByName` method which retrieves an enumeration item based on its name.
Enumerators are always exposed on `q.enumerators.*`.

These are the four steps to create a custom enumerator:

1. Import the `BaseEnumeration` module and other required modules
2. Create the enumeration class
3. Register the enumerator items
4. Finish the enumeration registration

These are the minimum steps for creating an enumerator. Extra functionality can be added, for example to show human readable values instead of some PyLabs internal codes.


##Example
Below you find an example of an enumerator in its simplest way.

[[code]]
from pylabs.baseclasses import BaseEnumeration

class YourCustomEnum(BaseEnumeration):
    '''Your PyDoc here'''
    
    @classmethod
    def _initItems(cls)
        cls.registerItem('parrot')
        cls.registerItem('dog')
        cls.registerItem('cat')
        cls.finishItemRegistration()
[[/code]]

In the Q-Shell this new enumerator will look like:

[[code]]
#we suppose that you are in the directory where you have stored YourYourCustomEnum.py
In [1]: from YourYourCustomEnum import YourCustomEnum
 
 
#Use Tab-completion
In [2]:  YourCustomEnum.
YourCustomEnum.CAT          YourCustomEnum.PARROT       YourCustomEnum.getByLevel(  YourCustomEnum.mro
YourCustomEnum.DOG          YourCustomEnum.check(       YourCustomEnum.getByName(   YourCustomEnum.printdoc(
 
In [3]:  q.enumerators.YourCustomEnum.
q.enumerators.YourCustomEnum.CAT          q.enumerators.YourCustomEnum.check(       q.enumerators.YourCustomEnum.mro
q.enumerators.YourCustomEnum.DOG          q.enumerators.YourCustomEnum.getByLevel(  q.enumerators.YourCustomEnum.printdoc(
q.enumerators.YourCustomEnum.PARROT       q.enumerators.YourCustomEnum.getByName(
[[/code]]


##Assign a Code to an Enumerator Value
When retrieving an enumerator value, you get an instance of the enumerator, which is often not easy to work with. 
Instead of getting an enumerator instance, it is also possible to assign an integer value and retrieve this integer.

This takes a few changes in your enumerator file.

[[code]]
from pylabs.baseclasses import BaseEnumeration

class YourCustomEnum(BaseEnumeration):
    '''Your PyDoc here'''

    def __init__(self, level):
        self.level = level

    def __int__(self):
        return self.level


    @classmethod
    def _initItems(cls):
        cls.registerItem('parrot', 1)
        cls.registerItem('dog', 2)
        cls.registerItem('cat', 3)
        cls.finishItemRegistration()
[[/code]]

Each enumerator value has now a corresponding code, in this example an integer. With the `__int__` function you can get the integer value instead of the enumerator value.
Let's have a look how it works in the Q-Shell:

[[code]]
In [13]: animal = q.enumerators.YourCustomEnum.CAT

In [14]: animal
Out[14]: cat

In [15]: type(animal)
Out[15]: <class 'YourFirstEnum.YourCustomEnum'>

In [16]: animalCode = q.enumerators.YourCustomEnum.__int__(q.enumerators.YourCustomEnum.CAT)

In [17]: animalCode
Out[17]: 3

In [18]: type(animalCode)
Out[18]: <type 'int'>
[[/code]]