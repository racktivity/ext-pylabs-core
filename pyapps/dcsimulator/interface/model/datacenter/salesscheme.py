import pymodel as model

#@doc Sales scheme of datacenter
class salesscheme(model.RootObjectModel):
	#@doc rental per rack in kEur/month
	collocation = model.Float(thrift_id = 1)

	#@doc sales of cpu rack in kEur/month
	cpu = model.Float(thrift_id = 2)

    #@doc sales of storage rack in kEur/month
	storage = model.Float(thrift_id = 3)

	#@doc sales of bandwidth in Eur per Mbps per month
	bandwidth = model.Float(thrift_id = 4)

