__author__ = "Incubaid"

TYPE = "distributionscheme"
GUID_FIELD = "%sguid" % TYPE

def main(q, i, p, params, tags):
    if GUID_FIELD not in params:
        raise ValueError("Cannot retrieve %s, there is no %s key in the params" % (TYPE, GUID_FIELD))
    guid = params[GUID_FIELD]

    o = p.api.model.datacenter.distributionscheme.get(guid)
    params['result'] = o
