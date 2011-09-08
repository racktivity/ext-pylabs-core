__author__ = 'incubaid'

def main(q, i, p, params, tags):
    investmentscheme = p.api.model.datacenter.investmentscheme.new()
    investmentscheme.leasebuilding= params['leasebuilding']
    investmentscheme.leaseinfrastructure= params['leaseinfrastructure']
    investmentscheme.leasehw= params['leasehw']
    investmentscheme.interestbuilding= params['interestbuilding']
    investmentscheme.interestdatacenter= params['interestdatacenter']
    investmentscheme.leaseperiodbuilding= params['leaseperiodbuilding']
    investmentscheme.leaseperioddatacenter= params['leaseperioddatacenter']
    investmentscheme.technology= params['technology']
    investmentscheme.installperiod= params['installperiod']
    p.api.model.datacenter.investmentscheme.save(investmentscheme)

    params['result'] = {'guid' : investmentscheme.guid,
 			'leasebuilding' : investmentscheme.leasebuilding,
			'leaseinfrastructure': investmentscheme.leaseinfrastructure,
			'leasehw' : investmentscheme.leasehw,
			'interestbuilding' : investmentscheme.interestbuilding,
			'interestdatacenter' : investmentscheme.interestdatacenter,
			'leaseperiodbuilding' : investmentscheme.leaseperiodbuilding,
			'leaseperioddatacenter' : investmentscheme.leaseperioddatacenter,
			'technology' : investmentscheme.technology,
			'installperiod' : investmentscheme.installperiod}

