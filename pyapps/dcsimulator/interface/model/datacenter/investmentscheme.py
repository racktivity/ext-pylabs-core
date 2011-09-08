import pymodel as model

#@doc class that provides the properties of an datacenter investment scheme
class investmentscheme(model.RootObjectModel):
    #@doc Percentage of the datacenter building in leasing
	leasebuilding = model.Integer(thrift_id = 1)

	#@doc Percentage of datacenter infrastructure in leasing (airco, power, ...)
	leaseinfrastructure = model.Integer(thrift_id = 2)

	#@doc Percentage of hardware in leasing (servers, storage, ...)
	leasehw = model.Integer(thrift_id = 3)

	#@doc Interest rate when leasing the datacenter building
	interestbuilding = model.Float(thrift_id = 4)

	#@doc Interest rate when leasing the datacenter equipment (infrastructure, servers...)
	interestdatacenter = model.Float(thrift_id = 5)

	#@doc Leasing period for the datacenter building
	leaseperiodbuilding = model.Integer(thrift_id = 6)

	#@doc Leasing period for the datacenter equipment (infrastructure, servers...)
	leaseperioddatacenter = model.Integer(thrift_id = 7)

	#@doc Percentage of technology installed before datacenter becomes active
	technology = model.Integer(thrift_id = 8)

	#@doc Number of months before datacenter is operational
	installperiod = model.Integer(thrift_id = 9)

