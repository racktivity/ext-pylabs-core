class MeteringDevice():
   """
    actor actions
    most of the actions have to do with a meteringdevice (e.g in fact this is the rackcontroller SAL )
   """
   
   
   def getMonitoringInfo(self, devicetype, deviceipaddress, deviceapiport,  login, password, deviceid="", request="", jobguid="", executionparams=dict()):
       """
       Get the MonitoringInfo from a device and return this in a dictionary which has the same structure as the monitoringinfo object of a meteringdevice.

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress
       
       @param deviceapiport: Ip port on which the device api is reachable.
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: string
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result and sensormonitoringinfo, jobguid: {'result': True, 'jobguid': guid, 'monitoringinfo': {}}
       @rtype:                  dictionary
       """
       
        
   def powerOnPowerPort(self, devicetype, deviceipaddress, deviceapiport, deviceid, portid, login, password, request="", jobguid="", executionparams=dict()):
       """
       Power On port on a meteringdevice

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param portid: Id of the port, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
       @rtype:                  dictionary
       """
   
   def powerOffPowerPort(self, devicetype, deviceipaddress, deviceapiport, deviceid, portid, login, password, request="", jobguid="", executionparams=dict()):
       """
       Power Off port on a meteringdevice

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param portid: Id of the port, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result and jobguid: {'result': True, 'jobguid': guid}
       @rtype:                  dictionary
       """
        
   def getPowerPortStatus(self, devicetype, deviceipaddress, deviceapiport, deviceid, portid, login, password, request="", jobguid="", executionparams=dict()):
        """
        Get the status of a power port on a meteringdevice

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param portid: Id of the port, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, portStatus which is True for On or False for Off: {'result': True,  'jobguid': guid, portStatus= Boolean}
       @rtype:                  dictionary
        """
        
   def getSensorData(self, devicetype, deviceipaddress, deviceapiport, deviceid, sensorid, datatype,login, password,  request="", jobguid="", executionparams=dict()):
        """
        Get a specific sensor metering value, several tasklets will implement this function use type to select the correct sensor information type.
        E.g humidity, temperature, ...

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param sensorid: Id of the sensorid, e.g for a racktivity device this is the sensorlabel.
       @param portid: String
       
       @param datatype: type of the sensor data to receive E.g humidity, temperature. This type will match to a tasklet which will return the correct information
       @param datatype: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid, value:}
       @rtype:                  dictionary
        """
        
   def getDeviceData(self, devicetype, deviceipaddress, deviceapiport, deviceid,  datatype, login, password,request="", jobguid="", executionparams=dict()):
        """
        Get a specific device metering  value, several tasklets will implement this function, use type to select the correct port type information you need
        E.g. Totalcurrent, Totalpower, Totalenergy ... 
        If datatype is all, the returned result will be a dict with a list of devicedata:
        Format:
               

            {Voltage:, MaxTotalCurrent:, MaxVoltage:, MinVoltage:, Frequency:,
              Ports:[{sequence:, ActiveEnergy:,ApparentEnergy: Power:, CurrentPortState:, Current:, MaxCurrent:, MaxPower},...],
              Sensors: [{sequence:, type:,sensorvalue:, maxvalue:, minvalue:}]
            }

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param powerportid: Id of the powerport, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param datatype: type of port information we need to receive. E.g current, power, energy. This type will match to a tasklet which will return the correct information
       @param datatype: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid, value:}
       @rtype:                  dictionary
        """
        
   def getPortData(self, devicetype, deviceipaddress, deviceapiport, deviceid, powerportid, datatype, login, password,request="", jobguid="", executionparams=dict()):
        """
        Get a specific port metering  value, several tasklets will implement this function, use type to select the correct port type information you need
        E.g. current, power, energy ... 

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param powerportid: Id of the powerport, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param datatype: type of port information we need to receive. E.g current, power, energy. This type will match to a tasklet which will return the correct information
       @param datatype: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid, value:}
       @rtype:                  dictionary
        """
        
   def setPortData(self, devicetype, deviceipaddress, deviceapiport, deviceid, powerportid, datatype, datavalue, login, password,request="", jobguid="", executionparams=dict()):
        """
        Set a specific port metering  value, several tasklets will implement this function
        E.g. PortName, ...

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param powerportid: Id of the powerport, e.g for a racktivity device this is the portnumber.
       @param portid: String
       
       @param datatype: type of port information we need to receive. E.g current, power, energy. This type will match to a tasklet which will return the correct information
       @param datatype: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': {'returncode': True}}
       @rtype:                  dictionary
        """
        
   def getConfigurationParameter(self, devicetype, deviceipaddress, deviceapiport, deviceid, configtype, login, password, request="", jobguid="", executionparams=dict()):
        """
        Get a specific configuration parameter.(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param configtype: type of the configuration parameter you wan't to get
       @type configtype: String 
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid, value:}
       @rtype:                  dictionary
        """
        
        
   def setConfigurationParameter(self, devicetype, deviceipaddress, deviceapiport, deviceid, configtype, configvalue, login, password,request="", jobguid="", executionparams=dict()):
        """
        Set a specific configuration parameter(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param configtype: Type of the configuration parameter you wan't to get
       @type configtype: String
       
       @param configvalue: Config value to set on the device
       @type configvalue: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
    
       @param jobguid:   Guid of the job
       @type jobguid:   guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid}
       @rtype:                  dictionary
        """
        
   def setAccount(self, devicetype, deviceipaddress, deviceapiport, login, password, newlogin, newpassword, usertype, request="", jobguid="", executionparams=dict()):
        """
        Set a specific configuration parameter(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param configtype: Type of the configuration parameter you wan't to get
       @type configtype: String
       
       @param configvalue: Config value to set on the device
       @type configvalue: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
    
       @param jobguid:   Guid of the job
       @type jobguid:   guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid}
       @rtype:                  dictionary
        """
        
   def setThresholdOnPowerPort(self, devicetype, deviceipaddress, deviceapiport, deviceid, portnumber, configtype, configvalue, login, password,request="", jobguid="", executionparams=dict()):
        """
        Set a specific configuration parameter(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param portnumber: port id (sequence) on the module to set threshold on
       @type: Integer
       
       @param configtype: Type of the configuration parameter you wan't to get
       @type configtype: String
       
       @param configvalue: Config value to set on the device
       @type configvalue: String
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
    
       @param jobguid:   Guid of the job
       @type jobguid:   guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid}
       @rtype:                  dictionary
        """
   def discover(self, agentguid, ipaddress, port, communitystring, request="", jobguid="", executionparams=dict()):
       """
       Discovers an IP address, and returns an structure with the device information in the form
       {'product': <product name>: 'version': <product version', 'date': <product version>,
        'ports': [{label: <port label>, sequence: <port sequence>}, ...],
        'sensors': [{label: <sensor label>, sequence: <sensor sequence>, sensortype: <sensor type>}, ...]}
        
        @param agentguid: The agent guid
        @type: guid
        
        @param ipaddress: The ip address to discover
        @type: string of ip address
        
        @param ipaddress: The SNMP port of the device
        @type: int
        
        @param communitystring: The SNMP community string
        @type: string
        
        @param jobguid:   Guid of the job
       @type jobguid:   guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, and 'device' which is the result of the discovery in the
                                descriped format above {'jobguid': guid, 'result' : {'returncode': True,  'device': device}}
       
       @rtype:                  dictionary
       """
   def getThresholdOnPowerPort(self, devicetype, deviceipaddress, deviceapiport, deviceid, portnumber, configtype, login, password, request="", jobguid="", executionparams=dict()):
        """
        Get a specific configuration parameter.(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param portnumber: port id (sequence) on the module to set threshold on
       @type: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param configtype: type of the configuration parameter you wan't to get
       @type configtype: String 
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
       
       @param jobguid:          Guid of the job
       @type jobguid:           guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid, value:}
       @rtype:                  dictionary
        """
        
   def setPowerPortStartupDelay(self, devicetype, deviceipaddress, deviceapiport, deviceid, portnumber, delay , login, password,request="", jobguid="", executionparams=dict()):
        """
        Set a specific configuration parameter(e.g oledbrightness, ipaddress, ...)

       @param devicetype: type of the device
       @type  devicetype: q.enumerators.meteringdevicetype
       
       @param deviceipaddress: Ipaddress of the meteringdevice(e.g ipaddress to contact the api)
       @type deviceipaddress: Ipaddress 
       
       @param deviceapiport: Ip port on which the device api is reachable
       @type deviceapiport: Integer
       
       @param deviceid: Optional device id, e.g for a racktivity device this is P1, T1, ...
       @type deviceid: String
       
       @param portnumber: port id (sequence) on the module to set threshold on
       @type: Integer
       
       @param delay: startup delay to set on the device
       @type configvalue: Integer
       
       @param login: login name to login on the meteringdevice
       @param login: String
       
       @param password: password of the meteringdevice
       @param password: String
    
       @param jobguid:   Guid of the job
       @type jobguid:   guid

       @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
       @type executionparams:   dictionary

       @return:                 dictionary with True as result, jobguid, value which is the result of the required information {'result': True,  'jobguid': guid}
       @rtype:                  dictionary
        """
