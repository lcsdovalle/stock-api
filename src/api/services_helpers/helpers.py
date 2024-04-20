from order.models.order import Order
import datetime
import pytz
from order.models.product_order import ProductOrder
from customer.models.customer import Customer
import re
from django.contrib.auth.models import User

def __get_date() -> str:
    sao_paulo_timezone = pytz.timezone("America/Sao_Paulo")
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    sao_paulo_now = utc_now.astimezone(sao_paulo_timezone)

    return sao_paulo_now.strftime("%d/%m/%Y")

def __build_list_of_items_for_message(order_model: Order, format:str = "whatsapp") -> str:
    products: list[ProductOrder] = order_model.productorder_set.all()
    list_message: str = ""
    for product in products:
        if format == "whatsapp":
            list_message += f"*{product.product.name}*: R$ {product.product.price_sale} | QTD: {product.quantity}\n"
        else: 
            list_message += f"<b>{product.product.name}</b>: R$ {product.product.price_sale} | QTD: {product.quantity}<br>"
    return list_message


def generate_body_message(order_model: Order, format:str="whatsapp") -> str:
    customer: Customer = order_model.customer or None
    owner: User = order_model.owner
    if format == "whatsapp":
        message = f"""Olá {customer.first_name}\n\n*Aqui está seu orçamento*:\n\n{__build_list_of_items_for_message(order_model=order_model)}\n*TOTAL:* R$ {order_model.total_price}\n\n{__get_date()}\nAtenciosamente,\n\n{owner.first_name}"""
    else: 
        message = f"""Olá {customer.first_name}<br><br><b>Aqui está seu orçamento</b>:<br><br>{__build_list_of_items_for_message(order_model=order_model, format="email")}<br><b>TOTAL:</b> R$ {order_model.total_price}<br><br>{__get_date()}<br>Atenciosamente,<br><br>{owner.first_name}"""
    return message
