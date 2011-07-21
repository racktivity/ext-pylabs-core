__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    lan = p.api.model.racktivity.lan.get(params['languid'])
    
    fields = ('publicflag', 'managementflag', 'storageflag')
    
    for key, value in params.iteritems():
        if key in fields and value and value != "":
            setattr(lan, key, value)
            
                
    p.api.model.racktivity.lan.save(lan)
    params['result'] = {'returncode': True}
    
def match(q, i, params, tags):
    return True
