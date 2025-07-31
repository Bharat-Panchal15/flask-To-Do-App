from app import create_app
import unittest

class TestBasicRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app("app.config.TestingConfig")

        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_dashboard_home(self):
        response = self.client.get('/dashboard/home')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard Home",response.data)
    
    def test_404_page(self):
        response = self.client.get('/doesnotexists')

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found",response.data)
    
    def test_500_page(self):
        response = self.client.get('/dashboard/error')
        
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Internal Server Error",response.data)