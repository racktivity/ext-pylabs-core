__author__ = 'racktivity'

def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    result = {}
    for storeid in params['storeids']:
        result[storeid] = store.getRange(storeid, params["resolution"],
                                          starttime=params["start"], stoptime=params["stop"],
                                          aggregationfunction=params["aggregationtype"])
    
    params['result'] = {'returncode': True, 'data': result}

def match(q, i, params, tags):
    return True
