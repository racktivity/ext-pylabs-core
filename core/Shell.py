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

'''Q-Shell implementation'''

import re
import os
import sys
import new
import itertools
import string
import inspect

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import pymonkey

from IPython.Shell import IPShellEmbed
from IPython.ultraTB import FormattedTB
import IPython.genutils
from IPython.OInspect import myStringIO
import IPython.OInspect
from IPython.iplib import SyntaxTB

class SimpleInteractiveTB(FormattedTB):
    '''Simple interactive shell traceback formatter

    This is an implementation of IPython's FormattedTB only displaying
    exception message and type. It is registered as traceback callback by
    the Q-Shell implementation, when running in normal (non-debug) mode.
    '''
    def __call__(self,etype=None,evalue=None,etb=None,
                 out=None,tb_offset=None):
        ##print
        ##print '*** Error:',

        ###if isinstance(etype, basestring):
            ###print str(etype)
        ###else:
            ####Print the 'msg' attribute of the exception if available (eg for
            ####SyntaxError, we don't want to display something like
            ####    EOL while scanning single-quoted string (<ipython console>, line 1)
            ####which is the value of str(SyntaxError e)
            ####Fallback to str()
            ###print getattr(evalue, 'msg', str(evalue)), '(type %s)' % etype.__name__

        pymonkey.q.errorconditionhandler._exceptionhook(etype, evalue, etb)


class SimpleSyntaxTB(SyntaxTB, SimpleInteractiveTB):
    '''Simple interactive shell syntax error traceback formatter

    This is an extension of IPython's SyntaxTB only displaying exception
    message and type. It is registered as traceback callback by the Q-Shell
    implementation, when running in normal (non-debug) mode.
    '''
    def __call__(self, etype, value, elist):
        self.last_syntax_error = value
        SimpleInteractiveTB.__call__(self, etype, value, elist)


def qexec(self, args):
    '''Execute a given script using Q-Shell

    Sample usage:

        %qexec myscript.py argument1 argument2

    Arguments are optional.
    '''
    s = args.split(' ', 1)
    if len(s) > 1:
        script, args = s[0], s[1]
    else:
        script, args = s[0], ''

    if not pymonkey.q.system.fs.exists(script):
        print 'Script \'%s\' not found' % script
        return

    cmd = '%s %s %s' % (
            pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir, 'qshell'),
            script,
            args)

    pymonkey.q.system.process.executeWithoutPipe(cmd)


def _complete(self, text, state, line_buffer=None):
    '''Duc-taped implementation of IPython.Completer.complete

    This method is duc-taped into Q-Shell when it is running in normal mode.
    It filters out several patterns from tab-completion output, including

     * Attributes starting with one or more underscores ('_')
     * Attributes starting with 'pm_'
    '''
    #Trash cache if state equals 0
    if state == 0 and text in self._completions:
        del self._completions[text]
    #Get cache
    completions = self._completions.get(text, None)

    #If no cache, get all completions and cache
    if not completions:
        getnext = True
        completions = list()
        for i in itertools.takewhile(lambda a: getnext, itertools.count()):
            r = self._complete_ori(text, i, line_buffer)
            if not r:
                getnext = False
            else:
                completions.append(r)

        # Remove completions starting with _ or pm_, but only if the existing text is empty, or ends with a .
        # This way d.pm_foo won't complete, but d.a_pm_foo will
        non_underscore_completions = itertools.ifilter(lambda s: not '._' in s, completions)
        no_initial_underscore = itertools.ifilter(lambda s: not s.startswith('_'), non_underscore_completions)
        non_pm__completions = itertools.ifilter(lambda s: not '.pm_' in s, no_initial_underscore)
        #More filters go here, update next assignment accordingly
        completion_iterator = non_pm__completions

        self._completions[text] = completions = list(completion_iterator)

    #Provide completion #state, or None
    if state >= len(completions):
        del self._completions[text]
        return None

    return completions[state]


def _magic_pinfo(self, parameter_s='', namespaces=None):
    """Override the Magic function that returns the doc when typing '?'"""
    if parameter_s.endswith("("):
        parameter_s = parameter_s[:-1]
    if parameter_s.endswith("(?"):
        parameter_s = "%s?" % parameter_s[:-2]

    return self._magic_pinfo_ori(parameter_s, namespaces)

