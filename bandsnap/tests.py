from django.test import TestCase
from django.contrib.auth.models import User
from .models import Skill, Artist, Band, Request
from django.urls import reverse

class SkillModelTest(TestCase):
    def setUp(self):
        Skill.objects.create(name="Guitar")

    def test_skill_creation(self):
        skill = Skill.objects.get(name="Guitar")
        self.assertEqual(skill.name, "Guitar")

class BandsnapViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('bandsnap:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bandsnap/index.html')

    def test_user_login(self):
        response = self.client.post(reverse('bandsnap:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to index upon successful login
        self.assertRedirects(response, reverse('bandsnap:index'))