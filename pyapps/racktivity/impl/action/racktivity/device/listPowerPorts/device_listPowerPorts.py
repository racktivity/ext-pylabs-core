__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}

    filterObject = p.api.model.racktivity.device.getFilterObject()
    filterObject.add('racktivity_view_device_powerports', 'guid' , params['deviceguid'])
    result = p.api.model.racktivity.device.findAsView(filterObject,'racktivity_view_device_powerports')

    params['result'] = {'returncode': True, 'powerports': result}

def match(q, i, params, tags):
    return True