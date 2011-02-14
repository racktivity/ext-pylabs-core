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

from pymonkey import q

class QPackageConfigure:

    def configure(self, name, version, domain):
        """
        Executes the configure tasklet
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        """
        from pymonkey.qpackages.client.QPackageTasklets import QPackageTasklets
        tasklets = QPackageTasklets()
        packageObject = q.qpackages.qpackagePackagesDir.qpackageFind(name=name, version=version, domain=domain, qualityLevels=q.qpackages.getDefaultQualityLevel())
        if not packageObject:raise ValueError('Failed to find qpackage (%s,%s,%s) on qualityLevel %s'%(name, version,domain, q.qpackages.getDefaultQualityLevel()))
        packageObject = packageObject[0]
        tasklets.configure(packageObject)

    def signalForConfiguration(self, name, version, domain):
        """
        Add the qpackage to the list of qpackages that needs configuration
        @param name: Name of the QPackage
        @param version: version of the QPackage
        @param domain: domain of the QPackage
        """
        iniFile = self.getIniFile()
        iniFileDict = iniFile.getFileAsDict()
        if {'name':name, 'version':version, 'domain':domain} in iniFileDict.values():
            # Duplicate entry. We will not register again
            return
        sectioncount = len(iniFile.getSections())
        iniFile.addSection(str(sectioncount))
        iniFile.addParam(str(sectioncount), 'name', name)
        iniFile.addParam(str(sectioncount), 'version', version)
        iniFile.addParam(str(sectioncount), 'domain', domain)
        iniFile.write()

    def reconfigure(self, qpackageName = None):
        """
        Reconfigures all qpackages marked for configurations. Loops through all the qpackages added
        to the ini file, sorts them, then call the configure tasklet for each qpackage. Then cleans up
        when all tasklets have been called.

        If errors occur in non-interactive mode, the user gets a number of choices on how to continue.
        If errors occur in interactive mode, this method will throw the exception thrown by the tasklet.
        """
        iniFile = self.getIniFile()
        sections = sorted(iniFile.getSections(), key=lambda x: int(x))

        if sections:
            q.action.start('QPackage reconfiguration')

        if qpackageName:
            skipCleanup = True
        else:
            skipCleanup = False

        for section in sections:
            name = iniFile.getValue(section, 'name')
            version = iniFile.getValue(section, 'version')
            domain = iniFile.getValue(section, 'domain')

            if qpackageName:
                if name != qpackageName:
                    continue
            q.action.start('Reconfiguring %s %s (%s)' % (name, version, domain))
            try:
                self.configure(name, version, domain)
                iniFile.removeSection(section)
                iniFile.write()
            except:
                if q.qshellconfig.interactive:
                    ()
                    err = q.eventhandler.getCurrentExceptionString()
                    q.console.echo("An error occurred during the reconfiguration")
                    q.console.echo(err)
                    LEAVE_QSHELL = 'Leave Q-Shell'
                    RECONFIGURE_OTHERS = 'Skip configuration of this package. Configure other packages'
                    GO_TO_QSHELL = 'Go to Q-Shell directly (package configurations will happen later)'
                    choice = q.console.askChoice([LEAVE_QSHELL, RECONFIGURE_OTHERS, GO_TO_QSHELL], 'How do you want to continue')
                    if choice == LEAVE_QSHELL:
                        # Leave Q-Shell immediately. Don't do sys.exit(.) because we want to leave
                        # as quickly as possible, without running the risk to have additional errors
                        # in pymonkey exithandlers (registered in atexit module).
                        # We need this behaviour because we are already in an error scenario.
                        import os
                        os._exit(1)
                    elif choice == RECONFIGURE_OTHERS:
                        continue
                    elif choice == GO_TO_QSHELL:
                        skipCleanup = True
                        break
                    else:
                        raise RuntimeError("Unsupported choice in QPackages reconfiguration")
                else:
                    # We are in non-interactive mode and get an exception from a configure tasklet.
                    # Raise the exception that was thrown by that tasklet.
                    # In principle, all kinds of exceptions are possible.
                    raise

            q.action.stop()

        if sections:
            q.action.stop()

        if not skipCleanup:
            self.cleanUp()

    def cleanUp(self):
        """
        Removes reconfigure directory after tasklets has been called
        """
        q.system.fs.removeDirTree(self._getReconfigureDir())

    def getIniFile(self):
        """
        Returns iniFile object
        """
        iniFileLocation = q.system.fs.joinPaths(self._getReconfigureDir(), 'reconfigure.cfg')
        if q.system.fs.isFile(iniFileLocation):
            iniFile = q.tools.inifile.open(iniFileLocation)
        else:
            iniFile = q.tools.inifile.new(iniFileLocation)

        return iniFile

    def _getReconfigureDir(self):
        """
        Returns the path to reconfigure dir (creates it if does not exist)
        """
        reconfigureDir = q.system.fs.joinPaths(q.dirs.varDir, 'reconfigure', 'qpackages')
        if not q.system.fs.exists(reconfigureDir):
            q.system.fs.createDir(reconfigureDir)
        return reconfigureDir