def _ofind(self, oname, namespaces=None):
    """Find an object in the available namespaces.

    self._ofind(oname) -> dict with keys: found,obj,ospace,ismagic

    Has special code to detect magic functions.

    This is a Q-Shell specific implementation which calls the standard IPython
    version, but falls back to an exec call in the user namespace to find the
    required object if it can't be found by the standard implementation. This
    fixes STDL-1400, and should have no side-effects.
    """
    info = self._ofind_ori(oname, namespaces)

    if info['found']:
        return info

    oname = oname.strip()

    ns = self.user_ns.copy()
    code = '_qshell_obj = %s' % oname
    try:
        exec code in ns
    except Exception:
        return info

    obj = ns['_qshell_obj']

    return {'found': 1, 'obj': obj, 'namespace': 'Interactive',
            'ismagic': 0, 'isalias': 0, 'parent': None}


def _attr_matches(self, text):
    """Compute matches when text contains a dot.

    Assuming the text is of the form NAME.NAME....[NAME], and is
    evaluatable in self.namespace or self.global_namespace, it will be
    evaluated and its attributes (as revealed by dir()) are used as
    possible completions.  (For class instances, class members are are
    also considered.)

    WARNING: this can still invoke arbitrary C code, if an object
    with a __getattr__ hook is evaluated.

    This version is duct-taped into our QShell IPython instance. It is equal
    to the IPython 0.8.2 completer.py:Completer.attr_matches, except the end
    which adds a '(' to all callable attributes.
    """
    import re
    import xmlrpclib
    try:
        from IPython.genutils import dir2
    except ImportError:
        dir2 = dir

    # Another option, seems to work great. Catches things like ''.<tab>
    m = re.match(r"(\S+(\.\w+)*)\.(\w*)$", text)

    if not m:
        return []
    
    expr, attr = m.group(1, 3)
    try:
        obj = eval(expr, self.namespace)
    except:
        try:
            obj = eval(expr, self.global_namespace)
        except:
            return []

    words = dir2(obj)

    # Build match list to return
    n = len(attr)
    
    #MOD
    from pymonkey.extensions.PMExtensionsGroup import PMExtensionsGroup
    words2 = list()
    for word in words:
        classobj = obj if inspect.isclass(obj) else getattr(obj, '__class__', None)
        classattr = getattr(classobj, word, None)

        if classattr and type(classattr) == property:
            words2.append(word)
        elif isinstance(obj, PMExtensionsGroup):
            # We don't want a getattr() on PMExtensionGroups, since this call
            # would load the extension modules, which breaks our lazy loading
            # and makes everything just plain slow. Just append the 'word'
            # without any '(' since extensions are no callables anyway.
            #
            # This fixes DAL-2627
            words2.append(word)
        else:
            try:
                iattr = getattr(obj, word)
            except Exception, e:
                words2.append(word)
            else:
                #Filter out enumeration stuff
                #If MyEnu is an enumeration, MyEnu.FOO.FOO should not be vissible
                #nor should MyEnu.FOO.registerItem
                #We want to filter out XMLRPC clients (getattr on them is not a good idea)
                if isinstance(iattr, xmlrpclib.Server):
                    word = None
                elif getattr(iattr, '_pm_enumeration_hidden', False):
                    if hasattr(obj, '_pm_enumeration_items') and inspect.isclass(obj):
                        word = word
                    elif not hasattr(obj, '_pm_enumeration_items') and not hasattr(obj, '_pm_enumeration_hidden'):
                        #Item is attribute on 'something else'
                        word = word
                    else:
                        word = None
                if word:
                    words2.append("%s%s" % (word, "(" if (inspect.isfunction(iattr) or inspect.ismethod(iattr)) else ""))
    words = words2
    #/MOD
    return ["%s.%s" % (expr, w) for w in words if w[:n] == attr ]


def _clean_glob(self, text):
    try:
        return self._clean_glob_ori(text)
    except:
        return list()


