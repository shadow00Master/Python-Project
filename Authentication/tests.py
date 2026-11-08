from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='workspace-user',
            email='workspace@example.com',
            password='SafePassword123!',
        )

    def test_root_redirects_to_login_for_signed_out_users(self):
        response = self.client.get('/')

        self.assertRedirects(response, reverse('Authentication:dashboard'))
        response = self.client.get(reverse('Authentication:dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('Authentication:login_view')}?next={reverse('Authentication:dashboard')}",
        )

    def test_dashboard_offers_both_apps_after_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('Authentication:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('Inventory:all_Product'))
        self.assertContains(response, reverse('TODO:all_task'))

    def test_inventory_and_todo_routes_require_login(self):
        for route_name in ('Inventory:all_Product', 'TODO:all_task'):
            response = self.client.get(reverse(route_name))
            self.assertRedirects(
                response,
                f"{reverse('Authentication:login_view')}?next={reverse(route_name)}",
            )

    def test_register_creates_and_signs_in_user(self):
        response = self.client.post(reverse('Authentication:register'), {
            'username': 'new-workspace-user',
            'email': 'new@example.com',
            'password1': 'AnotherSafePassword123!',
            'password2': 'AnotherSafePassword123!',
        })

        self.assertRedirects(response, reverse('Authentication:dashboard'))
        self.assertTrue(
            User.objects.filter(username='new-workspace-user').exists()
        )
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            User.objects.get(username='new-workspace-user').pk,
        )

    def test_login_respects_safe_next_path(self):
        response = self.client.post(
            f"{reverse('Authentication:login_view')}?next={reverse('TODO:all_task')}",
            {
                'username': self.user.username,
                'password': 'SafePassword123!',
                'next': reverse('TODO:all_task'),
            },
        )

        self.assertRedirects(response, reverse('TODO:all_task'))

    def test_logout_requires_post_and_returns_to_login(self):
        self.client.force_login(self.user)
        logout_url = reverse('Authentication:logout_view')

        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(logout_url)
        self.assertRedirects(response, reverse('Authentication:login_view'))
