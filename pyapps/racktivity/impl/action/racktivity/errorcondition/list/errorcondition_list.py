__author__ = 'racktivity'
__tags__ = 'errorcondition', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode': True, 'errorconditioninfo': rootobjectaction_list.errorcondition_list(errorconditionguid=params['errorconditionguid'])}

def match(q, i, params, tags):
    return True
