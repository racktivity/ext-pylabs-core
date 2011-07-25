#!/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import glob
import os
import xml.dom.minidom
from racktivity.common.GUIDLoader import Value,Functions

def readModule(filename):
    doc = xml.dom.minidom.parse(filename)
    root = doc.firstChild
    rootname = root.getAttribute("name")
    for module in root.childNodes:
        if module.nodeType != module.ELEMENT_NODE: continue
        if module.nodeName != "memory": continue
        modulename = module.getAttribute("name")
        for item in module.childNodes:
            if item.nodeType != module.ELEMENT_NODE: continue
            if item.nodeName != "item": continue
            guid = item.getAttribute("GUID")
            count = item.getAttribute("count")
            yield (modulename, rootname, count, guid)
            
def readGuidTable(filename):
    #Make connection to the database
    def getValue(valTag):
        ans = Value()
        ans.type = valTag.attributes["type"].value
        for v in valTag.childNodes:
            if v.nodeType == v.TEXT_NODE: continue
            if v.firstChild:
                if v.nodeName in ('size','scale','max','min','length'):
                    setattr(ans, v.nodeName, int(v.firstChild.nodeValue))
                else:
                    setattr(ans, v.nodeName, v.firstChild.nodeValue)
            else:
                setattr(ans, v.nodeName, "")
        return ans

    doc = xml.dom.minidom.parse(filename)
    guidtable = doc.firstChild
    
    for item in guidtable.childNodes:
        if item.nodeType == item.TEXT_NODE: continue
        funcs = Functions()
        for field in item.childNodes:
            if field.nodeType == item.TEXT_NODE: continue
            if (field.nodeName == u"value"):
                funcs.valDef = getValue(field)
            elif field.firstChild == None:
                setattr(funcs, field.nodeName, None)
            else:
                if field.nodeName in ('read','write','guid'):
                    setattr(funcs, field.nodeName, int(field.firstChild.nodeValue))
                else:
                    setattr(funcs, field.nodeName, field.firstChild.nodeValue)
        
        if funcs.guid != None:
            yield (funcs.guid, funcs.name, funcs.valDef.save() , funcs.read, funcs.write)
        else:
            raise Exception("Invalid device, no guid")

basicdb = '''
CREATE TABLE modules (id INTEGER PRIMARY KEY, name TEXT, type TEXT, count NUMERIC, guid NUMERIC);
CREATE TABLE tbl_guid (guid INTEGER PRIMARY KEY, name TEXT, valDef BLOB, read NUMERIC, write NUMERIC);
CREATE UNIQUE INDEX idx_guid_name ON tbl_guid(name ASC);
CREATE INDEX idx_modules_name ON modules(name ASC);
CREATE INDEX idx_modules_types ON modules(type ASC);
'''

#("insert into modules (name, type, count, guid) values (?, ?, ?, ?)",

def generateDB(folder, dbconnection):
    guidtable = os.path.join(folder, "GUIDtable.xml")
    modules = glob.glob("%s/*.xml" % folder)
    if guidtable in modules:
        modules.remove(guidtable)
    else:
        raise RuntimeError("Could not find %s" % guidtable)
    con = dbconnection
    cursor = con.cursor()
    cursor.executescript(basicdb)
    cursor.execute("DELETE FROM tbl_guid")
    cursor.execute("DELETE FROM modules")
    
    cursor.executemany("INSERT INTO tbl_guid values(?,?,?,?,?)", readGuidTable(guidtable))
    for module in modules:
        cursor.executemany("insert into modules (name, type, count, guid) values (?, ?, ?, ?)", readModule(module))
    con.commit()
