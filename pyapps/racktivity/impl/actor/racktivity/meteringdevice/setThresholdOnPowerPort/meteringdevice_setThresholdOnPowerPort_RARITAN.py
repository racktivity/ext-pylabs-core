__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'setThresholdOnPowerPort'

def main(q, i, params, tags):
    raise NotImplementedError()

def match(q, i, params, tags):
    return params['devicetype'] == "raritan"

