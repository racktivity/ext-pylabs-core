import os.path
import unittest
import itertools

try:
    import pylabs
except ImportError:
    # Fake pylabs
    import os
    import sys
    import types
    import fnmatch
    import logging

    pylabs = types.ModuleType('pylabs')

    sys.modules['pylabs'] = pylabs

    # Poor man mocking
    class Mock(object):
        def __getattr__(self, name):
            m = Mock()
            setattr(self, name, m)

            return m

        def __call__(self, *a, **k):
            pass

    q = pylabs.q = Mock()
    pylabs.i = Mock()
    pylabs.p = Mock()

    def listFilesInDir(path, recurse, filter=None):
        if not recurse:
            all_paths = (os.path.join(path, file_)
                for file_ in os.listdir(path))
            paths = (path_ for path_ in all_paths
                if os.path.isfile(path_))
        else:
            def list_():
                for root, _, files in os.walk(path):
                    for file_ in files:
                        yield os.path.join(root, file_)

            paths = list_()

        if filter:
            paths = (path_ for path_ in paths
                if fnmatch.fnmatch(path_, filter))

        return tuple(paths)

    q.system.fs.listFilesInDir = listFilesInDir

    q.logger.log = lambda msg, *_: logging.debug('[pylabs] %s', msg)


try:
    from pylabs.taskletengine import engine
except ImportError:
    try:
        from taskletengine import engine
    except ImportError:
        import engine

class TestClusters(unittest.TestCase):
    def setUp(self):
        self.tasklet_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'tasklets'))

        def _cluster(tasklet):
            basename = os.path.basename
            dirname = os.path.dirname
            split = lambda path: (dirname(path), basename(path))

            dir_, tasklet_name = split(tasklet.path)
            dir_, tag2 = split(dir_)
            _, tag1 = split(dir_)

            yield tasklet_name

            for permutation in itertools.permutations((tag1, tag2, )):
                yield permutation

            yield (tag1[::-1], tag2)
            yield tag2


        engine_ = engine.TaskletEngine(self.tasklet_path, _cluster)

        self.assertEquals(set(engine_._clusters.iterkeys()),
            set((
                ('tag1', 'tag2'),
                ('tag2', 'tag1'),
                ('1gat', 'tag2'),
                ('doubletag', 'doubletag'), 
                ('gatelbuod', 'doubletag'), 
                'tag2',
                'doubletag',
                '2_customer.py',
                '3_job.py', 
                '1_doubletag.py', 
            ),)
        )

        self._engine = engine_

    def tearDown(self):
        self._engine = None

    def _validate(self, p):
        self.assertEquals(tuple(sorted(p['testresults'])), ('customer', 'job', ))

    def test_clusters(self):
        engine_ = self._engine
        validate = self._validate

        params = {
            'testresults': [],
        }
        engine_.execute(params, clusters=(('1gat', 'tag2'), ))
        validate(params)

        params = {
            'testresults': [],
        }
        engine_.execute(params, clusters='tag2')
        validate(params)

        params = {}
        engine_.execute(params, clusters='tag3')
        self.assertEqual(params, {})

        params = {}
        engine_.execute(params, clusters=(('tag1', 'tag3'), ))
        self.assertEqual(params, {})

        params = {
            'testresults': [],
        }
        engine_.execute(params, clusters='3_job.py')
        self.assertEquals(params['testresults'], ['job'])

        params = {
            'testresults': [],
        }
        engine_.execute(params, clusters=('2_customer.py', '3_job.py'))
        validate(params)

        params = {
            'testresults': [],
        }
        engine_.execute(params, clusters=(('tag1', 'tag2'), ('tag2', 'tag1'),
            'tag2', ))
        validate(params)

        params = {}
        engine_.execute(params, name='test', clusters=(('tag1', 'tag2'), ))
        self.assertEquals(params, {})

        # 'name' filtering seems not to work (all names are None)
        #params = {}
        #engine_.execute(params, name='3_job.py', clusters=(('tag1', 'tag2'), ))
        #self.assertEquals(params['testresults'], ('job', ))

    def test_reload(self):
        '''Make sure cluster containers get cleared when necessary'''

        engine_ = self._engine
        num_clusters = len(engine_._clusters)

        engine_._cluster_fun = None
        engine_._reload(force=True)

        self.assertEquals(len(engine_._clusters), num_clusters)
        map(lambda s: self.assertEquals(len(s), 0),
            engine_._clusters.itervalues())
