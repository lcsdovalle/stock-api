import datetime

import pytz
from django.contrib.auth.models import User

from customer.models.customer import Customer
from order.models.order import Order
from order.models.product_order import ProductOrder


def __get_date() -> str:
    """
    Get the current date in the "America/Sao_Paulo" timezone.

    This function retrieves the current UTC time, converts it to the 
    "America/Sao_Paulo" timezone, and formats it as a string in the 
    "dd/mm/yyyy" format.

    Returns:
        str: The current date in the "America/Sao_Paulo" timezone, formatted as "dd/mm/yyyy".

    Example:
        >>> __get_date()
        '04/12/2024'
    """
    sao_paulo_timezone = pytz.timezone("America/Sao_Paulo")
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    sao_paulo_now = utc_now.astimezone(sao_paulo_timezone)

    return sao_paulo_now.strftime("%d/%m/%Y")


def __build_list_of_items_for_message(
    order_model: Order, format: str = "whatsapp"
) -> str:
    """
    Build a formatted list of items in an order for use in a message.

    This function generates a list of products in the given order, formatted either for 
    WhatsApp or email, including the product name, sale price, and quantity.

    Args:
        order_model (Order): The order instance containing the related product orders.
        format (str): The format of the list. Options are:
                      - "whatsapp": Formats the list using markdown-like syntax.
                      - "email": Formats the list using HTML-like syntax.
                      Default is "whatsapp".

    Returns:
        str: A formatted string representing the list of products in the order.

    Example:
        For WhatsApp:
        >>> __build_list_of_items_for_message(order_model, format="whatsapp")
        "*Product 1*: R$ 10.00 | QTD: 2\n*Product 2*: R$ 15.00 | QTD: 1\n"

        For Email:
        >>> __build_list_of_items_for_message(order_model, format="email")
        "<b>Product 1</b>: R$ 10.00 | QTD: 2<br><b>Product 2</b>: R$ 15.00 | QTD: 1<br>"
    """
    products: list[ProductOrder] = order_model.productorder_set.all()
    list_message: str = ""
    for product in products:
        if format == "whatsapp":
            list_message += f"*{product.product.name}*: R$ {product.product.price_sale} | QTD: {product.quantity}\n"
        else:
            list_message += f"<b>{product.product.name}</b>: R$ {product.product.price_sale} | QTD: {product.quantity}<br>"
    return list_message


def generate_body_message(order_model: Order, format: str = "whatsapp") -> str:
    """
    Generate a personalized message body for an order in a specified format.

    This function constructs a message for the customer, including the list of products, 
    total price, the current date, and a signature from the order owner. The message can 
    be formatted for WhatsApp or email.

    Args:
        order_model (Order): The order instance containing details such as the customer, 
                             owner, products, and total price.
        format (str): The format of the message. Options are:
                      - "whatsapp": Formats the message for WhatsApp using markdown-like syntax.
                      - "email": Formats the message for email using HTML-like syntax.
                      Default is "whatsapp".

    Returns:
        str: The generated message in the specified format.

    Example:
        For WhatsApp:
        >>> generate_body_message(order_model, format="whatsapp")
        "Olá John\n\n*Aqui está seu orçamento*:\n\n*Product 1*: R$ 10.00 | QTD: 2\n*TOTAL:* R$ 20.00\n\n01/01/2024\nAtenciosamente,\n\nLucas"

        For Email:
        >>> generate_body_message(order_model, format="email")
        "Olá John<br><br><b>Aqui está seu orçamento</b>:<br><br><b>Product 1</b>: R$ 10.00 | QTD: 2<br><b>TOTAL:</b> R$ 20.00<br><br>01/01/2024<br>Atenciosamente,<br><br>Lucas"
    """
    customer: Customer = order_model.customer or None
    owner: User = order_model.owner
    if format == "whatsapp":
        message = f"""Olá {customer.first_name}\n\n*Aqui está seu orçamento*:\n\n{__build_list_of_items_for_message(order_model=order_model)}\n*TOTAL:* R$ {order_model.total_price}\n\n{__get_date()}\nAtenciosamente,\n\n{owner.first_name}"""
    else:
        message = f"""Olá {customer.first_name}<br><br><b>Aqui está seu orçamento</b>:<br><br>{__build_list_of_items_for_message(order_model=order_model, format="email")}<br><b>TOTAL:</b> R$ {order_model.total_price}<br><br>{__get_date()}<br>Atenciosamente,<br><br>{owner.first_name}"""
    return message
