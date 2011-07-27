__author__ = 'racktivity'


import storelib

def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    storeids = params['storeids']
    for storeid in storeids:
        if store.exists(storeid):
            store.destroy(storeid)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True