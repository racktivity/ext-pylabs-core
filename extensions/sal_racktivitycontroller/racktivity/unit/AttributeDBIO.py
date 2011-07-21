#Establish the connection
import pg
conn = pg.connect("emulator","192.168.20.56", -1, None, "qbase", "qbase")
pg.set_decimal(float)

#if multiValue = True, I use port table for power
def getAttribute(miname,name,module,multiValue = False):
    if module == "master":
        sql = """select "%s" from mastermodule where "Name" = '%s'"""%(name, miname)
    elif module == "power":
        if multiValue:
            sql = """select "%s" from port where "PM" = '%s'  order by "Index" """%(name, miname)
        else:
            sql = """select "%s" from powermodule where "Name" = '%s'"""%(name, miname)
    try:
        #return [i[0] for i in conn.query(sql).getresult()]
        res = []
        for row in conn.query(sql).getresult():
            if isinstance(row[0], str):
                res.append(pg.unescape_bytea(row[0]))
            else:
                res.append(row[0])
        return res
    except pg.ProgrammingError:
        return None

def setAttribute(miname,name,module, value,index = 1, multiValue = False):
    if isinstance(value,str):
        value = "E'" + pg.escape_bytea(str(value)) + "'"
    
    if module == "master":
        sql = """update mastermodule set "%s" = %s where "Name" = '%s'"""%(name,value, miname)
    elif module == "power":
        if multiValue:
            sql = """update port set "%s" = %s where "PM" = '%s' and "Index" = %d """%(name, value, miname, index)
        else:
            sql = """update powermodule set "%s" = %s where "Name" = '%s'"""%(name, value, miname)
    try:
        val = conn.query(sql)
        #conn.commit()
        return val
    except Exception as e:
        msg = str(e)
        if msg.find("does not exist") <= 0:
            print "%s caused exception %s of type %s "%(sql, e, type(e))
        return -1

#setAttribute("P1","Current","power",str(3.6), 1 , True)
#print getAttribute("P1","Current","power",True)
#setAttribute("P1","PortName","power","Mina", 1 , True)
#print getAttribute("P1","PortName","power",True)
#setAttribute("M1","Password","master","roore")
#print getAttribute("M1","Password","master",False)
#setAttribute("P1","Frequency2","power",50.7)
#print getAttribute("P1","Frequency2","power",False)
