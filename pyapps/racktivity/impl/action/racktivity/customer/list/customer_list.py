__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'customerinfo': rootobjectaction_list.customer_list(customerguid=params['customerguid'])}

def match(q, i, params, tags):
    return True
