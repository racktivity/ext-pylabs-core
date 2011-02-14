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

'''Basic PyMonkey initialization functions used by pymonkey.InitBase*'''

import sys
import os
import sitecustomize
from pymonkey.enumerators import AppStatusType



def setup_dirs(q, base):
    '''Set up q.dirs

    This function calculates all paths for q.dirs.* and initializes q.dirs.

    @param q: PyMonkey instance to initialize
    @type q: L{PYMonkey}
    @param base: PyMonkey sandbox base folder
    @type base: string
    '''
    q.dirs.baseDir = base
    q.dirs.appDir = os.path.join(q.dirs.baseDir, 'apps', '')
    q.dirs.varDir = os.path.join(q.dirs.baseDir, 'var', '')
    q.dirs.cfgDir = os.path.join(q.dirs.baseDir, 'cfg', '')
    q.dirs.tmpDir = os.path.join(q.dirs.varDir, 'tmp', '')
    q.dirs.pidDir = os.path.join(q.dirs.varDir, 'pid', '')
    q.dirs.logDir = os.path.join(q.dirs.varDir, 'log', '')
    q.dirs.cmdbDir = os.path.join(q.dirs.varDir, 'cmdb', '')
    q.dirs.init()

def initialize_redirections(redirect_output, hide_output):
    '''Set up stdout/stderr redirection if required

    @param redirect_output: Whether redirection is requested
    @type redirect_output: bool
    @param hide_output: Don't send output to the real stdin/stdout
    @type hide_output: bool
    '''
    if not redirect_output:
        return

    from pymonkey.logging.RedirectStreams import redirectStreams
    redirectStreams(hideoutput=hide_output)


_initstack = None
def initialize_q(redirect_output, hide_output=False, verbose=False):
    '''Initialize the C{q} object

    @param setup_logging: Set up logging to a LogServer (see
                          L{initialize_logging})
    @type setup_logging: bool
    @param redirect_output: Set up output redirection (see
                            L{initialize_redirections})
    @type redirect_output: bool
    @param hide_output: Hide output (see L{initialize_redirections})
    @type hide_output: bool
    '''
    global _initstack

    import traceback

    from pymonkey import q

    if q._init_called or q._init_final_called:
        if _initstack:
            print 'Illegal attempt to re-initialize PyMonkey detected.'
            print
            print 'Previous initialization occurred at:'
            print
            print _initstack
            print
        raise RuntimeError('Do not reimport pymonkey.InitBase*')

    stack = traceback.extract_stack()
    # Skip the last 3 frames:
    # initialize_q (this function)
    # initialize
    # (import of InitBase*)
    _initstack = ''.join(traceback.format_list(stack[:-3]))
    del stack

    initialize_redirections(redirect_output, hide_output)

    q.init()

    baseDir = sitecustomize.find_qbase_path()
    if not baseDir:
        print "PyMonkey not supported on this platform"
        sys.exit(1)
    setup_dirs(q, baseDir)

    q.init_final()

    return q

def initialize_i():
    '''Initialize the C{i} object'''
    from pymonkey import q, i

    if q.vars.getVar("INTERACTIVE"):
        # TODO: No longer use qshellconfig
        q.qshellconfig.interactive = True

    i._initExtensions()

    return i


def initialize(redirect_output, hide_output=False, verbose=False):
    '''Initialize the C{q} and C{i} objects

    @see: L{initialize_q}
    @see: L{initialize_i}

    @returns: The initialized C{q} and C{i} objects
    @rtype: tuple<PYMonkey, Interactive>
    '''
    q = initialize_q(redirect_output, hide_output=False, verbose=verbose)
    i = initialize_i()

    return q, i
