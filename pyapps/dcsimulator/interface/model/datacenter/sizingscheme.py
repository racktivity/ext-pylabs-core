import pymodel as model

#@doc Sizing scheme of datacenter
class sizingscheme(model.RootObjectModel):
	#@doc datacenter size in square meters
	size = model.Integer(thrift_id = 1)

	#@doc required square meters per rack
	racksurface = model.Integer(thrift_id = 2)

    #@doc cost per kW/h
	kwhourcost = model.Float(thrift_id = 3)

	#@doc power usage effectiveness, ratio effective power needed per theoretical required power
	pue = model.Float(thrift_id = 4)

