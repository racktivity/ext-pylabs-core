from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

# @doc Activity type enumeration
class activitytype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('CALL')
        cls.registerItem('MEETING')
        cls.finishItemRegistration()

# @doc Activity status enumeration
class activitystatus(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('PLANNED')
        cls.registerItem('HELD')
        cls.registerItem('CANCELLED')
        cls.finishItemRegistration()

# @doc Activity priority enumeration
class activitypriority(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('HIGH')
        cls.registerItem('MEDIUM')
        cls.registerItem('LOW')
        cls.finishItemRegistration()

# @doc Activity object
class activity(model.RootObjectModel):

    #@doc name of activity
    name = model.String(thrift_id=1)

    #@doc description of activity
    description = model.String(thrift_id=2)

    #@doc location of activity
    location = model.String(thrift_id=3)

    #@doc type of activity
    type = model.Enumeration(activitytype, thrift_id=4)

    #@doc status of activity
    status = model.Enumeration(activitystatus, thrift_id=5)

    #@doc priority of activity
    priority = model.Enumeration(activitypriority, thrift_id=6)

    #@doc guid of lead in case of lead
    leadguid = model.GUID(thrift_id=7)

    #@doc guid of customer in case of customer
    customerguid = model.GUID(thrift_id=8)

    #@doc start date of activity
    startdate = model.DateTime(thrift_id=9)

    #@doc start time of activity
    starttime = mode.DateTime(thrift_id=10)
    
    #@doc end date of activity
    enddate = model.DateTime(thrift_id=11)
    
    #@doc end time of activity
    endtime = model.DateTime(thrift_id=12)
