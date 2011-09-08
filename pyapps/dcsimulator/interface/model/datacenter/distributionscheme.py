import pymodel as model

#@doc Distribution scheme of racks in a datacenter
class distributionscheme(model.RootObjectModel):
	#@doc percentage of racks used for collocation
	collocation = model.Integer(thrift_id = 1)

	#@doc percentage of racks used for storage nodes
	storage = model.Integer(thrift_id = 2)

	#@doc percentage of racks used for cpu nodes
	cpu = model.Integer(thrift_id = 3)

