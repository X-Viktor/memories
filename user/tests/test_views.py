from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from user.models import Memory


class UserMemoryListViewTest(TestCase):

    def setUp(self):
        # Creation of two test users
        test_user1 = User.objects.create_user(username='test_user1', password='1a2b3c')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user2', password='1a2b3c')
        test_user2.save()

        # Create memories for test users
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            if book_copy % 2:
                user = test_user1
            else:
                user = test_user2
            Memory.objects.create(
                location='Memory Location',
                name='Memory Name',
                comment='Commentary on the memory.',
                user=user
            )

    def test_redirect_if_not_logged_in(self):
        """ Checks if the user is redirected to the main page if they are not logged in. """
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, '/?next=/home/')

    def test_logged_in_uses_correct_template(self):
        """ Checks if the correct template is displayed in home. """
        self.client.login(username='test_user1', password='1a2b3c')
        resp = self.client.get(reverse('home'))

        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'user/home.html')

    def test_only_memories_owned_by_user(self):
        """ Checks if all displayed memories belong to an authorized user. """
        self.client.login(username='test_user1', password='1a2b3c')
        resp = self.client.get(reverse('home'))

        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertEqual(resp.status_code, 200)

        for memory in resp.context['user'].memories.all():
            self.assertEqual(resp.context['user'], memory.user)
