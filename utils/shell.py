#!/usr/bin/env python
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

from optparse import OptionParser
import sys
import os

def main():

    #parse commandline options
    parser = OptionParser()
    parser.add_option('-d', '--debug', dest='debug', action='store_true',
            default=False, help='run in debug mode')
    parser.add_option('-n', '--no-default-initialization', dest='init',
            action='store_true', default=False, help='do not perform default PyMonkey initialization using pymonkey.InitBase.initialize')
    parser.add_option("-f", "--file", dest="filename", help="Execute file")
    parser.add_option("-c", "--command", dest="command", help="Execute command")
    parser.add_option("-l", "--logserver", dest="logserver", action='store_true', help="Start logserver")
    (options, args) = parser.parse_args()
    #execute python file or first argu
    if options.filename or (len(args) > 0 and args[0].endswith('.py')):
        if options.filename:
            filename = options.filename
        else:
            filename = args[0]
            args = args[1:]
        sys.argv = sys.argv[0:1] + args
        sys.path.append(os.path.dirname(os.path.abspath(filename)))
        exec_ns = {
                '__name__': '__main__',
                'QSHELL_ENV': True,
                }
        execfile(filename, exec_ns)
        sys.exit(0)
    #start logserver
    elif options.logserver:
        try:
            #@todo for backwards compatibility
            from pymonkey.log.LogServer import startlogserver
            startlogserver()
            sys.exit(0)
        except:
            import pymonkey
            from pymonkey.InitBaseCore import q, i
            print "Pylabs logconsole started:"
            q.logger.console.start()
            sys.exit(0)


    #execute command
    elif options.command:
        import pymonkey
        from pymonkey.InitBaseCore import q, i
        exec options.command
        sys.exit(0)
    ns = {}
    if not options.init:
        import pymonkey
        pymonkey.q.vars.setVar('DEBUG', options.debug)
        from pymonkey.InitBaseCore import q, i

        ns['q'] = q
        ns['i'] = i
        q.application.appname = 'qshell'
        q.qshellconfig.interactive=True
        q.application.start()

        # First time Q-Shell is loaded: automatically update list of Q-Packages available on the server.
        mainCfg = q.config.getInifile("main")
        FIRSTRUN_PARAMNAME = "qshell_firstrun"

        #if not mainCfg.checkParam("main", FIRSTRUN_PARAMNAME) or mainCfg.getBooleanValue("main", FIRSTRUN_PARAMNAME) == True:
        #    q.action.start('Retrieving QPackage information from '
        #                   'package servers')
        #    i.qpackages.updateQPackageList()
        #    q.action.stop()
        #    mainCfg.setParam("main", FIRSTRUN_PARAMNAME, False)
        #    mainCfg.write()

        q.qshellconfig.interactive=True
        if options.debug:
            q.logger.consoleloglevel=8
        else:
            q.logger.consoleloglevel=2

        # Run QPackage configure tasklets if any registered
        #from pymonkey.qpackages.client.QPackageConfigure import QPackageConfigure
        #qpackageconfigure = QPackageConfigure()
        #qpackageconfigure.reconfigure()


        # Run QPackage4 configure tasklets if needed
        q.qp._runPendingReconfigeFiles()
        sys.path.append(q.system.fs.joinPaths(q.dirs.baseDir, 'var', 'tests'))
        from pymonkey.Shell import Shell
        # Cannot use ipshell or ipshellDebug because I want to twiddle with the namespace as well...
        Shell(debug=options.debug, ns=ns)()

        q.application.stop()

    else:
        # Give pure ipython Shell
        from IPython.Shell import IPShellEmbed
        IPShellEmbed(argv=[], banner="Welcome to IPython", exit_msg="Bye")()

if __name__ == '__main__':
    main()
