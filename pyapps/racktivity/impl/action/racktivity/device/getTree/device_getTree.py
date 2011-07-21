__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    from rootobjectaction_lib import rootobject_tree
    params['result'] = {"returncode":True, "tree":rootobject_tree.getTree(params["deviceguid"], params["depth"])}

def match(q, i, params, tags):
    return True


