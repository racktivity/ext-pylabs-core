# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import pylabs 
from ConfigParser import ConfigParser
import os,sys

#@todo UGLY, validation should not happen on object (file) where you read from but on file where you populate values (kds)
#@todo why has this been re-written? (kds)

class IniFile(object):
    """
    Use with care:
    - addParam and setParam are 'auto-write'
    - addSection isn't
    - removeSection isn't
    - removeParam isn't
    """

    __configParser = None ##ConfigParser
    __inifilepath = None ##string
    __file = None ##File-like object
    __removeWhenDereferenced = False ##bool

    def __init__(self, iniFile, create=False, removeWhenDereferenced = False):
        """ Initialize IniFile. If the file already exists, read it and parse the structure.
            If the file did not yet exist. Don't do anything yet.

            @param iniFile:                The file to write to. This can be either a string representing a file-path or a file-like object
            @type iniFile:                 string or file-like object
            @param create:                 Whether or not to create a new file (Ignored if iniFile is a file-like object)
            @type create: bool
            @param removeWhenDereferenced: Whether or not to remove the file when this object is dereferenced
            @type removeWhenDereferenced:  bool
        """
        self.__configParser = ConfigParser()
        self.__removeWhenDereferenced = removeWhenDereferenced
        if isinstance(iniFile, basestring): # iniFile is a filepath
            self.__inifilepath = iniFile
            if create:
                pylabs.q.system.fs.createDir(pylabs.q.system.fs.getDirName(iniFile))
                pylabs.q.logger.log("Create config file: "+iniFile,7)
                pylabs.q.system.fs.writeFile(iniFile, '')
            if not pylabs.q.system.fs.isFile(iniFile):
                raise RuntimeError("Inifile could not be found on location %s" %  iniFile)
        else: # iniFile is a file-like object
            self.__file = iniFile

        self.__readFile()

    def __str__(self):
        """Returns string representation of the IniFile"""
        return '<IniFile> filepath: %s ' % self.__inifilepath

    __repr__ = __str__

    def __del__(self):
        if self.__inifilepath and self.__removeWhenDereferenced:
            pylabs.q.system.fs.removeFile(self.__inifilepath)

    def __readFile(self):
        fp = None
        try:
            if self.__inifilepath:
                fp = open(self.__inifilepath, "r")
            else:
                fp = self.__file
            return self.__configParser.readfp(fp)
        except Exception, err:
            if fp and not fp.closed:
                fp.close()
            raise RuntimeError("Failed to read the inifile \nERROR: %s"%(str(err)))

    def getSections(self):
        """ Return list of sections from this IniFile"""
        try:
            return self.__configParser.sections()
        except Exception, err:
            raise LookupError("Failed to get sections \nERROR: %s"%str(err))

    def getParams(self, sectionName):
        """ Return list of params in a certain section of this IniFile
        @param sectionName: Name of the section for which you wish the param"""
        if not self.checkSection(sectionName): return
        try:
            return self.__configParser.options(sectionName)
        except Exception, err:
            raise LookupError("Failed to get parameters under the specified section: %s \nERROR: %s"%(sectionName, str(err)))

    def checkSection(self, sectionName):
        """ Boolean indicating whether section exists in this IniFile
        @param sectionName: name of the section"""
        try:
            return self.__configParser.has_section(sectionName)
        except Exception, err:
            raise ValueError('Failed to check if the specified section: %s exists \nERROR: %s'%(sectionName, str(err)))

    def checkParam(self, sectionName, paramName):
        """Boolean indicating whether parameter exists under this section in the IniFile
        @param sectionName: name of the section where the param should be located
        @param paramName:   name of the parameter you wish to check"""
        try:
            return self.__configParser.has_option(sectionName, paramName)
        except Exception, e:
            raise ValueError('Failed to check if the parameter: %s under section: %s exists \nERROR: %s'%(paramName, sectionName, str(e)))

    def getValue(self, sectionName, paramName, raw=False):
        """ Get value of the parameter from this IniFile
        @param sectionName: name of the section
        @param paramName:   name of the parameter
        @param raw:         boolean specifying whether you wish the value to be returned raw
        @return: The value"""
        try:
            result=self.__configParser.get(sectionName, paramName, raw)
            pylabs.q.logger.log("Inifile: get %s:%s from %s, result:%s" % (sectionName,paramName,self.__inifilepath,result),7)
            return result
        except Exception, err:
            raise LookupError('Failed to get value of the parameter: %s under section: %s \nERROR: %s'%(paramName, sectionName, str(err)))

    def getBooleanValue(self, sectionName, paramName):
        """Get boolean value of the specified parameter
        @param sectionName: name of the section
        @param paramName:   name of the parameter"""
        try:
            result= self.__configParser.getboolean(sectionName, paramName)
            pylabs.q.logger.log("Inifile: get boolean %s:%s from %s, result:%s" % (sectionName,paramName,self.__inifilepath,result),7)
            return result

        except Exception, e:
            raise LookupError('Inifile: Failed to get boolean value of parameter:%s under section:%s \nERROR: %s'%(paramName, sectionName, e))

    def getIntValue(self, sectionName, paramName):
        """Get an integer value of the specified parameter
        @param sectionName: name of the section
        @param paramName:   name of the parameter"""
        try:
            result= self.__configParser.getint(sectionName, paramName)
            pylabs.q.logger.log("Inifile: get integer %s:%s from %s, result:%s" % (sectionName,paramName,self.__inifilepath,result),7)
            return result
        except Exception, e:
            raise LookupError('Failed to get integer value of parameter: %s under section: %s\nERROR: %s' % (paramName, sectionName, e))

    def getFloatValue(self, sectionName, paramName):
        """Get float value of the specified parameter
        @param sectionName: name of the section
        @param paramName:   name of the parameter"""
        try:
            result=self.__configParser.getfloat(sectionName, paramName)
            pylabs.q.logger.log("Inifile: get integer %s:%s from %s, result:%s" % (sectionName,paramName,self.__inifilepath,result),7)
            return result
        except Exception, e:
            raise LookupError('Failed to get float value of parameter:%s under section:%s \nERROR: %'%(paramName, sectionName, e))

    def addSection(self, sectionName):
        """ Add a new section to this Inifile. If it already existed, silently pass
        @param sectionName: name of the section"""
        try:
            if(self.checkSection(sectionName)):
                return
            pylabs.q.logger.log("Inifile: add section %s to %s" % (sectionName,self.__inifilepath))
            self.__configParser.add_section(sectionName)
            if self.checkSection(sectionName):
                return True
        except Exception, err:
            raise RuntimeError('Failed to add section with sectionName: %s \nERROR: %s'%(sectionName, str(err)))

    def addParam(self, sectionName, paramName, newvalue):
        """ Add name-value pair to section of IniFile
        @param sectionName: name of the section
        @param paramName:   name of the parameter
        @param newValue:    value you wish to assign to the parameter"""
        try:
            if str(newvalue)=="none": 
                newvalue=="*NONE*"
            self.__configParser.set(sectionName, paramName, str(newvalue))
            pylabs.q.logger.log("Inifile: set %s:%s=%s on %s" % (sectionName,paramName,str(newvalue),self.__inifilepath))
            #if self.checkParam(sectionName, paramName):
            #    return True
            self.write()
            return False
        except Exception, err:
            raise RuntimeError('Failed to add parameter with sectionName: %s, parameterName: %s, value: %s \nERROR: %s'%(sectionName, paramName, newvalue, str(err)))

    def setParam(self, sectionName, paramName, newvalue):
        """ Add name-value pair to section of IniFile
        @param sectionName: name of the section
        @param paramName:   name of the parameter
        @param newValue:    value you wish to assign to the parameter"""
        self.addParam( sectionName, paramName, newvalue)

    def removeSection(self, sectionName):
        """ Remove a section from this IniFile
        @param sectionName: name of the section"""
        if not self.checkSection(sectionName): return False
        try:
            self.__configParser.remove_section(sectionName)
            pylabs.q.logger.log("inifile: remove section %s on %s" % (sectionName,self.__inifilepath))
            if self.checkSection(sectionName):
                return False
            return True
        except Exception, err:
            raise RuntimeError('Failed to remove section %s with \nERROR: %s'%(sectionName, str(err)))

    def removeParam(self, sectionName, paramName):
        """ Remove a param from this IniFile
        @param sectionName: name of the section
        @param paramName:   name of the parameter"""
        if not self.checkParam(sectionName, paramName): return False
        try:
            self.__configParser.remove_option(sectionName, paramName)
            pylabs.q.logger.log("Inifile:remove %s:%s from %s" % (sectionName,paramName,self.__inifilepath))
            return True
        except Exception, err:
            raise RuntimeError('Failed to remove parameter: %s under section: %s \nERROR: %s'%(paramName, sectionName, str(err)))

    def write(self, filePath=None):
        """ Write the IniFile content to disk
        This completely overwrites the file
        @param filePath: location where the file will be written
        """
        closeFileHandler = True
        fp = None
        pylabs.q.logger.log("Inifile: Write configfile %s to disk" % (self.__inifilepath))
        if not filePath:
            if self.__inifilepath: # Use the inifilepath that was set in the constructor
                filePath = self.__inifilepath
            elif self.__file: # write to the file-like object that was set in the constructor
                closeFileHandler = False # We don't want to close this object
                fp = self.__file
                fp.seek(0)
                fp.truncate() # Clear the file-like object before writing to it
            else: # Nothing to write to
                raise Exception("No filepath to write to")

        try:
            if not fp:
                fp = open(filePath, 'w') # Completely overwrite the file.
            self.__configParser.write(fp)
            fp.flush()
            if closeFileHandler:
                fp.close()

        except Exception, err:
            if fp and closeFileHandler and not fp.closed:
                fp.close()
            raise RuntimeError("Failed to update the inifile at '%s'\nERROR: %s\n" % (filePath, str(err)))

    def getContent(self):
        """ Get the Inifile content to a string
        """
        #@todo pylabs primitives should be used (no fp...)
        fp = None
        if self.__file and not self.__file.closed:
            fp = self.__file
            fp.seek(0)
            fp.truncate()
        else:
            try:
                from cStringIO import StringIO
            except ImportError:
                from StringIO import StringIO
            fp = StringIO()
        self.__configParser.write(fp)
        fp.seek(0)
        return fp.read()

    def getSectionAsDict(self, section):
        retval = {}
        for key in self.getParams(section):
            retval[key] = self.getValue(section, key)
        return retval

    def getFileAsDict(self):
        retval = {}
        for section in self.getSections():
            retval[section] = self.getSectionAsDict(section)
        return retval
