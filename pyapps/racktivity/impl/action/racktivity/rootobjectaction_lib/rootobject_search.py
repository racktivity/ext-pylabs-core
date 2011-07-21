from rootobjectaction_lib import rootobject_tree
from pylabs import q,p

def getGuids(q, types, names, tags):
    #SELECT X.root,X.guid FROM  (SELECT 'datacenter' AS root,guid FROM datacenter.view_datacenter_list UNION SELECT 'room' AS root,guid FROM room.view_room_list) as X
    
    sqlstr = "SELECT guid, name, type, tags FROM parenttree WHERE "
    if types:
        sqlstr += "type in ('" + "','".join(types) + "') "
    if names:
        if sqlstr.endswith("WHERE "):
            sqlstr += "("
        else:
            sqlstr += "AND ("

        for nidx, andnames in enumerate(names):
            nlastidx = len(names) -1
            str = " AND ".join(andnames)
            if nidx != nlastidx:
                str += " OR "
            sqlstr += str
        sqlstr += ")"
    #Fill tags list
    if tags:
        if sqlstr.endswith("WHERE "):
            sqlstr += "("
        else:
            sqlstr += "AND ("

        glastidx = len(tags) -1
        for gidx, andtags in enumerate(tags):
            str = " AND ".join(andtags)
            if gidx != glastidx:
                str += " OR "
            sqlstr += str
        sqlstr += ")"
    #If no result, select all
    if sqlstr.endswith("WHERE "):
        sqlstr = "SELECT guid, name, type, tags FROM parenttree"
    return p.api.model.racktivity.racktivity.query(sqlstr)

def parentFilter(data, parenttree): #No, its not what u think it is
    type, name = parenttree
    #Get guid of the parent I am searching for
    pguid = rootobject_tree.getObjectGuid(name, type)
    if not pguid:
        return []
    #Use this guid to get this object's children guids
    guids = rootobject_tree.getChildrenGuids(pguid)
    #use it for filtering
    
    c = 0
    while (c < len(data)):
        key = data[c]
        if key["guid"] not in guids:
            data.remove(key)
        else:
            c += 1
    return data

def prepareDataForSql(data):
    #Get the searched names
    if "name" in data:
        arrnames = list()
        for orname in data["name"].split("||"):
            andnames = list()
            for andname in orname.split("&&"):
                andname = andname.strip()
                andname = andname.replace("*", "%")
                andnames.append("name LIKE '" + andname + "'")
            arrnames.append(andnames)
    else:
        arrnames = None
    #Get the searched 
    if "tags_labels" in data:
        arrlabels = list()
        for orlabel in data["tags_labels"].split("||"):
            andlabels = list()
            for andlabel in orlabel.split("&&"):
                andlabels.append("tags SIMILAR TO '%(^| )" + andlabel.strip() + "($| )%'")
            arrlabels.append(andlabels)
    else:
        arrlabels = None
    #Get parentGuid
    if "parenttree" in data:
        parenttree = data["parenttree"].split(":")
        parenttree[0] = parenttree[0].strip("'\" ")
        parenttree[1] = parenttree[1].strip("'\" ")
    else:
        parenttree = None
    return arrnames, arrlabels, parenttree


def search(searchstr, aggregated = False):
    """"
        Search used for searching using logicalview search string
        aggregated determine if search should return aggregated data in the result
    """
    #sample search: "types:{energyswitch,datacenter}, parenttree:{datacenter: 'LOCHRISTI'}, name:{DCMU* || TESTENVIRONMENT* && Mina*}, tags_labels:{DCLOC && usage:storage}"
    import re
    
    arr = re.findall("([a-z_]*) *: *\{([^\}]*)\}", searchstr)
    data = dict()
    for key,value in arr:
        data[key.strip("'\" ")] = value.strip("'\" ")
    del arr
    #Validate keywords
    validKeywords = ("types", "parenttree", "name", "tags_labels")
    for key in data:
        if key not in validKeywords:
            raise ValueError("Unknown keyword %s"%key)
    #put the type in the right format
    if "types" in data:
        types = list()
        for type in data["types"].split(","):
            types.append(type.strip())
    else:
        types = None

    #The way I search for port/sensor is totally different than the way I search for a rootobject
    if types and len(types) == 1 and types[0] in ("energyswitch_port", "energyswitch_sensor"):
        if types[0] == "energyswitch_sensor":
            raise NotImplemented("energyswitch_sensor type is not yet implemented")
        if "parenttree" not in data or not data["parenttree"].startswith("energyswitch"):
            raise ValueError("parenttree must be specified when searching for port/sensor and it must be an energyswitch")
        ptype , pname = data["parenttree"].split(":")
        mdguid = rootobject_tree.getObjectGuid(name, "meteringdevice")
        if not mdguid:
            return
        #Get the metering device that I found
        md = p.api.model.racktivity.meteringdevice.get(mdguid)
        #Prepare the search string
        searchstr = re.escape(data["name"])
        #after escapping convert \\* into .* [to allow the use of * as wild card]
        searchstr = searchstr.replace("\\*", ".*")
        q.logger.log("#! Search string %s"%searchstr)
        result = list()
        for port in md.poweroutputs:
            if re.match(searchstr, port.label):
                key = {"name":port.label, "description":"", "guid": md.guid, "type":"powerport"}
                data = p.api.action.racktivity.meteringdevice.getViewData(md.guid, portlabel=port.label)["result"]["data"]
                for item in data:
                    item['viewdatastr'] = "%0.1f"%item["viewdatavalue"]
                key["data"] = data
                #Add this port to the result
                result.append(key)
    else:
        arrnames, arrlabels, parenttree = prepareDataForSql(data)
        #Do the query
        result = getGuids(q, types, arrnames, arrlabels)
        if parenttree:
            result = parentFilter(result, parenttree)
        if aggregated:
            for key in result:
                data = getattr(p.api.action.racktivity, key["type"]).getViewData(key["guid"])["result"]["data"]
                #Add the string represnation "viewdatastr"
                for item in data:
                    item['viewdatastr'] = "%0.1f"%item["viewdatavalue"]
                key["data"] = data
    return result
