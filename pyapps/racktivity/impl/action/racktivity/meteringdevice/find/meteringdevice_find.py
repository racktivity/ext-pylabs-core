__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True, 'guidlist': rootobjectaction_find.meteringdevice_find(name=params['name'],
                                                                                                  id=params['id'],
                                                                                                  meteringdevicetype=params['meteringdevicetype'],
                                                                                                  template=params['template'],
                                                                                                  thresholdguid=params['thresholdguid'],
                                                                                                  rackguid=params['rackguid'],
                                                                                                  cableguid=params['cableguid'],
                                                                                                  parentmeteringdeviceguid=params['parentmeteringdeviceguid'],
                                                                                                  clouduserguid=params['clouduserguid'],
                                                                                                  height=params['height'],
                                                                                                  positionx=params['positionx'],
                                                                                                  positiony=params['positiony'],
                                                                                                  positionz=params['positionz'],
                                                                                                  ipaddressguid=params['ipaddressguid'],
                                                                                                  tags=params['tags'],
                                                                                                  meteringdeviceconfigstatus=params['meteringdeviceconfigstatus'])}

def match(q, i, params, tags):
    return True
