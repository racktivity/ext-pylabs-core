# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import unittest
import random
import math

from pylabs import q
from pylabs.pmtypes import Integer, List, Float
from pylabs.baseclasses import BaseType

def tearDown(self):
    enumname = 'MyEnumeration'
    if hasattr(q.enumerators, enumname):
        delattr(q.enumerators, enumname)
        
class I(BaseType):
    '''Test class for integer properties

    It's also a (temporary) sample of what can be done with our typed properties
    '''

    # Basic integer value
    i = Integer(doc='The well-known integer i')

    # Integer value with a constant default value
    j = Integer(default=1)

    def check_positive(self, value):
        return value >= 0

    # Integer value with a custom check
    k = Integer(check=check_positive)

    #default as a callable
    def get_random(self):
        return random.randint(0, 100)

    #default should be a callable but *not* an unbound method
    r = Integer(default=lambda s: s.get_random())

    def _get_s(self):
        return 123
    s = Integer(default=_get_s)

    #This is a stupid example, you'd never define Pi as a settable attribute on a class
    pi = Float(default=math.pi, doc='The famous pi')

    #This is an integer which can be None
    n = Integer(allow_none=True)

    #This is a readonly integer with a default value
    ro = Integer(default=123, readonly=True)


class IntegerTest(unittest.TestCase):
    def test_class_creation(self):
        i = I()

    def test_simple_assignment(self):
        i = I()
        i.i = 1

    def test_string_assignment(self):
        i = I()
        self.assertRaises(ValueError, setattr, i, 'i', 'abc')

    def test_default(self):
        i = I()
        self.assertEquals(i.j, 1)

    def test_default_assignment(self):
        i = I()
        i.j = 123
        self.assertEquals(i.j, 123)

    def test_custom_check(self):
        i = I()
        i.k = 123
        self.assertRaises(ValueError, setattr, i, 'k', -1)

        self.assertEquals(i.k, 123)

    def test_custom_default(self):
        i = I()
        i.i = 0
        i.k = 100
        self.assert_(i.r >= 0 and i.r <= 100)
        #Check its the same random, once set
        self.assertEquals(i.r, i.r)
        #Check method call
        self.assertEquals(i.s, 123)

    def test_invalid_default(self):
        class I(BaseType):
            i = Integer(default='abc')

        self.assertRaises(RuntimeError, I)

    def test_pi(self):
        i = I()
        self.assertEqual(i.pi, math.pi)

    def test_set_none_fails(self):
        i = I()
        self.assertRaises(ValueError, setattr, i, 'i', None)

    def test_set_none_succeeds(self):
        i = I()
        i.n = None

    def test_readonly(self):
        i = I()
        self.assertEquals(i.ro, 123)

        self.assertRaises(AttributeError, setattr, i, 'ro', 456)


class L(BaseType):
    l = List()

class ListTest(unittest.TestCase):
    def test_instanciation(self):
        l = L()


from pylabs.baseclasses.dirtyflaggingmixin import DirtyFlaggingMixin
class DirtyFlaggedType(BaseType, DirtyFlaggingMixin):
    i = Integer(flag_dirty=True)

class DirtyFlaggingTest(unittest.TestCase):
    def test_instanciation(self):
        i = DirtyFlaggedType()

    def test_default_not_flagging(self):
        i = DirtyFlaggedType()
        self.assert_(not i.isDirtiedAfterSave)
        self.assert_(not i.isDirty)

    def test_set(self):
        i = DirtyFlaggedType()
        i.i = 123

        self.assert_(i.isDirty)
        self.assert_(i.isDirtiedAfterSave)
        self.assertEquals(tuple(i.dirtyProperties), ('i', ))

    def test_reset(self):
        i = DirtyFlaggedType()
        i.i = 123

        self.assert_(i.isDirtiedAfterSave)

        i.reset_dirtied_after_save()

        self.assert_(not i.isDirtiedAfterSave)
        self.assert_(i.isDirty)


from pylabs.pmtypes.GenericTypes import Object
class GenericObjectTest(unittest.TestCase):
    def test_class_instanciation(self):
        class ObjectTestType: pass

        class MyClass(BaseType):
            field = Object(ObjectTestType)

        i = MyClass()

    def test_type_instanciation(self):
        class ObjectTestType(object): pass

        class MyClass(BaseType):
            field = Object(ObjectTestType)

        i = MyClass()

    def test_correct_assignment(self):
        class ObjectTestType(object): pass

        class MyClass(BaseType):
            field = Object(ObjectTestType)

        i = MyClass()
        i.field = ObjectTestType()

    def test_incorrect_assignment(self):
        class ObjectTestType: pass

        class MyClass(BaseType):
            field = Object(ObjectTestType)

        i = MyClass()
        self.assertRaises(ValueError, setattr, i, 'field', 'A string is no ObjectTestType')

    def test_none(self):
        class ObjectTestType: pass

        class MyNoneClass(BaseType):
            field = Object(ObjectTestType, allow_none=True)

        class MyNotNoneClass(BaseType):
            field = Object(ObjectTestType)

        i = MyNoneClass()
        i.field = None

        i = MyNotNoneClass()
        self.assertRaises(ValueError, setattr, i, 'field', None)

    def test_default_instance(self):
        class ObjectTestType: pass

        class MyClass(BaseType):
            field = Object(ObjectTestType, default=ObjectTestType())

        i1 = MyClass()
        i2 = MyClass()

        self.assert_(i1.field == i2.field)

    def test_default_callable(self):
        class ObjectTestType:
            def __init__(self, i):
                self._i = i

            def __eq__(self, other):
                return self._i == other._i

        class MyClass(BaseType):
            field = Object(ObjectTestType, default=lambda o: ObjectTestType(1))

        i1 = MyClass()
        i2 = MyClass()

        self.assert_(not i1.field is i2.field)
        self.assert_(i1.field == i2.field)

        i2.field._i = 2
        self.assert_(not i1.field == i2.field)

    def test_descriptor_type_cache(self):
        class ObjectTestType: pass

        class MyClass(BaseType):
            field1 = Object(ObjectTestType)
            field2 = Object(ObjectTestType)

        self.assert_(type(MyClass.__dict__['field1']) is type(MyClass.__dict__['field2']))


