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
from pylabs import q

try:
    import cPickle as pickle
except ImportError:
    import pickle

from pylabs.baseclasses import BaseEnumeration, EnumerationWithValue
def tearDown(self):
    enumname = 'MyEqualEnumeration'
    if hasattr(q.enumerators, enumname):
        delattr(q.enumerators, enumname)
        
class MyEqualEnumeration(BaseEnumeration): pass

class EnumerationTest(unittest.TestCase):
    def test_simple(self):
        class MySimpleEnumeration(BaseEnumeration):
            foo = property(fget=lambda s: 'foo')

        MySimpleEnumeration.registerItem('foo')
        MySimpleEnumeration.registerItem('bar')

        self.assertEqual(MySimpleEnumeration.FOO.foo, 'foo')
        self.assertEqual(MySimpleEnumeration.BAR.foo, 'foo')

    def test_str(self):
        class MyStrEnumeration(BaseEnumeration):
            pass

        MyStrEnumeration.registerItem('foo')
        MyStrEnumeration.registerItem('bar')

        self.assertEqual(str(MyStrEnumeration.FOO), 'foo')
        self.assertEqual(str(MyStrEnumeration.BAR), 'bar')

        class MyCustomStrEnumeration(BaseEnumeration):
            def __str__(self):
                return 'foo'

        MyCustomStrEnumeration.registerItem('foo')
        MyCustomStrEnumeration.registerItem('bar')

        self.assertEqual(str(MyCustomStrEnumeration.FOO), 'foo')
        self.assertEqual(str(MyCustomStrEnumeration.BAR), 'foo')

    def test_get_by_name(self):
        class MyNamedEnumeration(BaseEnumeration):
            pass

        MyNamedEnumeration.registerItem('foo')
        MyNamedEnumeration.registerItem('bar')

        self.assertEqual(MyNamedEnumeration.getByName('foo'), MyNamedEnumeration.FOO)
        self.assertEqual(MyNamedEnumeration.getByName('bar'), MyNamedEnumeration.BAR)

    def test_constructor(self):
        class MyConstructedEnumeration(BaseEnumeration):
            def __init__(self, a, b):
                self._a, self._b = a, b

            a = property(fget=lambda s: s._a)
            b = property(fget=lambda s: s._b)

        MyConstructedEnumeration.registerItem('foo', 1, b=2)
        MyConstructedEnumeration.registerItem('bar', 3, b=4)

        self.assertEqual(MyConstructedEnumeration.FOO.a, 1)
        self.assertEqual(MyConstructedEnumeration.FOO.b, 2)
        self.assertEqual(MyConstructedEnumeration.BAR.a, 3)
        self.assertEqual(MyConstructedEnumeration.BAR.b, 4)

    def test_empty_type(self):
        class MyEmptyEnumeration(BaseEnumeration): pass

        MyEmptyEnumeration.registerItem('foo')
        MyEmptyEnumeration.registerItem('bar')

        self.assertNotEqual(MyEmptyEnumeration.FOO, MyEmptyEnumeration.BAR)

    def test_equality(self):
        try:
            import cPickle as pickle
        except ImportError:
            import pickle

        MyEqualEnumeration.registerItem('foo')
        MyEqualEnumeration.registerItem('bar')

        p = pickle.dumps(MyEqualEnumeration.FOO)

        o = pickle.loads(p)

        self.assertEqual(o, str(MyEqualEnumeration.FOO))
        self.assertNotEqual(o, str(MyEqualEnumeration.BAR))

    def test_finished_enumeration(self):
        class MyFinishedEnumeration(BaseEnumeration):
            pass

        MyFinishedEnumeration.registerItem('foo')
        MyFinishedEnumeration.finishItemRegistration()

        self.assertRaises(RuntimeError, MyFinishedEnumeration, 'bar')
        self.assert_(not hasattr(MyFinishedEnumeration, 'registerItem'))
        self.assert_(not hasattr(MyFinishedEnumeration, 'finishItemRegistration'))

    def test_check(self):
        class MyCheckedEnumeration(BaseEnumeration):
            pass

        class MyTestEnumeration(BaseEnumeration):
            pass

        MyCheckedEnumeration.registerItem('foo')
        MyCheckedEnumeration.registerItem('bar')

        MyTestEnumeration.registerItem('foo')
        MyTestEnumeration.registerItem('bat')

        self.assert_(MyCheckedEnumeration.check(MyCheckedEnumeration.FOO))
        self.assert_(MyCheckedEnumeration.check(MyCheckedEnumeration.BAR))

        self.assertFalse(MyCheckedEnumeration.check('foo'))
        self.assertFalse(MyCheckedEnumeration.check(MyTestEnumeration.BAT))
        self.assertFalse(MyCheckedEnumeration.check(MyTestEnumeration.FOO))

        crasher = MyCheckedEnumeration()
        crasher._pm_enumeration_name = 'foo'

        self.assertFalse(MyCheckedEnumeration.check(crasher))

    def test_enumerators_check(self):
        class MyRegisteredEnumeration(BaseEnumeration):
            pass

        MyRegisteredEnumeration.registerItem('foo')

        import pylabs
        self.assert_(pylabs.q.enumerators.MyRegisteredEnumeration.check(
                pylabs.q.enumerators.MyRegisteredEnumeration.FOO))

    def test_itemname_validation(self):
        class MySpecialItemEnumeration(BaseEnumeration):
            pass

        MySpecialItemEnumeration.registerItem('foo')
        MySpecialItemEnumeration.registerItem('_foo')
        MySpecialItemEnumeration.registerItem('foo123')
        MySpecialItemEnumeration.registerItem('foo123abc')
        MySpecialItemEnumeration.registerItem('foo_bar')

        self.assertRaises(ValueError, MySpecialItemEnumeration.registerItem, '123foo')
        self.assertRaises(ValueError, MySpecialItemEnumeration.registerItem, '123-321')
        self.assertRaises(ValueError, MySpecialItemEnumeration.registerItem, '+abc')
        self.assertRaises(ValueError, MySpecialItemEnumeration.registerItem, 'abc foo')

    def test_inititems(self):
        class MyInitializedEnumeration(BaseEnumeration):
            @classmethod
            def _initItems(cls):
                cls.registerItem('foo')
                cls.registerItem('bar')
                cls.finishItemRegistration()

        MyInitializedEnumeration.FOO
        MyInitializedEnumeration.BAR
        self.assertRaises(AttributeError, getattr, MyInitializedEnumeration, 'baz')


