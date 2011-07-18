__author__ = 'racktivity'
__tags__ = 'meteringdeviceevent', 'delete'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': q.drp.meteringdeviceevent.delete(params['meteringdeviceeventguid'])}

def match(q, i, params, tags):
    return True