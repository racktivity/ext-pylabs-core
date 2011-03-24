import os
import unittest

from pylabs.InitBase import q

class PathTagsTest(unittest.TestCase):
    def setUp(self):
        folder = os.path.join(os.path.dirname(__file__), 'tasklets')
        self.engine = q.taskletengine.get(folder)

    def test_execute_no_tags(self):
        testresults = []
        params = {"testresults": testresults}
        self.engine.execute(params)
        self.assertEqual(testresults, ["job", "customer"])

    def test_execute_with_tags(self):
        testresults = []
        params = {"testresults": testresults}
        tags = ("tag1", "tag2")
        self.engine.execute(params, tags=tags)
        self.assertEqual(testresults, ["job", "customer"])

    def test_execute_first_no_tags(self):
        testresults = []
        params = {"testresults": testresults}
        self.engine.executeFirst(params)
        self.assertEqual(testresults, ["job"])

    def test_execute_first_with_tags(self):
        testresults = []
        params = {"testresults": testresults}
        tags = ("tag1", "tag2")
        self.engine.executeFirst(params, tags=tags)
        self.assertEqual(testresults, ["job"])

    def test_execute_priority_2(self):
        testresults = []
        params = {"testresults": testresults}
        self.engine.executeFirst(params, priority=2)
        self.assertEqual(testresults, ["customer"])

    def test_execute_priority_3(self):
        testresults = []
        params = {"testresults": testresults}
        self.engine.executeFirst(params, priority=3)
        self.assertEqual(testresults, ["job"])
