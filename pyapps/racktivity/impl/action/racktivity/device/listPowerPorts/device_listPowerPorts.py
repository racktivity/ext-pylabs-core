__author__ = 'racktivity'
__tags__ = 'device', 'listPowerPorts'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}

    filterObject = q.drp.device.getFilterObject()
    filterObject.add('view_device_powerports', 'guid' , params['deviceguid'])
    result = q.drp.device.findAsView(filterObject,'view_device_powerports')

    params['result'] = {'returncode': True, 'powerports': result}

def match(q, i, params, tags):
    return True