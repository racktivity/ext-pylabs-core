__author__ = 'racktivity'
__tags__ = 'lan', 'setFlags'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    lan = q.drp.lan.get(params['languid'])
    
    fields = ('publicflag', 'managementflag', 'storageflag')
    
    for key, value in params.iteritems():
        if key in fields and value and value != "":
            setattr(lan, key, value)
            
                
    q.drp.lan.save(lan)
    params['result'] = {'returncode': True}
    
def match(q, i, params, tags):
    return True
