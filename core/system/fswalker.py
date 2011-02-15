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
import os.path
import pylabs
#from pylabs.Shell import *


class FSWalker:
    
    @staticmethod
    def _checkDepth(path,depths,root=""):
        if depths==[]:
            return True
        #path=q.system.fs.pathclean(path)
        path=pylabs.q.system.fs.pathRemoveDirPart(path,root)
        for depth in depths:
            dname=os.path.dirname(path)
            split=dname.split(os.sep)
            split = [ item for item in split if item<>""]
            #print split
            if depth==len(split):
                return True
        else:
            return False
    
    @staticmethod    
    def _checkContent(path,contentRegexIncludes=[], contentRegexExcludes=[]):
        if contentRegexIncludes==[] and contentRegexExcludes==[]:
            return True
        content=pylabs.q.system.fs.fileGetContents(path)
        if pylabs.q.codetools.regex.matchMultiple(patterns=contentRegexIncludes,text=content) and not pylabs.q.codetools.regex.matchMultiple(patterns=contentRegexExcludes,text=content):
            return True
        return False

    @staticmethod       
    def _findhelper(arg,path):
        arg.append(path)
    
    @staticmethod    
    def find(root, recursive=True, includeFolders=False, pathRegexIncludes=[".*"],pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[],depths=[]):
        listfiles=[]
        FSWalker.walk(root, FSWalker._findhelper, listfiles, recursive, includeFolders, pathRegexIncludes,pathRegexExcludes, contentRegexIncludes, contentRegexExcludes,depths)
        return listfiles
    
    @staticmethod
    def walk(root, callback, arg="", recursive=True, includeFolders=False, pathRegexIncludes=[".*"],pathRegexExcludes=[], contentRegexIncludes=[], contentRegexExcludes=[],depths=[],followlinks=True):
        '''Walk through filesystem and execute a method per file

        Walk through all files and folders starting at C{root}, recursive by
        default, calling a given callback with a provided argument and file
        path for every file we could find.

        If C{includeFolders} is True, the callback will be called for every
        folder we found as well.

        Examples
        ========
        >>> def my_print(arg, path):
        ...     print arg, path
        ...
        >>> FSWalker.walk('/foo', my_print, 'test:')
        test: /foo/file1
        test: /foo/file2
        test: /foo/file3
        test: /foo/bar/file4

        >>> def dirlister(arg, path):
        ...     print 'Found', path
        ...     arg.append(path)
        ...
        >>> paths = list()
        >>> FSWalker.walk('/foo', dirlister, paths, recursive=False, includeFolders=True)
        /foo/file1
        /foo/file2
        /foo/file3
        /foo/bar
        >>> print paths
        ['/foo/file1', '/foo/file2', '/foo/file3', '/foo/bar']

        @param root: Filesystem root to crawl (string)
        @param callback: Callable to call for every file found, func(arg, path) (callable)
        @param arg: First argument to pass to callback
        @param recursive: Walk recursive or not (bool)
        @param includeFolders: Whether to call C{callable} for folders as well (bool)
        @param pathRegexIncludes / Excludes  match paths to array of regex expressions (array(strings))
        @param contentRegexIncludes / Excludes match content of files to array of regex expressions (array(strings))
        @param depths array of depth values e.g. only return depth 0 & 1 (would mean first dir depth and then 1 more deep) (array(int)) 
        
        '''
        if not pylabs.q.system.fs.isDir(root):
            raise ValueError('Root path for walk should be a folder')
        if recursive==False:
            depths=[0]
        #We want to work with full paths, even if a non-absolute path is provided
        root = os.path.abspath(root)

        #if recursive:
        for dirpath, dirnames, filenames in os.walk(root,followlinks=followlinks):
            #Folders first
            if includeFolders:
                for dirname in dirnames:
                    path = os.path.join(dirpath, dirname)
                    if pylabs.q.codetools.regex.matchMultiple(patterns=pathRegexIncludes,text=path) and not pylabs.q.codetools.regex.matchMultiple(patterns=pathRegexExcludes,text=path):
                        if FSWalker._checkDepth(path,depths,root) and FSWalker._checkContent(path,contentRegexIncludes, contentRegexExcludes):
                            callback(arg, path)
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if pylabs.q.codetools.regex.matchMultiple(patterns=pathRegexIncludes,text=path) and not pylabs.q.codetools.regex.matchMultiple(patterns=pathRegexExcludes,text=path):
                    if FSWalker._checkDepth(path,depths,root) and FSWalker._checkContent(path,contentRegexIncludes, contentRegexExcludes):
                        callback(arg, path)
                
        #else: # not recursive
            #ipshell()
            ##Find all file/folder names of items under root
            #items = [os.path.join(root, name) for name in os.listdir(root)]
            #if includeFolders:
                ##Loop through all items in 'items', filter out folders, loop over these
                #for dirpath in (item for item in items if pylabs.q.system.fs.isDir(item)):
                    #callback(arg, dirpath)

            ##Loop through all items in 'items', filter out files, loop over these
            #for filepath in (item for item in items if pylabs.q.system.fs.isFile(item)):
                #callback(arg, filepath)