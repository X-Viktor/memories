from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        # Create a test user
        test_user1 = User.objects.create_user(username='test_user1', password='1a2b3c')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        """ Checks if the user is redirected to the main page if they are not logged in. """
        resp = self.client.get(reverse('memory_create'))
        self.assertRedirects(resp, '/?next=/home/create')

    def test_logged_in_uses_correct_template(self):
        """ Checks if the correct template is displayed in home. """
        self.client.login(username='test_user1', password='1a2b3c')
        resp = self.client.get(reverse('memory_create'))

        self.assertEqual(str(resp.context['user']), 'test_user1')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'user/memory-create.html')

    def test_redirects_to_all_memories_list_on_success(self):
        """ Checks that the user is redirected to the home page on successful memory creation. """
        self.client.login(username='test_user1', password='1a2b3c')
        resp = self.client.post(
            reverse(viewname='memory_create'),
            {
                'location': 'Memory Location',
                'name': 'Memory Name',
                'comment': 'Commentary on the memory.',
            }
        )

        self.assertRedirects(resp, reverse('home'))

    def test_404_if_not_logged_in(self):
        """ Checks that an unauthorized user cannot create a new memory. """
        resp = self.client.post(
            reverse(viewname='memory_create'),
            {
                'location': 'Memory Location',
                'name': 'Memory Name',
                'comment': 'Commentary on the memory.',
            }
        )

        self.assertEqual(resp.status_code, 404)

    def test_add_new_memory_to_user(self):
        """ Checks if a new memory has appeared in the user's profile. """
        self.client.login(username='test_user1', password='1a2b3c')
        resp = self.client.get(reverse('home'))

        self.assertEqual(list(resp.context['user'].memories.all()), [])

        self.client.post(
            reverse('memory_create'),
            {
                'location': 'Memory Location',
                'name': 'New Memory Name',
                'comment': 'Commentary on the memory.',
            }
        )

        self.assertEqual(resp.context['user'].memories.get().name, 'New Memory Name')