def _format_docstring(ds):
    '''Reformats a docstring from epydoc syntax to something we want to show
    the end-user'''
    if not ds:
        return ds

    #Split the original docstring in lines
    splitted = ds.splitlines()

    # Parse docstring
    #doclines are all lines above any @* definition
    doclines = list()
    #Take all lines before the first line starting with an @
    #itertools.takewhile is something like:
    # def takewhile(predicate, iterable):
    #     for i in iterable:
    #         if predicate(i):
    #             yield i
    #         else:
    #             break
    for line in itertools.takewhile(lambda l: not l.startswith('@'), splitted):
        import re
        line =  re.sub('[A-Z]{(?P<content>\w+)}', lambda mo: mo.groupdict()['content'], line)
        doclines.append(line)

    #tags stores all tags (@* stuff) we want to store/display to the end-user
    tags = {
        'param': list(),
        'returns': None,
        'return': None,
    }

    #Manipulator functions, re-arrange a tagged documentation line into the
    #format we want to display
    #Single tags: @returns: foo
    #Double tags: @param foo: Bar
    single_tags = {
        'returns': lambda v: 'Returns: %s' % v,
        'return': lambda v: 'Returns: %s' % v,
    }
    double_tags = {
        'param': lambda k, v: '- %s: %s' % (k, v),
    }

    #Loop through all tagged lines
    for line in (l for l in splitted if l.startswith('@')):
        import re
        line =  re.sub('[A-Z]{(?P<content>\w+)}', lambda mo: mo.groupdict()['content'], line)
        #Figure out the tag
        tag = line.split(' ', 1)[0].lstrip('@').rstrip(':')
        #Check whether we need this tag
        if tag in tags:
            #Split it and rearrange
            if tag in single_tags:
                value = line.split(' ', 1)[1]
                value = single_tags[tag](value)

            if tag in double_tags:
                try:
                    _, param, value = line.split(' ', 2)
                except ValueError:
                    value = '- %s (invalid docstring format)' % \
                            line.split()[1].strip(' :')
                else:
                    param = param.rstrip(':')
                    value = double_tags[tag](param, value)

            #Append or set
            if isinstance(tags[tag], list):
                tags[tag].append(value)
            else:
                tags[tag] = value

    # Rebuild docs
    out = StringIO()
    out.write('\n'.join(doclines))

    if tags['param']:
        out.write('\n\n')
        out.write('Parameters:\n\n')
        for param in tags['param']:
            out.write('%s\n' % param)

    if tags['returns'] or tags['return']:
        out.write('\n')
        out.write('%s\n' % (tags['returns'] or tags['return']))

    ds = out.getvalue().strip()

    return ds

def _getdoc(obj):
    from IPython.OInspect import getdoc

    ret = None

    try:
        inspect_frame = sys._getframe(2)
        if not inspect_frame.f_code.co_name == '_inspect':
            #Not the code path we expect
            raise Exception

        locals_ = inspect_frame.f_locals

        #From here on we could raise KeyErrors like hell, but we just ignore
        #them: if they occur, we can't get any info anyway
        obj_info = locals_['info']
        path = locals_['path']
        parent_object = obj_info['parent']

        properties_metadata = parent_object.pm_property_metadata
        property_metadata = properties_metadata[path[-1]]

        if property_metadata['doc']:
            ret = property_metadata['doc']
        elif property_metadata['doc'] is None:
            ret = property_metadata['self'].__class__.__doc__

    except Exception:
        pass

    if not ret:
        ret = getdoc(obj)

    return ret

