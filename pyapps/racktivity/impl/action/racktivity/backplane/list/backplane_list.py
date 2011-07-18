__author__ = 'racktivity'
__tags__ = 'backplane', 'list'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    params['result'] = {'returncode':True, 'backplaneinfo': rootobjectaction_list.backplane_list(backplaneguid=params["backplaneguid"])}

def match(q, i, params, tags):
    return True
