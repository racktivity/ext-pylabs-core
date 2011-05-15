__author__ = "incubaid"

def main(q, i, p, params, tags):
    global space
    global children_str
    macro_tags = params['tags'].tags

    appname = p.api.appname
    alkira_client = q.clients.alkira.getClient('127.0.0.1', appname)

    depth = int(macro_tags['depth'])
    space = macro_tags['space']
    if macro_tags.get('root', 'self') == 'self':
        root_page = macro_tags['page']
    else:
        root_page = macro_tags['root']

    all_pages = alkira_client.listPages(space)
    tree = {root_page:{}}

    def childPages(root, pages, tree, tree_depth):
        tree_depth -= 1
        children = {}
        root_guid = alkira_client.getPage(space, root).guid

        for page in pages:
            page_parent = alkira_client.getPage(space, page).parent
            if root_guid == page_parent:
                children.update({page:{}})
                all_pages.remove(page)
        tree[root].update(children)
        if  tree_depth > 0:
            for child in tree[root].keys():
                childPages(child, all_pages, tree[root], tree_depth)
        return tree

    values = childPages(root_page, all_pages, {root_page:{}}, depth)
    children_str = ""

    def treePrint(indent, value_dict):
        if value_dict:
            for item in value_dict:
                global children_str
                global space
                page_name = item.replace("_", "\_")
                children_str += indent*' ' + "* <a href='/" + appname + '/#/' + space + '/' + item + "'>" + page_name + '</a>  \n'
                treePrint(indent+4, value_dict[item])

    treePrint(0, values)

    result = """
__Children:__
 
%s
- - -
    """%(children_str)
    params['result'] = result 
