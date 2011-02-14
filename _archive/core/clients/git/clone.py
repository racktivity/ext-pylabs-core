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

'''Utility methods to work with Git repositories'''

import os.path

import pymonkey

def is_git_repository(path):
    '''Check whether a given folder is a git repository

    @param path: Path of potential repository
    @type path: string

    @returns: Whether the given path contains a Git repository
    @rtype: bool
    '''
    pymonkey.q.logger.log('Checking whether %s is a Git repository' % path)
    isdir = pymonkey.q.system.fs.isDir
    join = pymonkey.q.system.fs.joinPaths
    if not isdir(join(path, 'refs')) or \
       not isdir(join(path, 'objects')):
        return False

    # This is most likely a Git repository
    return True


def clone(project_name, remote_name, repository_path):
    '''Clone a Git repository to QBASE/var/git

    The project name should determine the project which is cloned, since the
    clone is created in QBASE/var/git/NAME.

    If this is an initial clone, the remote repository will be cloned into
    QBASE/var/git/NAME, using the provided remote_name as remote (overriding the
    default 'origin').

    If the target folder already exists, we check whether a remote with the
    provided name already exists. If not, it is added. If a remote already
    exists, the remote path is compared against the provided value. If it is not
    equal to the provided path, a RuntimeError is raised.

    Finally the remote is fetched.

    No actual checkout is ever performed.

    Example usage:

        >>> clone('pymonkey', 'mainline',
        ...       'git://staging.pymonkey.org/pymonkey/mainline.git')

    @param project_name: Repository name
    @type project_name: string
    @param remote_name: Name of the remote
    @type remote_name: string
    @param repository_path: Path to the remote repository
    @type repository_path: string
    '''
    pymonkey.q.logger.log('Cloning %s remote %s (%s)' % \
                          (project_name, remote_name, repository_path), 5)

    git_base = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                              'var', 'git')
    target = pymonkey.q.system.fs.joinPaths(git_base, project_name)

    # Target should be a folder, if it exists
    if pymonkey.q.system.fs.exists(target) and \
       not pymonkey.q.system.fs.isDir(target):
        raise RuntimeError(
            'Path %s exists, but is not a directory' % project_name)

    # If it exists, it's a folder which should have a .git subfolder
    if pymonkey.q.system.fs.exists(target) and \
        not is_git_repository(pymonkey.q.system.fs.joinPaths(target, '.git')):
            answer = pymonkey.q.gui.dialog.askYesNo('Export location %s exists. Do you want the folder to be removed before exporting?' % target)
            if answer:
                pymonkey.q.system.fs.removeDirTree(target)
                clone(project_name, remote_name, repository_path)
            else:
                raise RuntimeError('Folder %s exists, but is not a Git folder' % target)

    # If target doesn't exist
    if not pymonkey.q.system.fs.exists(target):
        pymonkey.q.logger.log(
            'Unknown project %s, creating environment' % project_name, 5)
        # Create it
        pymonkey.q.system.fs.createDir(target)
        # And make it a Git folder
        command = 'git init-db'
        ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                                  cwd=target)
        if ret:
            raise RuntimeError('Unable to initialize %s as a Git folder' % \
                               target)

    # If target exists (and it should once we reached this point), it's a
    # folder which should have a .git subfolder
    if not is_git_repository(pymonkey.q.system.fs.joinPaths(target, '.git')):
        raise RuntimeError('Folder %s exists, but is not a Git folder' % target)

    # Check whether the remote already exists
    if pymonkey.q.system.fs.exists(
        pymonkey.q.system.fs.joinPaths(target, '.git', 'refs', 'remotes',
                                       remote_name)):
        pymonkey.q.logger.log('Remote %s exists, checking URI' % remote_name, 6)

        # The remote exists, find it's path
        command = 'git remote show %s' % remote_name
        ret, stdout, _ = pymonkey.q.system.process.run(
            command, stopOnError=False, cwd=target)

        if ret:
            raise RuntimeError('Failed to retrieve info for remote %s in %s' % \
                               (remote_name, target))

        lines = stdout.splitlines()
        urls = list()
        for line in lines:
            if line.strip().startswith('URL:'):
                url = line.lstrip()[4:].lstrip()
                pymonkey.q.logger.log('Found remote URI %s' % url, 6)
                urls.append(url)

        if not urls:
            raise RuntimeError('Unable to retrieve the URL of remote %s' % \
                               remote_name)
        if len(urls) > 1:
            raise RuntimeError('Unable to parse \'git remote\' output')

        url = urls[0]

        if url != repository_path:
            raise RuntimeError('Remote %s already exists, '
                               'but with another path' % remote_name)
    else:
        # Create the remote
        pymonkey.q.logger.log('Adding remote %s as %s' % \
                              (remote_name, repository_path), 5)
        command = 'git remote add %s %s' % (remote_name, repository_path)
        ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                                  cwd=target)
        if ret:
            raise RuntimeError('Unable to add remote')

    # Perform fetch
    pymonkey.q.logger.log('Fetching remote %s' % remote_name, 5)
    command = 'git fetch %s' % remote_name
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                              cwd=target)
    if ret:
        raise RuntimeError('Unable to fetch remote')

    command = 'git fetch -t %s' % remote_name
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                              cwd=target)
    if ret:
        raise RuntimeError('Unable to fetch remote tags')

