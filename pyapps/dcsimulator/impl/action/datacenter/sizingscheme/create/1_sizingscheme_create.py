__author__ = 'incubaid'

def main(q, i, p, params, tags):
    sizingscheme = p.api.model.datacenter.sizingscheme.new()
    sizingscheme.size = params['size']
    sizingscheme.racksurface = params['racksurface']
    sizingscheme.kwhourcost = params['kwhourcost']
    sizingscheme.pue = params['pue']
    p.api.model.datacenter.sizingscheme.save(sizingscheme)
    
    params['result'] = {'guid': sizingscheme.guid,
    					'size': sizingscheme.size,
    					'racksurface': sizingscheme.racksurface,
    					'kwhourcost': sizingscheme.kwhourcost,
    					'pue': sizingscheme.pue
    					}

