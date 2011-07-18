__author__ = 'aserver'
__tags__ = 'backplane', 'setFlags'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    backplane = q.drp.backplane.get(params['backplaneguid'])
    flags = ('publicflag', 'managementflag', 'storageflag')
    for key, valye in params.iteritems():
        if key in flags and value:
            setattr(backplane, key, value)
    q.drp.backplane.save(backplane)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
