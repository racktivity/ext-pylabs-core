from xml2collections import xml2Dic, Hook

def User(xmlResponse):
    return xml2Dic(xmlResponse).get('user', Hook())

def Folder(xmlResponse):
    return xml2Dic(xmlResponse).get('folder', Hook())

def Workspace(xmlResponse):
    return xml2Dic(xmlResponse).get('workspace', Hook())

def File(xmlResponse):
    return xml2Dic(xmlResponse).get('file', Hook())

def CollectionContents(xmlResponse):
        return xml2Dic(xmlResponse).get('collectionContents', Hook())
    
def Albums(xmlResponse):
    return xml2Dic(xmlResponse).get('albums', Hook())
        
def Album(xmlResponse):
    return xml2Dic(xmlResponse).get('album', Hook())




