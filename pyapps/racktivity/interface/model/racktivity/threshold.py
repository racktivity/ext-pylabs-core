from enumerations import *
import pymodel as model

# @doc None
class thresholdtype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('VOLTAGE')
        cls.registerItem('POWER')
        cls.registerItem('CURRENT')
        cls.registerItem('POWERFACTOR')
        cls.registerItem('KILOWATTHOUR')
        cls.registerItem('TEMPERATURE')
        cls.registerItem('AIRFLOW')
        cls.registerItem('HUMIDITY')
        cls.finishItemRegistration()
        
class thresholdimpacttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('WARNING')
        cls.registerItem('SWITCHOFF')  
        cls.finishItemRegistration()     



# @doc class which provides the properties of a threshold
class threshold(model.RootObjectModel):
    #@doc threshold type, listed in the enumerator ThresholdType
    thresholdtype = model.Enumeration(thresholdtype,thrift_id=1)
      
    #@doc maximum value
    minimum = model.Integer(thrift_id=2)

    #@doc maximum value
    maximum = model.Integer(thrift_id=3)
    
    #@doc guid of the clouduser who set the threshold
    clouduserguid = model.GUID(thrift_id=4)
    
    #@doc threshold impact type
    thresholdimpacttype = model.Enumeration(thresholdimpacttype, thrift_id=5)
    
    #@doc series of tags format
    tags = model.String(thrift_id=6)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=7)