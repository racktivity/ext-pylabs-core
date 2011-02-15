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

import inspect
import re
from operator import attrgetter

from pylabs.baseclasses import BaseType
from pylabs.inifile import IniFile
import pylabs

"""
Note: does not support defaults (yet)
"""

class AutoCreateIniFile(IniFile):
    def __init__(self, path, auto_create=False):
        self._pmd_path = path
        if auto_create and not pylabs.q.system.fs.isFile(path):
            create=True
        else:
            create=False
        IniFile.__init__(self, path, create=create)

    def remove(self):
        pylabs.q.system.fs.removeFile(self._pmd_path)

class ConfigSection(BaseType):
    def __init__(self, config, name):
        BaseType.__init__(self)
        self._section_name = name
        self._config = config
        if not self._config.checkSection(self._section_name):
            self._config.addSection(self._section_name)
            self._config.write()

        for attrName, config in self.pm_property_metadata.iteritems():
            self._setProperty(attrName, config['self'], config['default'])
            self._config.setParam(self._section_name, attrName, getattr(self, attrName))

    def pm_remove(self):
        self._config.removeSection(self._section_name)
        self._config.removeSection(self._getParamsSectionName())
        self._config.write()

    def _setProperty(self, attrName, attr, default):
        if self._config.checkParam(self._section_name, attrName):
            str_val = self._config.getValue(self._section_name, attrName)
            val = attr.fromString(str_val)
        else:
            val = default # TODO if not BaseType.emptyDefault(default) else None
        privateName = self._getPrivateName(attrName)
        setattr(self, privateName, val)
        p = property(
            fget=attrgetter(privateName),
            fset=self._attrSetter(attrName, attr),
        )
        setattr(self.__class__, attrName, p)

    def _getPrivateName(self, name):
        return "_%s" % name

    def _attrSetter(self, name, basetype):
        def setter(o, val):
            if basetype.check(val):
                setattr(o, self._getPrivateName(name), val)
                str_val = basetype.toString(val)
                o._setConfigParam(name, str_val)
            else:
                raise ValueError("Invalid value for this parameter")
        return setter

    def _setConfigParam(self, name, val):
        self._config.setParam(self._section_name, name, val)

    def __str__(self):
        config_basename = pylabs.q.system.fs.getBaseName(self._config._pmd_path)
        return "Config Section '%s' of %s" % (self._section_name, config_basename)

    def __repr__(self):
        return str(self)

class Config(object):
    def __init__(self, filename):
        self._filename = filename
        self._setConfig()
        for section_name, section_class in self._genSectionClasses(self):
            section_instance = section_class(self._config, section_name)
            setattr(self, section_name, section_instance)

    def pm_addSection(self, name, klass):
        if hasattr(self, name):
            raise ValueError("Instance already has section '%s'" % name)
        instance = klass(self._config, name)
        setattr(self, name, instance)

    def pm_removeSection(self, name):
        """
        Add a section to the config

        @param name: Name of the section to remove
        @type name: string
        """
        section = getattr(self, name)
        section.pm_remove()
        delattr(self, name)

    def _genSectionClasses(self, o):
        for attrName, attr in self._genAttrs(o):
            if inspect.isclass(attr) and issubclass(attr, ConfigSection):
                yield attrName, attr

    def _genAttrs(self, o):
        for attrName in self._genAttrNames(self):
            attr = getattr(self, attrName)
            yield attrName, attr

    def _genAttrNames(self, o):
        for attrName in dir(o):
            yield attrName

    def _setConfig(self):
        self._config = AutoCreateIniFile(self._filename, auto_create=True)

    def remove(self):
        self._config.remove()

    def __str__(self):
        config_basename = pylabs.q.system.fs.getBaseName(self._filename)
        return "Config %s" % (config_basename)

    def __repr__(self):
        return str(self)