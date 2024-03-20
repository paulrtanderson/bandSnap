from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Skill, Gig, Artist, Band, Request
from .views import index, signup, user_login, search, about, restricted, user_logout, user_profile

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.skill1 = Skill.objects.create(name="Skill1")
        self.skill2 = Skill.objects.create(name="Skill2")
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')
        self.artist = Artist.objects.create(user=self.user1, photo='path/to/photo', description='Description')
        self.band = Band.objects.create(user=self.user2, photo='path/to/photo', description='Description')
        self.gig = Gig.objects.create(name="Gig", date='2024-03-20', venue_address='Venue', description='Description')
        self.request = Request.objects.create(artist=self.artist, band=self.band, accepted=False)

    def test_skill_creation(self):
        skill_count = Skill.objects.count()
        self.assertEqual(skill_count, 2, "Incorrect number of skills created")

    def test_artist_creation(self):
        artist_count = Artist.objects.count()
        self.assertEqual(artist_count, 1, "Incorrect number of artists created")

    def test_band_creation(self):
        band_count = Band.objects.count()
        self.assertEqual(band_count, 1, "Incorrect number of bands created")

    def test_request_creation(self):
        request_count = Request.objects.count()
        self.assertEqual(request_count, 1, "Incorrect number of requests created")

    def test_request_accepted_default(self):
        self.assertFalse(self.request.accepted, "Request accepted flag is not set to False by default")

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        request = self.factory.get('/index/')
        response = index(request)
        self.assertEqual(response.status_code, 200, "Index view returned unexpected status code")

    def test_signup_view(self):
        request = self.factory.get('/signup/')
        response = signup(request)
        self.assertEqual(response.status_code, 200, "Signup view returned unexpected status code")

    def test_user_login_view(self):
        # Create a test user
        User.objects.create_user(username='testuser', password='password')
        
        # Test login with correct credentials
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'password'})
        response = user_login(request)
        self.assertEqual(response.status_code, 302, "User login with correct credentials failed")

        # Test login with incorrect credentials
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        response = user_login(request)
        self.assertEqual(response.status_code, 200, "User login with incorrect credentials failed")

    def test_search_view(self):
        request = self.factory.get('/search/')
        response = search(request)
        self.assertEqual(response.status_code, 200, "Search view returned unexpected status code")

    def test_about_view(self):
        request = self.factory.get('/about/')
        response = about(request)
        self.assertEqual(response.status_code, 200, "About view returned unexpected status code")

    def test_restricted_view(self):
        request = self.factory.get('/restricted/')
        response = restricted(request)
        self.assertEqual(response.status_code, 302, "Restricted view did not redirect to login if not logged in")

    def test_user_logout_view(self):
        request = self.factory.get('/logout/')
        request.user = User.objects.create_user(username='testuser', password='password')
        response = user_logout(request)
        self.assertEqual(response.status_code, 302, "User logout did not redirect to index after logout")

    def test_user_profile_view(self):
        request = self.factory.get('/profile/')
        request.user = User.objects.create_user(username='testuser', password='password')
        response = user_profile(request)
        self.assertEqual(response.status_code, 200, "User profile view returned unexpected status code")