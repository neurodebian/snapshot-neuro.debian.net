from snapshot.tests import *

class TestArchiveController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='archive'))
        # Test response...
