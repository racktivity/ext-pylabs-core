from pylabs import i,q,p

def create(name="test_logicalview1", view_search_string = "types:{energyswitch,datacenter}, parenttree:{datacenter: 'LOCHRISTI'}, name:{DCMU* || TESTENVIRONMENT* && Mina*}, tags_labels:{DCLOC && usage:storage}",
            description="Logicalview 1 description"):
    ca = p.api.action.racktivity
    guid = ca.logicalview.create(name, description)['result']['logicalviewguid']
    lv = ca.logicalview.getObject(guid)
    if lv.name != name:
        raise Exception('logicalview %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = p.api.action.racktivity
    lv = ca.logicalview.getObject(guid)
    ca.logicalview.delete(guid)
    #Is it really gone?
    res = ca.logicalview.list(guid)['result']['logicalviewinfo']
    if len(res) > 0:
        raise Exception("Logicalview with guid %s still exists"%guid)