def _checkout_tree(repository_path, target_path, head, subtree='/'):
    '''Checkout a (sub)tree of a repository in a given path

    This function checks out a (sub)tree of a head in a given repository in a
    target folder.

    The target folder should not yet exist.

    @param repository_path: Path to source repository
    @type repository_path: string
    @param target_path: Path to target folder
    @type target_path: string
    @param head: Git refspec of the version to check out
    @type head: string
    @param tree: Path to subtree to check out
    @type tree: string
    '''
    pymonkey.q.logger.log('Checking out subtree %s of head %s '
                          'in repository %s into %s' % \
                          (subtree, head, repository_path, target_path))

    isdir = pymonkey.q.system.fs.isDir
    join = pymonkey.q.system.fs.joinPaths
    if not isdir(join(repository_path, 'refs')) or \
       not isdir(join(repository_path, 'objects')):
        raise RuntimeError('Repository path %s does not look like '
                           'a Git repository' % repository_path)

    # Check whether we can parse the given head
    subtree = subtree.lstrip('/')
    head = '%s:%s' % (head, subtree)

    command = 'git --git-dir=%s cat-file -e %s' % (repository_path, head)
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unknown refspec %s' % head)

    command = 'git --git-dir=%s cat-file -t %s' % (repository_path, head)
    ret, stdout, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unable to retrieve object type of %s' % head)
    if stdout.strip() != 'tree':
        raise RuntimeError('Object %s is not a tree' % head)

    if pymonkey.q.system.fs.exists(target_path):
        raise RuntimeError('Target path %s should not exist' % target_path)

    pymonkey.q.system.fs.createDir(target_path)
    command = 'git --git-dir=%s --work-tree=. read-tree -u --reset %s' % \
                  (repository_path, head)
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                              cwd=target_path)

    if ret:
        raise RuntimeError('Extracting tree failed')

def checkout_tree(project_name, target_path, remote_name, branch, subtree='/'):
    '''Checkout a (sub)tree of a repository to a given path

    This function checks out a (sub)tree of a branch in a repository to a
    target folder.

    The target folder should not yet exist.

    If C{remote_name} is empty or C{None}, a local branch is assumed.

    @param project_name: Name of the project to use (see C{clone})
    @type project_name: string
    @param target_path: Path to target folder
    @type target_path: string
    @param remote_name: Name of the remote
    @type remote_name: string
    @param branch: Name of the branch to checkout
    @type branch: string
    @param subtree: Path of the subtree to checkout
    @type subtree: string
    '''
    head = branch if not remote_name else '%s/%s' % (remote_name, branch)

    pymonkey.q.logger.log('Checking out subtree %s of %s branch %s to %s' % \
                          (subtree, project_name, head,
                           target_path), 5)

    repository_path = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                                     'var', 'git',
                                                     project_name, '.git')
    _checkout_tree(repository_path, target_path, head, subtree)


