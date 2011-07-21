__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    backplane = p.api.model.racktivity.backplane.get(params['backplaneguid'])
    flags = ('publicflag', 'managementflag', 'storageflag')
    for key, valye in params.iteritems():
        if key in flags and value:
            setattr(backplane, key, value)
    p.api.model.racktivity.backplane.save(backplane)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
