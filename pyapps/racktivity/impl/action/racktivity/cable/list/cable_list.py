__author__ = 'racktivity'
__tags__ = 'cable', 'list'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'cableinfo': rootobjectaction_list.cable_list(cableguid=params['cableguid'])}

def match(q, i, params, tags):
    return True

