from snapshot.tests import *

class TestRootController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='root'))
        # Test response...
