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

import os
import sys
import imp
import traceback
import zipimport
import threading

import pylabs

class BasePMExtension(object):
    """
    can be just the info of an extension or a fully loaded object (instance from class which represents extension)
    these BasePMEXtension objects are being put on q.[one or more PMExtensionsGroupObjects].[PMExtensionObject]
    """
    def __init__(self, extensionPath, moduleName, className, pmExtensionName):
        """
        Constructor for BasePMExtension instances.

        @param extensionPath: path of package of extension
        @type extensionPath: string
        @param moduleName: is filename (withoug .py) which includes class
        @type moduleName: string
        @param className: name of the root class of this extension
        @type className: string
        @param pmExtensionName: name used to expose class under q.[one or more extensionsgroup's].[pmExtensionName]
        @type pmExtensionName: string
        """
        self._activation_lock = threading.Lock()

        if not pylabs.q.basetype.dirpath.check(extensionPath):
            raise ValueError('Invalid extension path %s, not a folder' %
                    extensionPath)
        if not pylabs.q.basetype.string.check(moduleName):
            raise ValueError('Invalid moduleName provided, not a string')
        if not pylabs.q.basetype.string.check(className):
            raise ValueError('Invalid className provided, not a string')

        self.activated = False              #is extension already loaded or not
        self.moduleInfo = None              #is python info about module, is output of find_module of http://docs.python.org/lib/module-imp.html
        self.instance = None                #is instance of BasePMExtension
        self.extensionPath = extensionPath
        self.moduleName = moduleName
        self.className = className
        self.pmExtensionName = pmExtensionName

    def activate(self):
        """
        load extension (create instance) = lazy loading
        """
        if self.activated:
            return

        self._activation_lock.acquire()
        try:
            # Might be activated now as well, so re-check
            if not self.activated:
                self._activate()
                # Set activated to true only after activation
                self.activated = True
        finally:
            self._activation_lock.release()

    def _activate(self):
        """Internal activate method, only called if not yet activated"""
        classModule = self._loadClassModule()

        self.classDefinition = getattr(classModule, self.className)

        #make instance of definition of class
        try:
            self.instance = self.classDefinition()
        except Exception, e:
            #Get exception type, exception instance and backtrace
            t, v, tb = sys.exc_info()
            self._handleCreateInstanceException(t, v, tb)

    def _handleCreateInstanceException(self, t, v, tb):
        #Send to logserver
        pylabs.q.errorconditionhandler._exceptionhook(t, v, tb)

        #Display
        print 'An error occured while creating an instance of the %s extension' % self.moduleName
        print 'Extension path: %s' % self.extensionPath
        print
        print 'Exception: %s (type %s)' % (str(v), v.__class__.__name__)
        print
        stack = traceback.extract_tb(tb)
        last_frame = stack[-1]
        last_file = last_frame[0][len(self.extensionPath):]
        last_line = last_frame[1]
        last_code = last_frame[3]
        print 'The exception occurred in %s on line %d: %s' % (last_file, last_line, last_code)
        print
        if not pylabs.q.vars.getVar('DEBUG'):
            print 'To see a full error report, check your logserver or run Q-Shell using debug mode'
            # Reset TTY
            # See above for more info
            try:
                import termios
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, __IPYTHON__.tty_settings)
            except:
                pass

            pylabs.q.application.stop()
        else:
            raise

    def _handleLoadClassModuleException(self, t, v, tb):
        #Send to logserver
        if pylabs.q.vars.getVar("_ipython"):
            pylabs.q.qshellconfig.interactive=True
        pylabs.q.errorconditionhandler._exceptionhook(t, v, tb)

        #Display
        print 'An error occured while loading the %s extension' % self.moduleName
        print 'Extension path: %s' % self.extensionPath
        print
        print 'Exception: %s (type %s)' % (str(v), v.__class__.__name__)
        print
        stack = traceback.extract_tb(tb)
        last_frame = stack[-1]
        last_file = last_frame[0][len(self.extensionPath):]
        last_line = last_frame[1]
        last_code = last_frame[3]
        print 'The exception occurred in %s on line %d: %s' % (last_file, last_line, last_code)
        print
        if not pylabs.q.vars.getVar('DEBUG'):
            print 'To see a full error report, check your logserver or run Q-Shell using debug mode'
            # Reset TTY
            # We need to reset our TTY to the settings it had before
            # launching the ipython shell, which uses readline which
            # can put our TTY in raw mode, which gets funky if we get
            # back into $(getent passwd `whoami` | cut -d: -f7)
            try:
                import termios
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, __IPYTHON__.tty_settings)
            except:
                pass

            pylabs.q.application.stop()
        else:
            raise

    def _loadClassModule(self):
        """Load the class module for this extension"""
        raise NotImplementedError

    def __str__(self):
        return "pylabs Extension %s (at %s)" % (self.pmExtensionName, self.extensionPath)

class PMExtension(BasePMExtension):
    """Extension class for 'normal' (non-zipped) extensions"""
    def _loadClassModule(self):
        """Load the class module for this extension from the .py file"""
        cleanedPath = os.path.abspath(self.extensionPath)
        sys.path.append(cleanedPath)
        self.moduleInfo = imp.find_module(self.moduleName, [self.extensionPath, ])
        extensionName = os.path.basename(self.extensionPath)
        pylabs.q.logger.log("loadmodule: extensionName:%s, moduleName:%s" % (extensionName, self.moduleName), 8)
        #load module as _pm_[extensionName]_[moduleName]
        #This could fail if the module loading errors out. We'll catch this,
        #display a message providing info about the failing extension, then
        #raise the original exception
        try:
            return imp.load_module('_pm_%s_%s' % (extensionName, self.moduleName), *self.moduleInfo)
        except Exception, e:
            #Get exception type, exception instance and backtrace
            t, v, tb = sys.exc_info()
            v = "Error Loading Extention : %s, File: %s, Error: %s" % (self.moduleName, self.moduleInfo[1], v)         

            self._handleLoadClassModuleException(t, v, tb)
        finally:
            sys.path.remove(cleanedPath)

class EggPMExtension(BasePMExtension):
    """Extension class for zipped extensions"""
    def _loadClassModule(self):
        """Load the class module for this extension from the zip file"""
        sep = "/"

        # Zipped extension path:
        zippedExtensionPath = self.extensionPath
        pylabs.q.logger.log("Zipped extension path: '%s'" % (zippedExtensionPath), 5)

        extensionImporter = zipimport.zipimporter(zippedExtensionPath)
        try:
            return extensionImporter.load_module(self.moduleName)
        except Exception, e:
            #Get exception type, exception instance and backtrace
            t, v, tb = sys.exc_info()
            self._handleLoadClassModuleException(t, v, tb)
