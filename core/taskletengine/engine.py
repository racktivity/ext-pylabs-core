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

'''pylabs *tasklet* engine implementation'''

import os
import os.path
import operator
import time
import stat
import weakref
import functools
try:
    import threading
except ImportError:
    threading = None

import pylabs

MATCH_FAILED = object()

from tasklet import Tasklet

Tasklet.MATCH_FAILED = MATCH_FAILED

#@feedback (kds) everywhere we use priority 1 as highest, here it is the reverse

def _ignore(t, c, *a, **k):
    '''Evaluate c(*a, **k), ignoring exceptions of type t'''

    try:
        c(*a, **k)
    except t:
        pass


class locked(object): #pylint: disable-msg=R0903
    '''
    Decorator for methods which should be locked using an instance-wide lock
    '''
    def __init__(self, name):
        self.name = name

    def __call__(self_, fun): #pylint: disable-msg=E0213
        @functools.wraps(fun)
        def wrapped(self, *args, **kwargs): #pylint: disable-msg=C0111
            lock = getattr(self, self_.name, None)
            if lock:
                lock.acquire()
            try:
                return fun(self, *args, **kwargs)
            finally:
                if lock:
                    lock.release()

        return wrapped


class TaskletEngine(object):
    '''Tasklet engine as bound on q.tasklets'''

    STOP = object()
    CONTINUE = object()

    def __init__(self, taskletsDir, clusterFun=None):
        """
        @param taskletsDir is directory in which tasklets live

        @param clusterFun: Callable which yields all keys for which a given
            tasklet should be added to the index
        @type clusterFun: callable
        """
        self._tasklets = None
        self._path_load_times = dict()  #@question (kds) why is this?

        if threading:                   #@question (kds) is threading support like this really needed?
            self._lock = threading.RLock()

        self._cluster_fun = clusterFun
        self._clusters = dict()

        self.addFromPath(taskletsDir)

    # Needs to be locked since it uses self._tasklets as a sentinel
    @locked('_lock')
    def _init(self):
        '''Initialize the engine'''
        if self._tasklets is not None:
            return

    @locked('_lock')
    def addFromPath(self, path):
        '''Load all tasklets from a given folder, recursively

        @param path: Tasklet container folder
        @type path: string
        '''
        pylabs.q.logger.log('Loading tasklets in %s' % path, 6)

        #Make sure we got a dict
        self._tasklets = self._tasklets or dict()

        #Generate a list of .py and .qshell files in the given path
        #Use a generator instead of list concatenation for readability
        def listTaskletFiles():
            '''List all .py and .qshell files in *path*'''
            for script in pylabs.q.system.fs.listFilesInDir(path, True,
                                                     filter='*.py'):
                yield script

            for script in pylabs.q.system.fs.listFilesInDir(path, True,
                    filter='*.qshell'):
                yield script

        self._path_load_times[path] = time.time()

        for taskletfile in listTaskletFiles():
            self._registerTasklet(taskletfile, path)

    def _registerTasklet(self, path, tasklet_root):
        '''Register one tasklet in a given file in the system'''
        pylabs.q.logger.log('Loading tasklet %s' % path)
        if path in self._tasklets:
            raise RuntimeError('Tasklet in %s already registered' % path)

        name = self._getPathInfo(path)

        tasklet = self._tasklets[path] = Tasklet(name, path, tasklet_root)

        if self._cluster_fun:
            for key in self._cluster_fun(tasklet):
                if key not in self._clusters:
                    self._clusters[key] = weakref.WeakSet()

                self._clusters[key].add(tasklet)

    @staticmethod
    def _getPathInfo(path):
        '''Get tasklet name from the tasklet module path'''
        filename = pylabs.q.system.fs.getBaseName(path)

        return filename


    def _check_reload(self, path):
        '''Check whether the tasklets in *path* should be reloaded'''
        if path not in self._path_load_times:
            pylabs.q.logger.log('Unknown folder %s, force reloading' % path,
                                  6)
            return True

        tasklets_updated = pylabs.q.system.fs.joinPaths(path, 'tasklets_updated')

        #Don't reload if file is not touched
        if not pylabs.q.system.fs.exists(tasklets_updated):
            pylabs.q.logger.log('Not reloading tasklets in %s, ' \
                                  '%s doesn\'t exist' % \
                                  (path, tasklets_updated), 6)
            return False

        stat_info = os.stat(tasklets_updated)

        # This needs to be >= since mtime is seconds-based on some systems, so
        # reloading too quickly can cause a > to fail
        return stat_info[stat.ST_MTIME] >= self._path_load_times[path]

    @locked('_lock')
    def _reload(self, force=False):
        '''Reload all tasklets, if required'''
        # This needs to be locked down in case this engine is shared between
        # threads.
        # Locking this function is a pretty coarse-grained approach but it
        # should do.
        paths = self._path_load_times.keys()

        for path in paths:
            if force or self._check_reload(path):
                for taskletpath in self._tasklets.copy():
                    if taskletpath.startswith(path):
                        tasklet = self._tasklets.pop(taskletpath)

                        remove = lambda s: _ignore(KeyError, s.remove, tasklet)
                        map(remove, self._clusters.itervalues())

                self.addFromPath(path)

    #pylint: disable-msg=R0912,R0913
    def find(self, author="*", name="*", tags=None, priority=-1, path="*",
        clusters=None):
        '''Find all matching tasklets

        Tasklets can be filtered on author, name, tags and priority. If author
        or name is '*', any value is accepted.

        If tags is not None, it should be an iterable (array). A matching tasklet
        should have all provided tags.

        If priority is larger than 0, the tasklet matches if its priority is
        the same.

        @param author: Author filter
        @type author: string
        @param name: Name filter
        @type name: string
        @param tags: Tags filter
        @type tags: iterable
        @param priority: Priority filter
        @type priority: number
        @param path: Path filter
        @type path: string
        @param clusters: Keys of clusters to use as tasklet source
        @type clusters: iterable

        @returns: All matching tasklets, sorted on priority
        @rtype: tuple<Tasklet>
        '''
        self._init()

        self._reload()

        pylabs.q.logger.log(
            'Searching for tasklets, author=%s, name=%s, '
            'tags=%s, priority=%d' % (author, name, tags, priority), 7)

        #Some filter generators
        #These filters are chained together to create one filter pipeline to
        #find all matching tasklets given the search criteria.
        #Using a generator pipeline simplifies adding new filter criteria and
        #makes the code somewhat more readable (not to mention more efficient)
        def authorFilter(tasklets):
            '''Filter tasklets based on author'''
            for tasklet in tasklets:
                if author == '*' or  tasklet.author == author:
                    yield tasklet

        def nameFilter(tasklets):
            '''Filter tasklets based on name'''
            for tasklet in tasklets:
                if name == '*' or tasklet.name == name:
                    yield tasklet

        def tagFilter(tasklets):
            '''Filter tasklets based on tags'''
            if tags is not None:
                _tags = set(tags or tuple())
            for tasklet in tasklets:
                if tags is None or _tags in (set(t) for t in tasklet.tags):
                    yield tasklet

        def priorityFilter(tasklets):
            '''Filter tasklets based on priority'''
            for tasklet in tasklets:
                if priority < 0 or tasklet.priority == priority:
                    yield tasklet

        def pathFilter(tasklets):
            '''Filter tasklets based on path'''
            for tasklet in tasklets:
                if path == '*' or tasklet.path.startswith(path):
                    yield tasklet

        #Master filter
        def filterTasklets(tasklets):
            '''Chain all tasklet filters'''
            author_matches = authorFilter(tasklets)
            name_matches = nameFilter(author_matches)
            tag_matches = tagFilter(name_matches)
            priority_matches = priorityFilter(tag_matches)
            path_matches = pathFilter(priority_matches)

            for tasklet in path_matches:
                yield tasklet

        if not clusters:
            #Apply all filters on all known tasklets
            tasklets = self._tasklets.itervalues()
        else:
            #Apply all filters on specific clusters of tasklets
            if isinstance(clusters, basestring):
                clusters = (clusters, )

            def iter_clusters():
                seen = weakref.WeakSet()

                for cluster in clusters:
                    if cluster in self._clusters:
                        set_ = self._clusters[cluster]

                        for tasklet in set_:
                            # Weakref protection, and duplicate protection
                            if tasklet and tasklet not in seen:
                                seen.add(tasklet)

                                yield tasklet

            tasklets = iter_clusters()

        filtered_tasklets = filterTasklets(tasklets)

        #Sort on priority
        sorted_tasklets = sorted(filtered_tasklets,
            key=operator.attrgetter('priority'), reverse=True)

        return tuple(sorted_tasklets)

    #pylint: disable-msg=R0913
    def findFirst(self, author="*" , name="*", tags=None, priority=-1,
        path='*', clusters=None):
        '''Find the first matching tasklet (highest priority)

        @see: TaskletsEngine.find

        @return: Matching tasklet, or None
        @rtype: Tasklet
        '''
        matches = self.find(author, name, tags, priority, path=path,
            clusters=clusters)

        if not matches:
            return None

        if len(matches) == 1:
            return matches[0]

        if matches[0].priority == matches[1].priority:
            raise RuntimeError('Priorities of tasklets %s and %s conflict' % (
                matches[0].path, matches[1].path))

        return matches[0]

    #pylint: disable-msg=R0913
    def execute(self, params, author="*", name="*", tags=None, priority=-1,
        path='*', clusters=None, wrapper=None):
        '''Execute all matching tasklets

        @param params: Params to pass to the tasklet function,is a dict
        @type params: dict
        @param wrapper: Optional function decorator which can be used to wrap
                        tasklet main() functions
        @type wrapper: callable

        @see: TaskletsEngine.find
        '''
        realized = set()

        matches = self.find(author, name, tags, priority, path=path,
            clusters=clusters)
        pylabs.q.logger.log('Executing previously found tasklets', 6)

        for tasklet in matches:
            if tasklet.realizes and tasklet.realizes in realized:
                pylabs.q.logger.log('%s already realized, ' \
                                      'skipping tasklet %s' % \
                                      (tasklet.realizes, tasklet.name), 6)
                continue

            ret = tasklet.executeIfMatches(params, tags or tuple(), wrapper)

            if ret is not MATCH_FAILED and tasklet.realizes:
                pylabs.q.logger.log('%s realized by %s' % (tasklet.realizes,
                                                    tasklet.name), 6)
                realized.add(tasklet.realizes)

            if ret is self.STOP:
                break

    #pylint: disable-msg=R0913
    def executeFirst(self, params, author="*", name="*", tags=None,
        priority=-1, path='*', clusters=None, wrapper=None):
        '''Execute the first matching tasklet

        @return: Tasklet function return value
        @rtype: object
        @param wrapper: Optional function decorator which can be used to wrap
                        tasklet main() functions
        @type wrapper: callable

        @see: TaskletsEngine.execute
        '''
        wrapper = wrapper or (lambda func: func)
        assert callable(wrapper)

        tasklet = self.findFirst(author, name, tags, priority, path=path,
            clusters=clusters)

        if tasklet:
            return tasklet.execute(params, tags, wrapper)
        else:
            return None
