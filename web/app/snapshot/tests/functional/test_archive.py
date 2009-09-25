from snapshot.tests import *

class TestArchiveController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='archive', action='index'))
        # Test response...
