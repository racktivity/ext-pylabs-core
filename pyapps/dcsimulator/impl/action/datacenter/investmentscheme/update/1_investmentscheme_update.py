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
GUID_FIELD = "%sguid" % TYPE

def get_model_handle(p):
    return p.api.model.datacenter.investmentscheme

def main(q, i, p, params, tags):
    handle = get_model_handle(p)

    if GUID_FIELD not in params:
        raise ValueError("Cannot update %s, there is no %s key in the params" % (TYPE, GUID_FIELD))
    guid = params[GUID_FIELD]

    o = handle.get(guid)

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not updating field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None:
            q.logger.log("Field %s is None: not updating field %s" % (field, field), 7)
            continue

        q.logger.log("Updating field %s to value %s" % (field, value), 7)
        setattr(o , field, value)

    handle.save(o)
    params['result'] = True
