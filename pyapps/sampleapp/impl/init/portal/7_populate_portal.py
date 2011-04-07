import os 
import re
import functools

def main (q,i,p,params,tags):
    appName = params['appname']
    appDir = q.system.fs.joinPaths( q.dirs.pyAppsDir, appName )
    MD_PATH = q.system.fs.joinPaths( appDir, 'portal', 'spaces' )
    serverapi = p.application.getAPI(appName,context=q.enumerators.AppContext.APPSERVER)
    connection = p.application.getAPI(appName).action
    macros_homepage = None
    
    for folder in q.system.fs.listDirsInDir(MD_PATH):
        files = q.system.fs.listFilesInDir(folder, filter='*.md', recursive=True)
        space = folder.split(os.sep)[-1]
    
        for f in files:
            name = q.system.fs.getBaseName(f).split('.')[0]
            content = q.system.fs.fileGetContents(f)
    
            # Check if page exists
            #f = connection.ui.page.getFilterObject()
            #f.add('ui_view_page_list', 'name', name, True)
            #f.add('ui_view_page_list', 'space', space, True)
            page_info = connection.ui.page.find(name=name, space=space, exact_properties=("name", "space"))
            if len(page_info['result']) > 1:
                raise ValueError('Multiple pages found ? ' )
            elif len(page_info['result']) == 1:
                page = connection.ui.page.getObject(page_info['result'][0])
                save_f = functools.partial( connection.ui.page.update, page.guid )
            else:
                page = serverapi.model.ui.page.new()
                page.name = name
                page.space = space
                page.category = 'portal'
                save_f = connection.ui.page.create
    
            if name.startswith('Macro') and name not in ['Macros_Home', 'Macros']:
                if not macros_homepage:
                    #check if Macros_Home page is already created, then get its guid to set it as parent guid to other macro pages
                    filter = connection.ui.page.getFilterObject()
                    filter.add('ui_view_page_list', 'name', 'Macros_Home', True)
                    filter.add('ui_view_page_list', 'space', space, True)
                    macros_page_info = connection.ui.page.findAsView(filter, 'ui_view_page_list')
                    if len(macros_page_info) == 1:
                        macros_homepage = connection.ui.page.get(macros_page_info[0]['guid'])
                page.parent = macros_homepage.guid
    
            # content
            page.content = content if content else 'empty'
    
            # tags
            if page.tags:
                t = page.tags.split(' ')
            else:
                t = []
            tags = set(t)
    
            # page and space 
            tags.add('space:%s' % space)
            tags.add('page:%s' % name)
    
            # split CamelCase in tags
            for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                tags.add(tag)
    
            p.tags = ' '.join(tags)
            save_f (page.name, page.space, page.category, page.parent, page.tags, page.content)