class EnumerationPropertyTestEnumeration(BaseEnumeration):
    pass

EnumerationPropertyTestEnumeration.registerItem('foo')
EnumerationPropertyTestEnumeration.registerItem('bar')
EnumerationPropertyTestEnumeration.finishItemRegistration()

from pylabs.baseclasses.BaseEnumeration import EnumerationProperty

class PickleTest(object):
    t = EnumerationProperty(EnumerationPropertyTestEnumeration,
            fget=lambda s: s._t, fset=lambda s, v: setattr(s, '_t', v),
            fdel=lambda s: delattr(s, '_t'))

class EnumerationPropertyTest(unittest.TestCase):
    def test_instanciation(self):
        class TestInstanciation(object):
            t = EnumerationProperty(EnumerationPropertyTestEnumeration)

        test = TestInstanciation()

    def test_get(self):
        class TestGet(object):
            def __init__(self, t):
                #This is a test hack, do not use in your code!
                self._t = t._pm_enumeration_name

            t = EnumerationProperty(EnumerationPropertyTestEnumeration,
                    fget=lambda s: s._t)

        test = TestGet(EnumerationPropertyTestEnumeration.FOO)

        self.assertEquals(test._t, 'foo')
        self.assertEquals(test.t, EnumerationPropertyTestEnumeration.FOO)
        self.assert_(test.t is EnumerationPropertyTestEnumeration.FOO)

    def test_set(self):
        class TestSet(object):
            t = EnumerationProperty(EnumerationPropertyTestEnumeration,
                    fget=lambda s: s._t, fset=lambda s, v: setattr(s, '_t', v))

        test = TestSet()
        test.t = EnumerationPropertyTestEnumeration.FOO

        self.assertEquals(test._t, 'foo')
        self.assertEquals(test.t, EnumerationPropertyTestEnumeration.FOO)
        self.assert_(test.t is EnumerationPropertyTestEnumeration.FOO)

    def test_del(self):
        class TestDel(object):
            t = EnumerationProperty(EnumerationPropertyTestEnumeration,
                    fget=lambda s: s._t, fset=lambda s, v: setattr(s, '_t', v),
                    fdel=lambda s: delattr(s, '_t'))

        test = TestDel()
        test.t = EnumerationPropertyTestEnumeration.FOO

        self.assert_(test.t is EnumerationPropertyTestEnumeration.FOO)

        delattr(test, 't')

        self.assertRaises(AttributeError, getattr, test, 't')

    def test_validation(self):
        class TestValidation(object):
            t = EnumerationProperty(EnumerationPropertyTestEnumeration,
                    fget=lambda s: s._t, fset=lambda s, v: setattr(s, '_t', v),
                    fdel=lambda s: delattr(s, '_t'))

        class MyEnum(BaseEnumeration): pass
        MyEnum.registerItem('foo')
        MyEnum.finishItemRegistration()

        test = TestValidation()

        test.t = EnumerationPropertyTestEnumeration.FOO
        self.assert_(test.t is EnumerationPropertyTestEnumeration.FOO)

        test.t = EnumerationPropertyTestEnumeration.BAR
        self.assert_(test.t is EnumerationPropertyTestEnumeration.BAR)

        self.assertRaises(TypeError, setattr, test.t, 'foo')
        self.assertRaises(TypeError, setattr, test.t, MyEnum.FOO)

    def test_pickling(self):
        #This is rather hackish, but needed as a test
        test = PickleTest()
        test.t = EnumerationPropertyTestEnumeration.FOO

        p = pickle.dumps(test)

        np = p.replace('\'foo\'', '\'bar\'')

        ntest = pickle.loads(np)

        self.assert_(ntest.t is EnumerationPropertyTestEnumeration.BAR)


class EnumerationWithValueTest(unittest.TestCase):
    def test_instanciation(self):
        class MyInstanceTest(EnumerationWithValue):
            pass

        t = MyInstanceTest('value')
        t = MyInstanceTest(value='value')
        t = MyInstanceTest('value', 'doc')
        t = MyInstanceTest('value', doc='doc')

        self.assertRaises(TypeError, MyInstanceTest, doc='doc')

    def test_value(self):
        class MyValueTest(EnumerationWithValue):
            pass

        t = MyValueTest('value')
        self.assertEquals(str(t), 'value')

    def test_doc(self):
        class MyDocTest(EnumerationWithValue):
            pass

        t = MyDocTest('value')
        self.assertEquals(repr(t), 'value')

        t = MyDocTest('value', doc='doc')
        self.assertEquals(repr(t), 'doc')
