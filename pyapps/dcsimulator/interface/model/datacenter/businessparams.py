import pymodel as model

#@doc properties of a datacenter business properties scheme
class businessparams(model.RootObjectModel):
    #@doc Name of the datacenter
    name = model.String(thrift_id = 1)
    
    #@doc Total surface of datacenter
    size = model.Integer(thrift_id = 2)
    
    #@doc Total surface that one rack takes
    racksurface = model.Integer(thrift_id = 3)
    
    #@doc Cost per used kWh
    kwhourcost = model.Float(thrift_id = 4)
    
    #@doc power usage effectiveness, ratio effective power needed per theoretical required power
    pue = model.Float(thrift_id = 5)
    
    #@doc rental per rack in kEur/month
    salescollocation = model.Float(thrift_id = 6)

    #@doc sales of cpu rack in kEur/month
    salescpu = model.Float(thrift_id = 7)

    #@doc sales of storage rack in kEur/month
    salesstorage = model.Float(thrift_id = 8)

    #@doc sales of bandwidth in Eur per Mbps per month
    salesbandwidth = model.Float(thrift_id = 9)    
    
    #@doc Percentage of the datacenter building in leasing
    leasebuilding = model.Integer(thrift_id = 10)

    #@doc Percentage of datacenter infrastructure in leasing (airco, power, ...)
    leaseinfrastructure = model.Integer(thrift_id = 11)

    #@doc Percentage of hardware in leasing (servers, storage, ...)
    leasehw = model.Integer(thrift_id = 12)

    #@doc Interest rate when leasing the datacenter building
    interestbuilding = model.Float(thrift_id = 13)

    #@doc Interest rate when leasing the datacenter equipment (infrastructure, servers...)
    interestdatacenter = model.Float(thrift_id = 14)

    #@doc Leasing period for the datacenter building
    leaseperiodbuilding = model.Integer(thrift_id = 15)

    #@doc Leasing period for the datacenter equipment (infrastructure, servers...)
    leaseperioddatacenter = model.Integer(thrift_id = 16)

    #@doc Percentage of technology installed before datacenter becomes active
    technology = model.Integer(thrift_id = 17)

    #@doc Number of months before datacenter is operational
    installperiod = model.Integer(thrift_id = 18)
    
        #@doc percentage of racks used for collocation
    collocation = model.Integer(thrift_id = 19)

    #@doc percentage of racks used for storage nodes
    storage = model.Integer(thrift_id = 20)

    #@doc percentage of racks used for cpu nodes
    cpu = model.Integer(thrift_id = 21)