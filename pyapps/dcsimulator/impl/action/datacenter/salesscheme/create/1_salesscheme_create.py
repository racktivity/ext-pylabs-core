__author__ = 'incubaid'

def main(q, i, p, params, tags):
    salesscheme = p.api.model.datacenter.salesscheme.new()
    salesscheme.collocation = params['collocation']
    salesscheme.cpu = params['cpu']
    salesscheme.storage = params['storage']
    salesscheme.bandwidth = params['bandwidth']
    p.api.model.datacenter.salesscheme.save(salesscheme)
    
    params['result'] = {'guid': salesscheme.guid,
    					'collocation': salesscheme.collocation,
    					'cpu': salesscheme.cpu,
    					'storage': salesscheme.storage,
    					'bandwidth': salesscheme.bandwidth
    					}
    
