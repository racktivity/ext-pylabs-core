__author__ = 'incubaid'

def main(q, i, p, params, tags):
    businessparams = p.api.model.datacenter.businessparams.new()
    businessparams.name = params['name']
    businessparams.size = params['size']
    businessparams.racksurface = params['racksurface']
    businessparams.kwhourcost = params['kwhourcost']
    businessparams.pue = params['pue']
    businessparams.salescollocation = params['salescollocation']
    businessparams.salescpu = params['salescpu']
    businessparams.salesstorage = params['salesstorage']
    businessparams.salesbandwidth = params['salesbandwidth']
    businessparams.collocation = params['collocation']
    businessparams.storage = params['storage']
    businessparams.cpu = params['cpu']
    businessparams.leasebuilding= params['leasebuilding']
    businessparams.leaseinfrastructure= params['leaseinfrastructure']
    businessparams.leasehw= params['leasehw']
    businessparams.interestbuilding= params['interestbuilding']
    businessparams.interestdatacenter= params['interestdatacenter']
    businessparams.leaseperiodbuilding= params['leaseperiodbuilding']
    businessparams.leaseperioddatacenter= params['leaseperioddatacenter']
    businessparams.technology= params['technology']
    businessparams.installperiod= params['installperiod']
    p.api.model.datacenter.businessparams.save(businessparams)

    params['result'] = {'guid' : businessparams.guid,
                        'name': businessparams.name,
                        'size': businessparams.size,
                        'racksurface' : businessparams.racksurface,
                        'kwhourcost': businessparams.kwhourcost,
                        'pue': businessparams.pue,
                        'salescollocation': businessparams.salescollocation,
                        'salescpu': businessparams.salescpu,
                        'salesstorage': businessparams.salesstorage,
                        'salesbandwidth': businessparams.salesbandwidth,
                        'collocation': businessparams.collocation,
                        'storage': businessparams.storage,
                        'cpu': businessparams.cpu,
 			'leasebuilding' : businessparams.leasebuilding,
			'leaseinfrastructure': businessparams.leaseinfrastructure,
			'leasehw' : businessparams.leasehw,
			'interestbuilding' : businessparams.interestbuilding,
			'interestdatacenter' : businessparams.interestdatacenter,
			'leaseperiodbuilding' : businessparams.leaseperiodbuilding,
			'leaseperioddatacenter' : businessparams.leaseperioddatacenter,
			'technology' : businessparams.technology,
			'installperiod' : businessparams.installperiod}

