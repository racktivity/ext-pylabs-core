from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

#@todo despiegk:hendrik P1 please check

class portstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ON')
        cls.registerItem('OFF')
        cls.finishItemRegistration()

# @doc monitoring port information of a power device
class portmonitoringinfo(model.Model):
    
  
    #@doc sequence of the port
    sequence = model.Integer(thrift_id=1)

    #@doc status, listed in the enumerator PortStatusType
    status = model.Enumeration(portstatustype,thrift_id=2)
    
    #@doc frequency, when requesting the monitor information.
    frequency = model.Float(thrift_id=3)
    
    #@doc active energy, power expressed in Wh, accumulated real power(e.g power usage from the resistive load) in time when requesting the monitor information..
    energyactive = model.Float(thrift_id=4)

    #@doc apparent energy, power expressed in VAh, accumulated apparent power(e.g absolute value of complex sum of reactive and real power) when requesting the monitor information.
    energyapparent = model.Float(thrift_id=5)

    ##############################################################
    ##################   POWER related information ###############
    ##############################################################

    #@doc real power expressed in watt, real power (power usage from resistive loads) when requesting the monitor information.
    power = model.Float(thrift_id=6) 
    
    #@doc maximum power consumption  occured
    powermax = model.Float(thrift_id=7)    
                             
    power5minuteaverages =model.List(model.Float(), thrift_id=8)
    ##############################################################
    ################   VOLTAGE related information ###############
    ##############################################################
    #@doc voltage, when requesting the monitor information.
    voltage = model.Float(thrift_id=9)
      
    #@doc maximum voltage occured
    voltagemax = model.Float(thrift_id=10) 
    
    #@doc average voltage over 5 minutes timespan 
    voltage5minuteaverages =model.List(model.Float(), thrift_id=11)

    #@doc average voltage over 60 minutes timespan 
    voltageaverage60minutes = model.Float(thrift_id=12) 

    ##############################################################
    ################   CURRENT related information ###############
    ##############################################################
    #@doc current, when requesting the monitor information.
    current = model.Float(thrift_id=13)
   
    #@doc maximum current occurred
    currentmax = model.Float(thrift_id=14)
        
 
    #@doc average current over 5 minutes timespan 
    current5minuteaverages =model.List(model.Float(), thrift_id=15) 

    #@doc average current over 60 minutes timespan 
    currentaverage60minutes = model.Float(thrift_id=16) 

   
    #@doc powerfactor, when requesting the monitor information
    powerfactor = model.Float(thrift_id=17)
    
    #@doc timestamp  
    timestamp = model.DateTime(thrift_id=18)
    

    
class sensorporttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('AIRFLOWSENSOR')
        cls.registerItem('HUMIDITYSENSOR')        
        cls.registerItem('TEMPERATURESENSOR')        
        cls.finishItemRegistration()

# @doc monitoring sensor port information of a power device
class sensorportmonitoringinfo(model.Model):
    
    #@doc status, listed in the enumerator PortStatusType
    sensortype = model.Enumeration(sensorporttype,thrift_id=1)

    #@doc value, when requesting the monitor information.
    value = model.Float(thrift_id=2) 

    #@doc minimum value occurred, between two monitoring requests
    valuemin = model.Float(thrift_id=3)
    
    #@doc maximum value occurred, between two monitoring requests
    valuemax = model.Float(thrift_id=4)
      
    #@doc average value over 5 minutes timespan 
    value5minuteaverages =model.List(model.Float(), thrift_id=15)

    #@doc average value over 60 minutes timespan 
    valueaverage60minutes = model.Float(thrift_id=10) 

    #@doc maximum value over 60 minutes timespan 
    valuemax60minutes = model.Float(thrift_id=11) 
    
    #@doc timestamp 
    timestamp = model.DateTime(thrift_id=12)
  
from acl import acl
# @doc Monitoring info object
class monitoringinfo(model.RootObjectModel):
    
    #@doc guid of related the power device
    meteringdeviceguid = model.GUID(thrift_id=1)
    
    #@doc list of port monitoring info objects
    ports = model.List(model.Object(portmonitoringinfo),thrift_id=2)
    
    #@doc list of sensor port monitoring info objects
    sensors = model.List(model.Object(sensorportmonitoringinfo),thrift_id=3)

    #@doc access control list
    acl = model.Object(acl,thrift_id=4)