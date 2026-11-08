from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Todo_task


class TodoPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='todo-owner', password='password')
        self.client.force_login(self.user)
        self.task = Todo_task.objects.create(
            user=self.user,
            title='Restock packing supplies',
            discription='Check the storage shelf',
            category='Operations',
            due_date=date(2026, 11, 12),
        )

    def test_task_list_is_private_and_foreign_tasks_cannot_be_changed(self):
        other_user = User.objects.create_user(username='other-todo-owner', password='password')
        other_task = Todo_task.objects.create(
            user=other_user,
            title='Private task',
            discription='Do not show this to another user',
            category='Private',
            due_date=date(2026, 11, 13),
        )

        response = self.client.get(reverse('TODO:all_task'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restock packing supplies')
        self.assertNotContains(response, 'Private task')
        self.assertEqual(response.context['task'].count(), 1)

        for route_name in ('TODO:edit_task', 'TODO:delete_task'):
            response = self.client.get(reverse(route_name, args=[other_task.pk]))
            self.assertEqual(response.status_code, 404)

    def test_task_list_renders_tasks_and_actions(self):
        response = self.client.get(reverse('TODO:all_task'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restock packing supplies')
        self.assertContains(response, reverse('TODO:edit_task', args=[self.task.pk]))
        self.assertContains(response, reverse('TODO:delete_task', args=[self.task.pk]))

    def test_add_task_saves_and_redirects(self):
        response = self.client.post(reverse('TODO:add_task'), {
            'title': 'Count incoming stock',
            'discription': 'Verify the delivery',
            'category': 'Inventory',
            'due_date': '2026-11-15',
        })

        self.assertRedirects(response, reverse('TODO:all_task'))
        self.assertTrue(
            Todo_task.objects.filter(title='Count incoming stock', user=self.user).exists()
        )

    def test_edit_task_updates_and_renders_form(self):
        edit_url = reverse('TODO:edit_task', args=[self.task.pk])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restock packing supplies')

        response = self.client.post(edit_url, {
            'title': 'Restock shipping supplies',
            'discription': 'Check the storage shelf',
            'category': 'Operations',
            'due_date': '2026-11-13',
        })

        self.assertRedirects(response, reverse('TODO:all_task'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Restock shipping supplies')

    def test_delete_task_requires_post(self):
        delete_url = reverse('TODO:delete_task', args=[self.task.pk])

        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse('TODO:all_task'))
        self.assertTrue(Todo_task.objects.filter(pk=self.task.pk).exists())

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('TODO:all_task'))
        self.assertFalse(Todo_task.objects.filter(pk=self.task.pk).exists())
