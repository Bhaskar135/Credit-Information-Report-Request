import unittest
from flask import current_app
from app import create_app,db

class BasicsTestCase(unittest.TestCase): 
    #def setUp(self):
        #self.app=create_app('testing')	# Creates an application configured for testing
        #self.app_context=self.app.app_context()     # activates the context
        #self.app_context.push()
        #db.create_all()
    
    #def tearDown(self):         # database and application context are removed here
        #db.session.remove()
        #db.drop_all()
        #self.app_context.pop()


    def test_app_exists(self):       # ensures application instance exists
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):     # ensures application is running under the testing configuration
        self.assertTrue(current_app.config['TESTING'])