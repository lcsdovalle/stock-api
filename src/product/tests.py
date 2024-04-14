# from django.contrib.auth.models import User
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase, override_settings

# from product.models.product import Product


# @override_settings(REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES": []})
# class ProductTests(APITestCase):
#     def setUp(self):
#         # Create some sample products
#         Product.objects.create(
#             name="Test Product 1",
#             description="Description 1",
#             price_sale=10.00,
#             price_purchase=5.00,
#             active=True,
#         )
#         Product.objects.create(
#             name="Test Product 2",
#             description="Description 2",
#             price_sale=20.00,
#             price_purchase=10.00,
#             active=False,
#         )
#         Product.objects.create(
#             name="Test Product 3",
#             description="Description 3",
#             price_sale=30.00,
#             price_purchase=15.00,
#             active=True,
#         )

#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.client.force_authenticate(user=self.user)

#     def test_get_active_products(self):
#         """
#         Ensure we can retrieve active products.
#         """
#         url = reverse("product:active_products")
#         response = self.client.get(url)

#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # pdb.set_trace()

#         # Check that we get only active products
#         for product in response.data["results"]:
#             self.assertTrue(product["active"])

#     def test_filter_products_by_id(self):
#         """
#         Ensure we can filter products by id.
#         """
#         url = reverse("product:active_products") + "?id=1"
#         response = self.client.get(url)

#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check that the response contains only the requested product
#         self.assertEqual(len(response.data["results"]), 1)
#         self.assertEqual(response.data["results"][0]["name"], "Test Product 1")
