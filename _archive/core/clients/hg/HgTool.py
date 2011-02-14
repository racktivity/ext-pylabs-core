# -*- coding: utf-8 -*-
# <License type="Sun BSD" version="2.0">
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
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE193
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

'''Utility methods to work with hg repositories'''

import os.path
from urlparse import urlparse, urlunparse
import re
import pymonkey
from pymonkey import q
from pymonkey.baseclasses.CommandWrapper import CommandWrapper

class HgConnection:
  def __init__(self, url, username, password, destination=''):
    self.url = url
    self.username = username
    self.password = password
    self.destination = destination
    self._tool = HgTool()

  def clone(self, noUpdate=False):
    self.destination= self._tool.clone(self.url, self.username, self.password, self.destination, noUpdate)

  def export(self, destination, source=None, branch=''):
    self._tool.hg_export(self.destination, destination, '' , branch, source)

class HgTool(CommandWrapper):

  def is_hg_repository(self,path):
    '''Check whether a given folder is a hg repository

    @param path: Path of potential repository
    @type path: string

    @returns: Whether the given path contains a hg repository
    @rtype: bool
    '''
    pymonkey.q.logger.log('Checking whether %s is a hg repository' % path)
    isdir = pymonkey.q.system.fs.exists
    join = pymonkey.q.system.fs.joinPaths
    if ( not isdir(join(path, 'store')) or \
         not isdir(join(path, 'requires'))):
      return False
    pymonkey.q.logger.log('Returning False Value ')
    # This is most likely a hg repository
    return True


  def clone(self, repository_path, username, password, destination='', noUpdate=False):
    '''Clone a hg repository to QBASE/var/hg

    The project name should determine the project which is cloned, since the
    clone is created in QBASE/var/hg/NAME.

    If this is an initial clone, the remote repository will be cloned into
    QBASE/var/hg/NAME, using the provided remote_name as remote (overriding the
    default 'origin').

    If the target folder already exists, we check whether a remote with the
    provided name already exists. If not, it is added. If a remote already
    exists, the remote path is compared against the provided value. If it is not
    equal to the provided path, a RuntimeError is raised.

    Finally the remote is fetched.

    No actual checkout is ever performed.
    For SSH cloning the public private key has to be set in prior for non-interactive execution.


    Example usage:
     clone('ssh://user1@hostname//home/user1/pylabs-core3',None,None,'/home/user/TEMP/SSHPYLABS2')
     clone('https://user@bitbucket.org/user/hg-recipe/',None,None,'/home/user/TEMP/EXIST/HGRECIPE')

    @param repository_path: Path to the remote repository
    @type repository_path: string
    @param username: Username of the HTTP/HTTPS repository
    @type username : string
    @param password: User Password
    @type password : string
    @param destination : Optional , local clone destination (default QBASE/var/hg/)
    @type destination : string
    '''
    pymonkey.q.logger.log('Cloning (%s)' % \
                          (repository_path), 5)

    hg_base = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                             'var', 'hg')
    if not q.system.fs.exists(hg_base):
      q.system.fs.createDir(hg_base)

    defaultDest = repository_path.rstrip('/').split('/')[-1]
    destination = destination or defaultDest

    target = pymonkey.q.system.fs.joinPaths(hg_base, destination)

    # Target should be a folder, if it exists
    if pymonkey.q.system.fs.exists(target) and \
       not pymonkey.q.system.fs.isDir(target):
      raise RuntimeError(
        'Path %s exists, but is not a directory' % project_name)

    # If it exists, it's a folder which should have a .hg subfolder
    if pymonkey.q.system.fs.exists(target) and \
       not pymonkey.q.clients.hg.is_hg_repository(pymonkey.q.system.fs.joinPaths(target, '.hg')):
      raise RuntimeError('Folder %s exists, but is not a hg folder' % target)

    # Check whether the remote already exists
    if pymonkey.q.system.fs.exists(
      pymonkey.q.system.fs.joinPaths(target, '.hg', 'hgrc'
                                     )):
      command = 'hg paths'
      ret, stdout, stderr = pymonkey.q.system.process.run(
        command, stopOnError=False, cwd=target)

      if ret:
        raise RuntimeError('Failed to retrieve info for paths %s in %s. Error %s' % \
                           (remote_name, target, stderr))

      match = False
      pattern = re.compile('default\s*=\s*')

      for line in stdout.splitlines():
        pymonkey.q.logger.log('The Line %s' % line)
        split = pattern.split(line)
        if len(split) > 1:
          parsed = urlparse(split[-1])
          url = '%s://%s%s'%(parsed[0], parsed.hostname, parsed.path)
          pymonkey.q.logger.log('Found remote URI %s' % url, 6)
          if url == repository_path:
            match = True
            break

      if not match:
        raise RuntimeError('Remote destination already exists, '
                           'but with another path')

    else:
      parsed = list(urlparse(repository_path))
      if username and password:
        parsed[1] = parsed[1].replace('@','')
        parsed[1] = '%s:%s@%s'%(username, password, parsed[1].replace(username,''))
      else:
        parsed[1] = '%s' % parsed[1]

      repository_path = urlunparse(tuple(parsed))
      command = 'hg clone %s "%s" %s' %('-U' if noUpdate else '',repository_path, '' if defaultDest == destination else destination)
      if destination == defaultDest:
        base = hg_base
      else:
        if os.path.isabs(pymonkey.q.system.fs.getDirName(destination)) and not pymonkey.q.system.fs.isDir(destination):
          base = destination
        elif not pymonkey.q.system.fs.isDir(target):
          base = target
        else:
          raise RuntimeError('Destination Directory is not Empty . Error %s'%stderr)
        q.system.fs.createDir(base)
      ret, _, stderr= pymonkey.q.system.process.run(command, stopOnError=False,
                                                    cwd=base)
      if ret:
        raise RuntimeError('Unable to add clone remote. Error %s'%stderr)

    return destination

  def _checkout(self,repository_path,project_name, head, source):
    '''Checkout an object from a repository to a given path

    This function checks out an object of a head in a given repository in a
    target location.

    The target location should not exist.

    @param repository_path: Path to source repository
    @type repository_path: string
    @project_name: Name of the the Project Under Repository
    @type project_name: string
    @param head: hg refspec of the version to check out
    @type head: string
    @param source: Path to source object in the repository
    @type source: string
    '''
    pymonkey.q.logger.log('Checking out object %s of head %s '
                          'in repository %s ' % \
                          (source, head, repository_path ))

    if not pymonkey.q.clients.hg.is_hg_repository(repository_path):
      raise RuntimeError('Repository path %s does not look like '
                         'a hg repository' % repository_path)

    orig_head, orig_source = head, source

    # Check whether we can parse the given head
    #source = source.lstrip('/')
    #head = '%s:%s' % (head, source)

    headpath = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                              'var', 'hg',
                                              project_name,head)
    pymonkey.q.logger.log('headpath,head PATH: %s %s' % (headpath,head))


    if not pymonkey.q.system.fs.exists(headpath):
      raise RuntimeError('The branch does not exist')

