__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    
    rackguid = params['rackguid']
    parentguid = params['parentguid']
    
    #import racktivityui.uigenerator
    #import racktivityui.uigenerator.rack
    #racktivityui.uigenerator.deletePage(rackguid)
    #racktivityui.uigenerator.deletePage("%s-graphs" % rackguid)
    #racktivityui.uigenerator.rack.create(rackguid, parentguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
