from enumerations import *
import pymodel as model


# @doc os type
class ostype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('WINDOWS')
        cls.registerItem('SOLARIS')
        cls.registerItem('OPENSOLARIS')
        cls.registerItem('LINUX')
        cls.finishItemRegistration()
        
class osbitversiontype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BIT32')
        cls.registerItem('BIT64')
        cls.finishItemRegistration()



# @doc operating system
class os(model.RootObjectModel):

    #@doc name of the operating system
    name = model.String(thrift_id=1)

    #@doc os brand
    ostype = model.Enumeration(ostype,thrift_id=2)

    #@doc filename of icon representing os in various clouduser interfaces
    iconname = model.String(thrift_id=3)

    #@doc version of the operating system
    osversion = model.String(thrift_id=4)

    #@doc patch level of operating system
    patchlevel = model.String(thrift_id=5)

    #@doc description of the operating system
    description = model.String(thrift_id=6)


    #@doc bitversion of the operating system
    osbitversion = model.Enumeration(osbitversiontype,thrift_id=7)

    #@doc system
    system = model.Boolean(thrift_id=8)
    
    #@doc series of tags format
    tags = model.String(thrift_id=9)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=10)
