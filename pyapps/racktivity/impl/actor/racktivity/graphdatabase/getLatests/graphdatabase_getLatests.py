__author__ = 'racktivity'
__tags__ = 'graphdatabase', 'getLatests'

def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    results = {}
    stores = params['stores']
    for key, storeid in stores.iteritems():
        if store.exists(storeid):
            results[key] = store.getLatest(storeid)
        else:
            results[key] = None

    params['result'] = {'returncode': True, 'values': results}

def match(q, i, params, tags):
    return True
