__author__ = 'racktivity'

def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    results = dict()
    stores = params['stores']
    for key, storeid in stores.iteritems():
        if not store.exists(storeid):
            results[key] = None
            continue
        data = (store.getAverage(storeid, starttime="e-1d") or 0,
                store.getAverage(storeid, starttime="e-1w") or 0,
                store.getAverage(storeid, starttime="e-1m") or 0,
                store.getAverage(storeid, starttime="e-1y") or 0)
        results[key] = data
    params['result'] = {'returncode': True, 'values': results}

def match(q, i, params, tags):
    return True