def _pinfo(self,obj,oname='',formatter=None,info=None,detail_level=0):
    """Show detailed information about an object.

    Optional arguments:

    - oname: name of the variable pointing to the object.

    - formatter: special formatter for docstrings (see pdoc)

    - info: a structure with some information fields which may have been
    precomputed already.

    - detail_level: if set to 1, more information is given.

    This is a copy of the method found in IPython 0.8.1 and is duc-taped into
    IPython.OInspect.
    """
    #Some extra imports
    import types
    import linecache
    from IPython.OInspect import myStringIO, getsource
    from IPython.genutils import indent, page
    #We need access to private stuff, blergh
    self.__head = getattr(self, '_%s__head' % self.__class__.__name__)
    self.__getdef = getattr(self, '_%s__getdef' % self.__class__.__name__)


    obj_type = type(obj)

    header = self.__head
    if info is None:
        ismagic = 0
        isalias = 0
        ospace = ''
    else:
        ismagic = info.ismagic
        isalias = info.isalias
        ospace = info.namespace
    # Get docstring, special-casing aliases:
    if isalias:
        ds = "Alias to the system command:\n  %s" % obj[1]
    else:
        ds = _getdoc(obj)
        if ds is None:
            ds = '<no docstring>'
    if formatter is not None:
        ds = formatter(ds)

    ds = _format_docstring(ds)

    # store output in a list which gets joined with \n at the end.
    out = myStringIO()

    string_max = 200 # max size of strings to show (snipped if longer)
    shalf = int((string_max -5)/2)

    # reconstruct the function definition and print it:
    defln = self.__getdef(obj,oname)
    if defln:
        out.write(header('Definition:\t')+self.format(defln))

    # Docstrings only in detail 0 mode, since source contains them (we
    # avoid repetitions).  If source fails, we add them back, see below.
    if ds and detail_level == 0:
        out.writeln(header('Documentation:\n') + indent(ds))

    # Filename where object was defined
    binary_file = False
    try:
        fname = inspect.getabsfile(obj)
        if fname.endswith('<string>'):
            fname = 'Dynamically generated function. No source code available.'
        if (fname.endswith('.so') or fname.endswith('.dll') or
            not os.path.isfile(fname)):
            binary_file = True
    except:
        # if anything goes wrong, we don't want to show source, so it's as
        # if the file was binary
        binary_file = True

    # Original source code for any callable
    if detail_level:
        # Flush the source cache because inspect can return out-of-date source
        linecache.checkcache()
        source_success = False
        try:
            source = self.format(getsource(obj,binary_file))
            if source:
                out.write(header('Source:\n')+source.rstrip())
                source_success = True
        except Exception, msg:
            pass

        if ds and not source_success:
            out.writeln(header('Documentation [source file open failed]:\n')
                        + indent(ds))

    # Constructor docstring for classes
    if obj_type is types.ClassType:
        # reconstruct the function definition and print it:
        try:
            obj_init =  obj.__init__
        except AttributeError:
            init_def = init_ds = None
        else:
            init_def = self.__getdef(obj_init,oname)
            init_ds  = _getdoc(obj_init)

        if init_def or init_ds:
            out.writeln(header('\nConstructor information:'))
            if init_def:
                out.write(header('Definition:\t')+ self.format(init_def))
            if init_ds:
                out.writeln(header('Documentation:\n') + indent(init_ds))

    # Finally send to printer/pager
    output = out.getvalue()
    if output:
        page(output)
    # end pinfo


def page(strng,start=0,screen_lines=0,pager_cmd = None):
    '''Non-paging page implementation to provide a non-paging Q-Shell
    '''
    #This comes from IPython.genutils.page
    str_lines = strng.split(os.linesep)[start:]
    str_toprint = os.linesep.join(str_lines)

    print >>IPython.genutils.Term.cout, str_toprint