#    if pymonkey.q.system.fs.isDir(pymonkey.q.system.fs.joinPaths(headpath,source)):
#       raise RuntimeError('The Source is a Directory Tree')

    command = 'hg locate %s' % source
#
    ret, stdout, stderr = pymonkey.q.system.process.run(command, stopOnError=False,cwd=headpath)
#    if ret:
#    print ('Unable to find the source file %s in the local repo, checking the cloned repository for changes ')
    command = 'hg pull -u'
    ret, stdout, stderr= pymonkey.q.system.process.run(command, stopOnError=False,
                                                       cwd=headpath)
    if ret:
      raise RuntimeError('Unable to pull the changes from default repo. %s'%stderr)
    else:
      command = 'hg locate %s' % source
      ret,stdout,stderr = pymonkey.q.system.process.run(command, stopOnError=False,cwd=headpath)
      if ret:
        print ('Source Not found')
      else:
        print ('Source is Pulled')


      pymonkey.q.logger.log('CHANGE RET : %s stdout: %s ' % (ret, stdout))
    #else:
    #   print ('The source exists in the local repo')


  def checkout(self,project_name, remote_name, branch, source):
    '''Checkout an file of a repository to a given path

    This function checks out an source file in a repository

    If C{remote_name} is empty or C{None}, a local branch is assumed.

    @param project_name: Name of the project to use (see C{clone})
    @type project_name: string
    @param remote_name: Name of the remote
    @type remote_name: string
    @param branch : Tree under which the source is residing.
    @type branch : string
    @param source: checkout source object in the repository
    @type source: string
    '''
    head = branch if not remote_name else '%s/%s' % (remote_name, branch)

    pymonkey.q.logger.log('Checking out object %s of %s branch %s ' % \
                          (source, project_name, head
                           ), 5)

    repository_path = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                                     'var', 'hg',
                                                     project_name, '.hg')
    pymonkey.q.clients.hg._checkout(repository_path, project_name, head, source)

  def checkin(self,project_name,remote_name,addsource,sourcepath,commit_message):
    ''' Checkin a file or commited source to the bitbucket repository

    This function checks in a source file to a repository

    @param project_name:  Name of the Project to Use to look for the Remote Name
    @type project_name: string
    @param remote_name:  Source or Tree to use under the project_name.
    @type remote_name: string
    @param add_source_path: source or tree to be added to local repository for commit
    @type add_source_path: string
    @param commit_message: Message to be included with the commit message
    @type commit_message: string
    '''

    repository_path=pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,'var','hg',
                                                   project_name,remote_name)
    hg_repo = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,'var','hg',
                                             project_name,remote_name,'.hg')

    if not pymonkey.q.clients.hg.is_hg_repository(hg_repo):
      raise RuntimeError('Repository path %s does not look like '
                         'a hg repository' % repository_path)

    if not pymonkey.q.system.fs.exists(pymonkey.q.system.fs.joinPaths(repository_path,sourcepath)):
      raise RuntimeError('The add source does not exist in the repository')

    source = pymonkey.q.system.fs.joinPaths(repository_path,sourcepath)

    command = 'hg add %s' % addsource

    ret,stdout,_ = pymonkey.q.system.process.run(command, stopOnError=False,cwd=source)

    if ret:
      raise RuntimeError('Adding Source Failed')
    else:
      command = 'hg commit -m "%s" %s' % (commit_message,addsource)
      ret,stdout,_ = pymonkey.q.system.process.run(command, stopOnError=False,cwd=source)
      if ret:
        raise RuntimeError('Committing %s failed' % addsource)

    command='hg push'

    ret,stdout,_ = pymonkey.q.system.process.run(command, stopOnError=False,cwd=source)

    if ret:
      raise RuntimeError('Unable to Push the changes to repository')

  def hg_export(self,project_name, destination, remote_name, branch_name, source=None):

    ''' Svn Export like mercurial top level directory copy

    This function exports a source repository to a destination

    @param project_name:  Name of the Project to Use to look for the Remote Name
    @type project_name: string
    @param remote_name:  Source or Tree to use under the project_name.
    @type remote_name: string
    @param destination: Export Destination
    @type add_source_path: string
    @param branch_name: Branch name under remote_name
    @type branch_name : string
    @param source : The source that is to be exported
    @type source: string
    '''

    repository_path=pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,'var','hg',
                                                   project_name, remote_name)
    hg_repo = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,'var','hg',
                                             project_name,remote_name,'.hg')

    if not pymonkey.q.clients.hg.is_hg_repository(hg_repo):
      raise RuntimeError('Repository path %s does not look like '
                         'a hg repository' % repository_path)

    destination=pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,destination)
    archive = q.system.fs.joinPaths(q.dirs.tmpDir, 'hg', 'archive')
    if q.system.fs.exists(archive): q.system.fs.removeDirTree(archive)

    ###pull lastest changes first
    command = 'hg pull'
    ret,stdout,stderror = pymonkey.q.system.process.run(command, stopOnError=False,cwd=repository_path)

    if ret:
      raise RuntimeError('Failed to update, %s'%stderror)

    command='hg archive -r %s %s' % ('default' if not branch_name else branch_name, archive)

    ret,stdout,stderror = pymonkey.q.system.process.run(command, stopOnError=False,cwd=repository_path)
    if ret:
      raise RuntimeError('Unable to export, %s'%stderror)

    if source and not q.system.fs.exists(q.system.fs.joinPaths(archive, source)):
      raise IOError('%s does not exist '%q.system.fs.joinPaths(archive, source))

    source=q.system.fs.joinPaths(archive,source) or archive

    q.system.fs.copyDirTree(source, destination)
    archivalFile = q.system.fs.joinPaths(destination, '.hg_archival.txt')
    if q.system.fs.exists(archivalFile):
      q.system.fs.removeFile(archivalFile)

    q.system.fs.removeDirTree(archive)

