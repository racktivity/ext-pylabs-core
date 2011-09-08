__author__ = "Incubaid"

FIELDS = []
FIELDS.append("leasebuilding")
FIELDS.append("installperiod")
FIELDS.append("interestbuilding")
FIELDS.append("leasehw")
FIELDS.append("leaseperiodbuilding")
FIELDS.append("leaseperioddatacenter")
FIELDS.append("interestdatacenter")
FIELDS.append("leaseinfrastructure")
FIELDS.append("technology")
TYPE = "investmentscheme"
DOMAIN = "datacenter"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def get_model_handle(p):
    return p.api.model.datacenter.investmentscheme

def main(q, i, p, params, tags):
    handle = get_model_handle(p)

    f = handle.getFilterObject()

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not searching for field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None or value=='' :
            q.logger.log("Field %s is None: not searching for field %s" % (field, field), 7)
            continue

        q.logger.log("Adding filter on field %s with value value %s" % (field, value), 7)
        f.add(VIEW, field, value)

    result = handle.findAsView(f, VIEW)
    params['result'] = result
