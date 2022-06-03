from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser('admin@admin.com', 'admin_1234567890')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user('test@test.com', 'test', name='Test User')

    def test_users_listed(self):
        """ > Probar que los usuarios han sido listados en la página de usuario """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