class Shell:
    '''PyMonkey-customized IPython shell class'''

    def __init__(self, debug=False, ns=None):
        '''Initialize a new shell instance

        Debugging can be enabled by using the corresponding argument. A custom
        initial namespace can be provided as well.

        @param debug: Run in debug mode
        @type debug: bool
        @param ns: Initial namespace used in the shell
        @type ns: dict
        '''
        self.debug = debug
        self.ns = ns
        
    def __call__(self, *args, **kwargs):
        '''Create a new shell, which can run by calling the instance.

        Differences between a standard IPython shell and this one include:
            - Less output when using ?? or ?
            - Very limited exception reporting (no backtrace)
            - Custom tab-completion, removing protected or private members

        If debug is True, most customizations will be disabled.

        *args and **kwargs are those you'd pass to
        C{IPython.Shell.IPShellEmbed.__call__}.
        '''
        pymonkey.q.vars.setVar('DEBUG', self.debug)
        pymonkey.q.qshellconfig.interactive=True

        argv = ['ipy_user_conf.py']
        banner = '''
Welcome to qshell

?          -> Introduction to features.
help()     -> python help system.
object?    -> Details about \'object\'.
object??   -> Extended details about \'object\'.

Type q. and press [TAB] to list qshell library
Type i. and press [TAB] to list interactive commands

'''
        exit_msg = None

        ns = self.ns

        rc_override = {
            "readline_remove_delims": "-/~'\"[]",
            "autocall": 0,
        }

        if hasattr(sys, 'frozen') and sys.platform.startswith('win'):
            # This is a py2exed version of PyMonkey and we are on Windows
            from user import home
            home = home.decode(sys.getfilesystemencoding())
            rc_override['ipythondir'] = os.path.join(home, "_ipython")

        #TODO should set rc_override['readline_omit__names'] on 0 for debug and on 2 for non-debug
        #     and should then remove code customization

        #Call parent constructor. Do we really need to preserve excepthook?
        _oldexcepthook = sys.excepthook
        myshell = IPShellEmbed(argv, banner=banner, exit_msg=exit_msg, user_ns=ns, rc_override=rc_override)
        sys.excepthook = _oldexcepthook

        if not self.debug:
            #Set customized exception display
            myshell.IP.InteractiveTB = SimpleInteractiveTB()
            myshell.IP.SyntaxTB = SimpleSyntaxTB()

            #Replace completer
            myshell.IP.Completer._complete_ori = myshell.IP.Completer.complete
            completefunc = new.instancemethod(_complete, myshell.IP.Completer, myshell.IP.Completer.__class__)
            myshell.IP.Completer.complete = completefunc
            myshell.IP.Completer._completions = dict()
            attr_matchesfunc = new.instancemethod(_attr_matches, myshell.IP.Completer, myshell.IP.Completer.__class__)
            myshell.IP.Completer.attr_matches = attr_matchesfunc

            myshell.IP.Completer._clean_glob_ori = myshell.IP.Completer._clean_glob
            clean_globfunc = new.instancemethod(_clean_glob, myshell.IP.Completer, myshell.IP.Completer.__class__)
            if myshell.IP.Completer.clean_glob.__name__ == '_clean_glob':
                myshell.IP.Completer.clean_glob = clean_globfunc
            myshell.IP.Completer._clean_glob = clean_globfunc

            # replace the magic_pinfo that shows the doc when typing ?
            # this we do so it has the same behaviour when using (?
            myshell.IP._ofind_ori = myshell.IP._ofind
            myshell.IP._ofind = new.instancemethod(_ofind, myshell.IP, myshell.IP.__class__)
            myshell.IP._magic_pinfo_ori = myshell.IP.magic_pinfo
            myshell.IP.magic_pinfo = new.instancemethod(_magic_pinfo, myshell.IP, myshell.IP.__class__)

            # Replace IPython.OInspect.pinfo with our custom page method which
            # mangles docstring output
            myshell.IP.inspector.pinfo = new.instancemethod(_pinfo, myshell.IP.inspector, myshell.IP.inspector.__class__)

            myshell.IP.api.expose_magic('qexec', qexec)

            #Overwrite paging pager with non-paging pager
            IPython.genutils.page = page

        if 'WINGDB_ACTIVE' in os.environ:
            return
        #set var for _ipython so we can know we are in an interactive
        #environment without having to run the same code again.
        pymonkey.q.vars.setVar("_ipython", "True")
        try:
            __IP
        except NameError:
            pass
        else:
            return
        
        _stdout = None
        _stderr = None
        # first check whether the sys._stdout_ori exists.  The check returns None if it does not exists, and fails the equals.
        # if the check exists getattr will return  the sys._stdout_ori and check for equality
        if hasattr(sys, '_stdout_ori') and not sys._stdout_ori == sys.stdout:
            _stdout = sys.stdout
            sys.stdout = sys._stdout_ori
            
        if hasattr(sys, '_stderr_ori') and not sys._stderr_ori == sys.stderr:
            _stderr = sys.stderr
            sys.stderr = sys._stderr_ori

        # Store TTY settings and reset TTY later on if necessary (ie unclean exit)
        try:
            import termios
            import atexit
            fd = sys.stdin.fileno()

            __IPYTHON__.tty_settings = termios.tcgetattr(fd)

        except:
            #We can ignore any exceptions (eg termios not available on Windows)
            pass

        kwargs['local_ns'] = kwargs.pop('local_ns', dict())
        kwargs['global_ns'] = kwargs.pop('global_ns', ns)

        myshell(*args, **kwargs)
        
        if _stdout:
            sys.stdout = _stdout
        if _stderr: 
            sys.stderr = _stderr


class _ipshellShell(Shell):
    def __call__(self):
        #Get stack frame of the frame on top of this one
        frame = sys._getframe(1)

        #Get his locals and globals
        locals_ = frame.f_locals.copy()
        globals_ = frame.f_globals.copy()

        Shell.__call__(self, local_ns=locals_, global_ns=globals_)

ipshell = _ipshellShell(debug=False)
'''Basic Q-Shell instance'''
qshell = ipshell
'''Embedable Q-Shell instance'''

ipshellDebug = Shell(debug=True)
'''Q-Shell instance with debug mode enabled'''