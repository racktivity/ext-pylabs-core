__author__ = 'racktivity'
__tags__ = 'lan', 'setDefaultGateway'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    lan = q.drp.lan.get(params['languid'])
    lan.gateway = params['gateway']
    q.drp.lan.save(lan)
                        
    params['result'] = {'returncode': True}
    
def match(q, i, params, tags):
    return True