from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Skill, Artist, Band, Request
from django.urls import reverse

class SkillModelTest(TestCase):
    def setUp(self):
        Skill.objects.create(name="Guitar")
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.artist = Artist.objects.create(user=self.user1, photo='path/to/photo', description='Description')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')
        self.band = Band.objects.create(user=self.user2, photo='path/to/photo', description='Description')
        self.request = Request.objects.create(artist=self.artist, band=self.band, accepted=False)

    def test_skill_creation(self):
        skill = Skill.objects.get(name="Guitar")
        self.assertEqual(skill.name, "Guitar")
    def test_artist_creation(self):
        artist_count = Artist.objects.count()
        self.assertEqual(artist_count, 1, "Incorrect number of artists created")
    def test_band_creation(self):
        band_count = Band.objects.count()
        self.assertEqual(band_count, 1, "Incorrect number of bands created")
    def test_request_creation(self):
        request_count = Request.objects.count()
        self.assertEqual(request_count, 1, "Incorrect number of requests created")

class BandsnapViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('bandsnap:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bandsnap/index.html')

    def test_signup_view(self):
        response = self.client.get(reverse('bandsnap:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bandsnap/signup.html')

    def test_search_view(self):
        response = self.client.get(reverse('bandsnap:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bandsnap/search.html')

    def test_about_view(self):
        response = self.client.get(reverse('bandsnap:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bandsnap/about.html')

    def test_user_login(self):
        response = self.client.post(reverse('bandsnap:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to index upon successful login
        self.assertRedirects(response, reverse('bandsnap:index'))