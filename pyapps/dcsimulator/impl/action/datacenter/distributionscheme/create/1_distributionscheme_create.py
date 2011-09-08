__author__ = 'incubaid'

def main(q, i, p, params, tags):
    distributionscheme = p.api.model.datacenter.distributionscheme.new()
    distributionscheme.collocation = params['collocation']
    distributionscheme.storage = params['storage']
    distributionscheme.cpu = params['cpu']
    p.api.model.datacenter.distributionscheme.save(distributionscheme)

    params['result'] = {'guid': distributionscheme.guid,
						'collocation': distributionscheme.collocation,
						'storage': distributionscheme.storage,
						'cpu': distributionscheme.cpu
						}