def _checkout_blob(repository_path, target_path, head, source):
    '''Checkout a blob of a repository in a given path

    This function checks out a blob of a head in a given repository in a
    target file.

    The target file should not exist.

    @param repository_path: Path to source repository
    @type repository_path: string
    @param target_path: Path to target folder
    @type target_path: string
    @param head: Git refspec of the version to check out
    @type head: string
    @param source: Path to blob to check out
    @type source: string
    '''
    pymonkey.q.logger.log('Checking out blob %s of head %s '
                          'in repository %s into %s' % \
                          (source, head, repository_path, target_path))

    if not is_git_repository(repository_path):
        raise RuntimeError('Repository path %s does not look like '
                           'a Git repository' % repository_path)

    # Check whether we can parse the given head
    source = source.lstrip('/')
    head = '%s:%s' % (head, source)

    command = 'git --git-dir=%s cat-file -e %s' % (repository_path, head)
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unknown refspec %s' % head)

    command = 'git --git-dir=%s cat-file -t %s' % (repository_path, head)
    ret, stdout, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unable to retrieve object type of %s' % head)
    if stdout.strip() != 'blob':
        raise RuntimeError('Object %s is not a blob' % head)

    if pymonkey.q.system.fs.exists(target_path):
        raise RuntimeError('Target path %s should not exist' % target_path)

    # Make sure the target folder exists
    target_folder = os.path.dirname(target_path)
    pymonkey.q.system.fs.createDir(target_folder)
    command = 'git --git-dir=%s --work-tree=. cat-file -p %s' % \
                  (repository_path, head)
    ret, stdout, _ = pymonkey.q.system.process.run(command, stopOnError=False,
                                                   cwd=target_folder)

    if ret:
        raise RuntimeError('Extracting blob failed')

    # Dump file content
    pymonkey.q.system.fs.writeFile(target_path, stdout)


def checkout_blob(project_name, target_path, remote_name, branch, blob_path):
    '''Checkout a blob of a repository to a given path

    This function checks out a blob of a branch in a repository to a
    target file.

    The target file should not exist.

    If C{remote_name} is empty or C{None}, a local branch is assumed.

    @param project_name: Name of the project to use (see C{clone})
    @type project_name: string
    @param target_path: Path to target file
    @type target_path: string
    @param remote_name: Name of the remote
    @type remote_name: string
    @param branch: Name of the branch to checkout
    @type branch: string
    @param blob_path: Path of the blob to checkout
    @type blob_path: string
    '''
    head = branch if not remote_name else '%s/%s' % (remote_name, branch)

    pymonkey.q.logger.log('Checking out blob %s of %s branch %s to %s' % \
                          (blob_path, project_name, head,
                           target_path), 5)

    repository_path = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                                     'var', 'git',
                                                     project_name, '.git')
    _checkout_blob(repository_path, target_path, head, blob_path)


def _checkout(repository_path, target_path, head, source):
    '''Checkout an object from a repository to a given path

    This function checks out an object of a head in a given repository in a
    target location.

    The target location should not exist.

    @param repository_path: Path to source repository
    @type repository_path: string
    @param target_path: Path to target folder
    @type target_path: string
    @param head: Git refspec of the version to check out
    @type head: string
    @param source: Path to source object in the repository
    @type source: string
    '''
    pymonkey.q.logger.log('Checking out object %s of head %s '
                          'in repository %s into %s' % \
                          (source, head, repository_path, target_path))

    if not is_git_repository(repository_path):
        raise RuntimeError('Repository path %s does not look like '
                           'a Git repository' % repository_path)

    orig_head, orig_source = head, source

    # Check whether we can parse the given head
    source = source.lstrip('/')
    head = '%s:%s' % (head, source)

    command = 'git --git-dir=%s cat-file -e %s' % (repository_path, head)
    ret, _, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unknown refspec %s' % head)

    command = 'git --git-dir=%s cat-file -t %s' % (repository_path, head)
    ret, stdout, _ = pymonkey.q.system.process.run(command, stopOnError=False)
    if ret:
        raise RuntimeError('Unable to retrieve object type of %s' % head)
    object_type = stdout.strip()

    if object_type == 'tree':
        _checkout_tree(repository_path, target_path, orig_head, orig_source)
    elif object_type == 'blob':
        _checkout_blob(repository_path, target_path, orig_head, orig_source)
    else:
        raise RuntimeError('Object %s is of unknown type %s' % \
                           (head, object_type))


def checkout(project_name, target_path, remote_name, branch, source):
    '''Checkout an object of a repository to a given path

    This function checks out an object in a repository to a target path, where
    the object can be a tree or a blob.

    The target path should not exist.

    If C{remote_name} is empty or C{None}, a local branch is assumed.

    @param project_name: Name of the project to use (see C{clone})
    @type project_name: string
    @param target_path: Path to destination
    @type target_path: string
    @param remote_name: Name of the remote
    @type remote_name: string
    @param branch: Name of the branch to checkout
    @type branch: string
    @param source: Path to source object in the repository
    @type source: string
    '''
    head = branch if not remote_name else '%s/%s' % (remote_name, branch)

    pymonkey.q.logger.log('Checking out object %s of %s branch %s to %s' % \
                          (source, project_name, head,
                           target_path), 5)

    repository_path = pymonkey.q.system.fs.joinPaths(pymonkey.q.dirs.baseDir,
                                                     'var', 'git',
                                                     project_name, '.git')
    _checkout(repository_path, target_path, head, source)