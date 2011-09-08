__author__ = "Incubaid"

TYPE = "investmentscheme"
GUID_FIELD = "%sguid" % TYPE

def main(q, i, p, params, tags):
    if GUID_FIELD not in params:
        raise ValueError("Cannot delete %s, there is no %s key in the params" % (TYPE, GUID_FIELD))
    guid = params[GUID_FIELD]

    p.api.model.datacenter.investmentscheme.delete(guid)
    params['result'] = True
