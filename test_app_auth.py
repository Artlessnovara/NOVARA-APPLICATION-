import unittest
from app import create_app, db
from models import User
import os

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a new application context."""
        os.environ['FLASK_ENV'] = 'testing'
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,  # Disable CSRF for simpler testing
            "SERVER_NAME": "localhost" # Required for url_for to work in tests
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_page_loads(self):
        """Test that the signup page loads correctly."""
        with self.app.app_context():
            response = self.client.get('/auth/signup')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sign Up', response.data)

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        with self.app.app_context():
            response = self.client.get('/auth/login')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_successful_signup(self):
        """Test a user can sign up successfully."""
        with self.app.app_context():
            response = self.client.post('/auth/signup', data={
                'full_name': 'Test User',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'role': 'Student'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have successfully signed up! Please login.', response.data)
            # Check if user was actually created
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)

    def test_successful_login_and_logout(self):
        """Test a registered user can login and then logout."""
        with self.app.app_context():
            # First, create a user to login with
            self.client.post('/auth/signup', data={
                'full_name': 'Login Test',
                'email': 'login@example.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'role': 'Student'
            })

            # Test login
            response = self.client.post('/auth/login', data={
                'email': 'login@example.com',
                'password': 'password123'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            # A new user is redirected to the welcome page
            self.assertIn(b'Welcome to Scholars Novara Institute', response.data)

            # Test logout
            logout_response = self.client.get('/auth/logout', follow_redirects=True)
            self.assertEqual(logout_response.status_code, 200)
            # After logout, user should be redirected to a page with a Login link
            self.assertIn(b'Login', logout_response.data)


if __name__ == '__main__':
    unittest.main()
