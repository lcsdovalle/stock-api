from django.urls import reverse

from api.base_tests import BaseAuthenticatedAPITestCase

# Create your tests here.


class OrderViewsTestCase(BaseAuthenticatedAPITestCase):
    fixtures = [
        "api/tests/fixtures/groups",
        "api/tests/fixtures/users",
        "customer/tests/fixtures/customers",
        "order/tests/fixtures/order",
    ]

    def test_order_list_view(self):
        list_order_url = reverse("order:order-list")
        response = self.client.get(list_order_url)
        data = response.json()
        count = len(data)

        self.assertGreater(count, 0)
        self.assertEqual(response.status_code, 200)

    def test_create_order_view(self):
        pass

    def test_add_product_to_order_view(self):
        pass

    def test_remove_product_from_order_view(self):
        pass
