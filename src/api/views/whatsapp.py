# isort: skip_file
from rest_framework.views import APIView
from order.models.order import Order
from api.settings.base import VENON_BOT_ENDPOINT
from rest_framework.response import Response
from django.contrib.auth.models import User
import requests as requestAPI
from rest_framework.request import Request
from customer.models.customer import Customer
import re
from api.services_helpers.helpers import generate_body_message
import logging


class WhatsappAPIView(APIView):
    def __sanitize_phone(self, phone: str) -> str:
        if phone:
            sanitized_phone = re.sub(r"\D", "", phone)
            return sanitized_phone
        return ""

    def __send__order_whatsapp_message(self, order_model: Order) -> bool:
        try:
            owner: User = order_model.owner
            customer: Customer = order_model.customer or None
            if customer and customer.phone:
                response = requestAPI.post(
                    f"{VENON_BOT_ENDPOINT}/send-message",
                    json={
                        "sessionName": owner.username,
                        "phoneNumber": self.__sanitize_phone(customer.phone),
                        "textMessage": generate_body_message(order_model=order_model),
                    },
                )
        except Exception as e:
            logging.error("Erro while trying to communicate with Whatsapp API")
            raise e
        else:
            if status_code := getattr(response, "status_code", None):
                return status_code == 200
            return status_code == 200

    def post(self, request: Request):
        """This starts a session on venon service"""
        try:
            order_id = request.data.get("order_id")
            order_model = Order.objects.get(pk=order_id)
            sent = self.__send__order_whatsapp_message(order_model=order_model)
            if sent:
                return Response("OK", 200)
            return Response("Not sent", 400)
        except Exception as e:
            raise e

    def get(self, request: Request, *args, **kwargs):
        """This checks if the qr code the session is available"""
        user: User = request.user
        result = requestAPI.get(
            url=f"{VENON_BOT_ENDPOINT}/get-qrcode",
            params={"sessionName": user.username},
        )
        data: dict = result.json()
        if data.get("qrcode", None):
            return Response(data={"qrcode": data.get("qrcode")}, status=200)
        return Response(data="Not cound", status=404)
