from xml.dom import minidom
import new
import re

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

#http://code.activestate.com/recipes/116539/
#Recipe 116539: turn the structure of a XML-document into a combination of dictionaries and lists

class Hook(object):
    pass

class NotTextNodeError:
    pass

def cleanString(s):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
    return s   

def getTextFromNode(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    t = ""
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            t += n.nodeValue
        else:
            raise NotTextNodeError
    return t


def xml2Dic(xmlDoc):
    return node2Dic(minidom.parseString(xmlDoc))

def node2Dic(node):
    """
    node2Dic() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
    - if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
    - if the node has the attribute "method" set to "true",
    then it's children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
    - else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary).
    """
    dic = {} 
    for n in node.childNodes:
        if n.nodeType != n.ELEMENT_NODE:
            continue
#        if n.hasChildNodes():
        if n.getAttribute("multiple") == "true" or n.nodeName == 'collectionContents':
            # node with multiple children:
            # put them in a list
            childrenDict = {}
            childrenDict.update(dict(n.attributes.items()))
            counter = int(childrenDict.get('start', -1))
            for c in n.childNodes:
                if c.nodeType != n.ELEMENT_NODE:
                    continue
#                childrenDict['%s_%s'%(c.nodeName, counter)] = node2Dic(c)
                childrenDict.update({'%s_%.03d'%(str(c.nodeName), counter) : new.classobj(str('%s_%.03d'%(c.nodeName, counter)), (Hook,), node2Dic(c))})
                if counter > -1: counter += 1
#            dic.update({n.nodeName: childrenDict})
            dic.update({n.nodeName : new.classobj(str(n.nodeName), (Hook,), childrenDict)})
            continue
        
        try:
            text = getTextFromNode(n)
        except NotTextNodeError:
                # 'normal' node
#                dic.update({n.nodeName:node2Dic(n)})
                dic.update({n.nodeName : new.classobj(str(n.nodeName), (Hook,), node2Dic(n))})
                continue
        
            # text node
        dic.update({n.nodeName:text})
        continue
    return dic

if __name__ == '__main__':
    testdata = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><collectionContents start="0" hasMore="false" end="19">
<file><displayName>testfile001</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_346323097</ref><size>-1</size><lastModified>2011-02-28T04:26:27.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file>
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_346336274</ref><size>-1</size><lastModified>2011-02-28T04:30:29.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file>
<file><displayName>testfile003</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_346359590</ref><size>0</size><lastModified>2011-02-28T07:06:31.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_346359590/data</fileData></file>
<file><displayName>mypic</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347205307</ref><size>0</size><lastModified>2011-02-28T07:59:00.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_347205307/data</fileData></file>
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347716746</ref><size>-1</size><lastModified>2011-02-28T09:16:02.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347802605</ref><size>-1</size><lastModified>2011-02-28T09:30:11.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347803221</ref><size>0</size><lastModified>2011-02-28T09:32:59.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_347803221/data</fileData></file><file><displayName>testfile004</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347855514</ref><size>-1</size><lastModified>2011-02-28T09:40:22.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>smallimageonchunk</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_355266259</ref><size>-1</size><lastModified>2011-03-01T05:41:10.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>smallimageonchunk</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_355273970</ref><size>40519</size><lastModified>2011-03-01T05:44:41.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_355273970/data</fileData></file><file><displayName>test_urllib2</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356820535</ref><size>29828</size><lastModified>2011-03-01T10:27:37.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_356820535/data</fileData></file><file><displayName>testurllib2create</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356965074</ref><size>-1</size><lastModified>2011-03-01T11:06:38.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create02</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356970622</ref><size>-1</size><lastModified>2011-03-01T11:08:06.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create03</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356999786</ref><size>-1</size><lastModified>2011-03-01T11:16:32.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create04</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357006151</ref><size>-1</size><lastModified>2011-03-01T11:18:34.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create05</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357106572</ref><size>-1</size><lastModified>2011-03-01T11:45:36.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357112560</ref><size>-1</size><lastModified>2011-03-01T11:46:21.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357117128</ref><size>-1</size><lastModified>2011-03-01T11:46:53.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create07</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357315027</ref><size>-1</size><lastModified>2011-03-01T12:14:02.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357332735</ref><size>29828</size><lastModified>2011-03-01T12:51:54.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_357332735/data</fileData></file></collectionContents>'''
    
    
    testdata2 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><collectionContents start="0" hasMore="false" end="19">
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_346336274</ref><size>-1</size><lastModified>2011-02-28T04:30:29.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file>
<file><displayName>testfile003</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_346359590</ref><size>0</size><lastModified>2011-02-28T07:06:31.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_346359590/data</fileData></file>
<file><displayName>mypic</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347205307</ref><size>0</size><lastModified>2011-02-28T07:59:00.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_347205307/data</fileData></file>
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347716746</ref><size>-1</size><lastModified>2011-02-28T09:16:02.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file>
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347802605</ref><size>-1</size><lastModified>2011-02-28T09:30:11.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file>
<file><displayName>testfile002</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347803221</ref><size>0</size><lastModified>2011-02-28T09:32:59.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_347803221/data</fileData></file>
<file><displayName>testfile004</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_347855514</ref><size>-1</size><lastModified>2011-02-28T09:40:22.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>smallimageonchunk</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_355266259</ref><size>-1</size><lastModified>2011-03-01T05:41:10.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>smallimageonchunk</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_355273970</ref><size>40519</size><lastModified>2011-03-01T05:44:41.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_355273970/data</fileData></file><file><displayName>test_urllib2</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356820535</ref><size>29828</size><lastModified>2011-03-01T10:27:37.000-08:00</lastModified><mediaType>image/jpeg</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_356820535/data</fileData></file><file><displayName>testurllib2create</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356965074</ref><size>-1</size><lastModified>2011-03-01T11:06:38.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create02</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356970622</ref><size>-1</size><lastModified>2011-03-01T11:08:06.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create03</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_356999786</ref><size>-1</size><lastModified>2011-03-01T11:16:32.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create04</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357006151</ref><size>-1</size><lastModified>2011-03-01T11:18:34.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create05</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357106572</ref><size>-1</size><lastModified>2011-03-01T11:45:36.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357112560</ref><size>-1</size><lastModified>2011-03-01T11:46:21.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357117128</ref><size>-1</size><lastModified>2011-03-01T11:46:53.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create07</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357315027</ref><size>-1</size><lastModified>2011-03-01T12:14:02.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>false</presentOnServer></file><file><displayName>testurllib2create06</displayName><ref>https://api.sugarsync.com/file/:sc:977916:31_357332735</ref><size>29828</size><lastModified>2011-03-01T12:51:54.000-08:00</lastModified><mediaType>text/xml</mediaType><presentOnServer>true</presentOnServer><fileData>https://api.sugarsync.com/file/:sc:977916:31_357332735/data</fileData></file></collectionContents>'''
    result =  xml2Dic(testdata)['collectionContents']
    print result