from pylabs.pmtypes.GenericTypes import Enumeration
from pylabs.baseclasses import BaseEnumeration
class MyEnumeration(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('foo')
        cls.registerItem('bar')
        cls.finishItemRegistration()

class MyEnumerationClass(BaseType):
    field1 = Enumeration(MyEnumeration)
    field2 = Enumeration(MyEnumeration)

class GenericEnumerationTest(unittest.TestCase):
    def test_instanciation(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        i = MyClass()

    def test_item_assignment(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        i = MyClass()
        i.field = MyEnumeration.FOO

        self.assert_(i.field is MyEnumeration.FOO)

    def test_string_assignment(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        i = MyClass()
        i.field = 'bar'

        self.assert_(i.field is MyEnumeration.BAR)

    def test_wrong_type_assignment(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        class dummy: pass

        i = MyClass()

        self.assertRaises(ValueError, setattr, i, 'field', dummy())

    def test_wrong_string_assignment(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        i = MyClass()

        self.assertRaises(ValueError, setattr, i, 'field', 'No MyEnumeration item')

    def test_stored_value_is_string(self):
        class MyClass(BaseType):
            field = Enumeration(MyEnumeration)

        i = MyClass()
        i.field = MyEnumeration.FOO

        self.assert_(isinstance(i._pm_field, basestring))

    def test_pickle(self):
        i = MyEnumerationClass()
        i.field1 = MyEnumeration.FOO
        i.field2 = 'bar'

        try:
            import cPickle as pickle
        except ImportError:
            import pickle

        pickledi = pickle.dumps(i)

        newi = pickle.loads(pickledi)

        self.assert_(not i is newi)

        self.assert_(newi.field1 is MyEnumeration.FOO)
        self.assert_(newi.field1 is i.field1)
        self.assert_(newi.field2 is MyEnumeration.BAR)
        self.assert_(newi.field2 is i.field2)

    def test_descriptor_type_cache(self):
        class MyClass(BaseType):
            field1 = Enumeration(MyEnumeration)
            field2 = Enumeration(MyEnumeration)

        self.assert_(type(MyClass.__dict__['field1']) is type(MyClass.__dict__['field2']))


class MetadataType(BaseType):
    i = Integer()
    j = Integer(doc='Documentation for j')
    k = Integer(default=1234, allow_none=True, flag_dirty=True)

class MetadataSubType(MetadataType):
    i = Integer(doc='Some docs for i')
    l = Integer()

class PropertyMetadataTest(unittest.TestCase):
    def test_instanciation(self):
        i = MetadataType()

    def test_fields(self):
        expected_names = ('i', 'j', 'k', )

        d = MetadataType.pm_property_metadata

        self.assertEquals(set(expected_names), set(d.keys()))

    def test_field_i(self):
        d = MetadataType.pm_property_metadata['i']

        self.assert_(not d['doc'])
        self.assert_(not d['check'])
        self.assert_(not d['allow_none'])
        self.assert_(not d['flag_dirty'])

    def test_field_j(self):
        d = MetadataType.pm_property_metadata['j']

        self.assertEquals(d['doc'], 'Documentation for j')

    def test_field_k(self):
        d = MetadataType.pm_property_metadata['k']

        self.assert_(not d['doc'])
        self.assert_(not d['check'])
        self.assertEquals(d['default'], 1234)
        self.assert_(d['allow_none'])
        self.assert_(d['flag_dirty'])

    def test_subtype_fields(self):
        expected_names = ('i', 'j', 'k', 'l', )

        d = MetadataSubType.pm_property_metadata

        self.assertEquals(set(expected_names), set(d.keys()))

    def test_subtype_override_field(self):
        d = MetadataSubType.pm_property_metadata['i']

        self.assertEquals(d['doc'], 'Some docs for i')


from pylabs.pmtypes.base import IGNORE

class FsetTestType(BaseType):
    def fset_test(self, value):
        #This is executed *before* the actual save operation
        new_value = value + 1

        #We need to yield exactly 1 value, which will be saved
        #Do note type checks will be executed on the yielded value
        #If we yield pylabs.pmtypes.base.IGNORE, no save operation will
        #be performed
        if value == 0:
            #We don't want to save if value equals 0
            saved_value = yield IGNORE
        else:
            saved_value = yield new_value

        #This is executed *after* the actual save operation
        #saved_value contains the actual saved value as saved by the descriptor
        #This could be different from new_value if one day we add some other
        #value-changing code to basetypes
        #IGNORE is returned when IGNORE was yielded
        if saved_value is not IGNORE:
            self.j = saved_value - 1

    i = Integer(fset=fset_test)
    j = Integer()

class FsetTest(unittest.TestCase):
    def test_valid_fset(self):
        t = FsetTestType()
        t.i = 123

        self.assertEquals(t.i, 124)
        self.assertEquals(t.j, 123)

    def test_ignore(self):
        t = FsetTestType()
        t.i = 123

        self.assertEquals(t.i, 124)

        t.i = 0

        self.assertEquals(t.i, 124)
