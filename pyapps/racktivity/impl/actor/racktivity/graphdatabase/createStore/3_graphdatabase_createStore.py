__author__ = 'racktivity'


def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    store.create(params['storeid'])
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True