from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Product


class ProductPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='inventory-owner', password='password')
        self.client.force_login(self.user)

    def test_product_list_renders_products(self):
        Product.objects.create(
            user=self.user,
            product_id='P-001',
            name='Notebook',
            category='Stationery',
            price=5,
            qty=10,
        )

        response = self.client.get(reverse('Inventory:all_Product'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notebook')
        self.assertContains(response, 'P-001')
        self.assertContains(response, '<td>50</td>', html=True)

    def test_inventory_is_private_and_product_ids_are_per_user(self):
        other_user = User.objects.create_user(username='other-owner', password='password')
        Product.objects.create(
            user=self.user,
            product_id='SHARED-ID',
            name='My product',
            category='Mine',
            price=5,
            qty=4,
        )
        other_product = Product.objects.create(
            user=other_user,
            product_id='SHARED-ID',
            name='Other product',
            category='Theirs',
            price=100,
            qty=50,
        )

        response = self.client.get(reverse('Inventory:all_Product'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My product')
        self.assertNotContains(response, 'Other product')
        self.assertEqual(response.context['inventory'].count(), 1)
        self.assertEqual(response.context['category_count'], 1)
        self.assertEqual(response.context['total_units'], 4)

        for route_name in ('Inventory:update_Product', 'Inventory:delete_Product'):
            response = self.client.get(reverse(route_name, args=[other_product.pk]))
            self.assertEqual(response.status_code, 404)

    def test_add_product_page_renders_and_saves_products(self):
        response = self.client.get(reverse('Inventory:add_Product'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

        response = self.client.post(
            reverse('Inventory:add_Product'),
            {
                'product_id': 'P-002',
                'name': 'Pen',
                'category': 'Stationery',
                'price': 2,
                'qty': 20,
            },
        )

        self.assertRedirects(response, reverse('Inventory:all_Product'))
        self.assertTrue(Product.objects.filter(product_id='P-002', user=self.user).exists())
