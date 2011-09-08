__author__ = "Incubaid"

FIELDS = []
FIELDS.append("storage")
FIELDS.append("collocation")
FIELDS.append("cpu")
TYPE = "distributionscheme"
GUID_FIELD = "%sguid" % TYPE

def get_model_handle(p):
    return p.api.model.datacenter.distributionscheme

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
