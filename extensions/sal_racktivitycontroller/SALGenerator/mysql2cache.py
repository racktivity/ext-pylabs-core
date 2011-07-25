#!/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import glob
import os
import MySQLdb
from racktivity.common.GUIDLoader import Value,Functions

def readModules(rackdb):
    #Make connection to the database
    cur = rackdb.cursor()
    cur.execute("SELECT GUID, ModuleAbbr, Count FROM moduleguids")
    row = cur.fetchone()
    while row:
        guid = row[0]
        count = row[2]
        if row[1] == "P":
            rootname = "power"
        elif row[1] == "M":
            rootname = "master"
        row = cur.fetchone()
        yield (rootname.capitalize(), rootname, count, guid)
    
def readGuidTable(rackdb):
    #Make connection to the database
    cur = rackdb.cursor()
    cur.execute("SELECT guids.GUID, guids.Name, types.Name, Length, Scale, Unit, AdminRead, AdminWrite, guids.Comment \
                  FROM guids, types \
                  WHERE guids.Type = types.Type")
    row = cur.fetchone()
    while row:
        guid = row[0]
        name = row[1]
        val = Value()
        val.type = row[2]
        val.size = row[3]
        val.scale = row[4]
        val.length = val.size
        val.unit = row[5]
        read = row[6]
        write = row[7]
        try:
            comment = row[8].encode("ascii")
        except:
            comment = ""
        row = cur.fetchone()
        yield guid, name, val.save() , read, write, comment

basicdb = '''
CREATE TABLE modules (id INTEGER PRIMARY KEY, name TEXT, type TEXT, count NUMERIC, guid NUMERIC);
CREATE TABLE tbl_guid (guid INTEGER PRIMARY KEY, name TEXT, valDef BLOB, read NUMERIC, write NUMERIC, comment TEXT);
CREATE UNIQUE INDEX idx_guid_name ON tbl_guid(name ASC);
CREATE INDEX idx_modules_name ON modules(name ASC);
CREATE INDEX idx_modules_types ON modules(type ASC);
'''

#("insert into modules (name, type, count, guid) values (?, ?, ?, ?)",

def generateDB(dbconnection):
    #guidtable = os.path.join(folder, "GUIDtable.xml")
    rackdb=MySQLdb.connect(host = "172.19.8.107", user = "nikoRO", passwd = "nikoRO", db = "rack_db")
    
    #modules = glob.glob("%s/*.xml" % folder)
    #if guidtable in modules:
    #    modules.remove(guidtable)
    #else:
    #    raise RuntimeError("Could not find %s" % guidtable)
    con = dbconnection
    cursor = con.cursor()
    cursor.executescript(basicdb)
    cursor.execute("DELETE FROM tbl_guid")
    cursor.execute("DELETE FROM modules")
    
    cursor.executemany("INSERT INTO tbl_guid values(?,?,?,?,?,?)", readGuidTable(rackdb))
    cursor.executemany("INSERT into modules (name, type, count, guid) values (?, ?, ?, ?)", readModules(rackdb))
    con.commit()
    rackdb.close()
