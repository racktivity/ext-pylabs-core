__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': p.api.model.racktivity.meteringdeviceevent.delete(params['meteringdeviceeventguid'])}

def match(q, i, params, tags):
    return True