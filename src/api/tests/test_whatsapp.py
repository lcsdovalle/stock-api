from unittest.mock import MagicMock, patch

from django.test import RequestFactory
from requests.models import Response
from rest_framework.test import APITestCase

from api.base_tests import BaseAuthenticatedAPITestCase
from api.views.whatsapp import WhatsappAPIView
from order.models.order import Order


class TestWhatsappAPIView(APITestCase, BaseAuthenticatedAPITestCase):
    def setUp(self) -> None:
        self.view = WhatsappAPIView()
        self.request_factory = RequestFactory()
        return super().setUp()

    @patch("api.views.whatsapp.requestAPI.post")
    def test_send_order_whatsapp_message_success(self, mock_post):
        """This test covers the happy path"""
        mock_post.return_value = MagicMock(status_code=200)
        order = Order.objects.filter(customer__isnull=False).first()
        result = self.view._WhatsappAPIView__send__order_whatsapp_message(
            order_model=order
        )
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch("api.views.whatsapp.requestAPI.post")
    def test_send_order_whatsapp_message_failure(self, mock_post):
        """This test covers the unhappy path"""
        mock_post.side_effect = Exception("Something wrong")
        with self.assertRaises(Exception) as exec:
            order = Order.objects.filter(customer__isnull=False).first()
            _ = self.view._WhatsappAPIView__send__order_whatsapp_message(
                order_model=order
            )

        assert isinstance(exec.exception, Exception)

    @patch("api.views.whatsapp.requestAPI.get")
    def test_get_qrcode_success(self, mock_get):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"qrcode": "mocked_qr_code"}
        mock_get.return_value = mock_response

        request = self.request_factory.get("/get-qrcode/")
        request.user = self.user

        order = Order.objects.filter(customer__isnull=False).first()
        response = self.view.get(request=request, order_model=order)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["qrcode"], "mocked_qr_code")
        mock_get.assert_called_once()
