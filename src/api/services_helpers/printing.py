import os
from datetime import datetime

from django.conf import settings  # Use settings instead of direct import
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable

from order.models.order import Order  # Adjust your import as needed


def save_order_pdf(order_id):
    order = Order.objects.get(pk=order_id)
    file_path = os.path.join(settings.MEDIA_ROOT, f"order_{order_id}.pdf")

    # Create a PDF document using SimpleDocTemplate
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Create a horizontal line
    line = HRFlowable(
        width="100%",
        thickness=1,
        lineCap="round",
        color=colors.sienna,
        spaceBefore=20,
        spaceAfter=20,
    )

    # Add elements to the PDF
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Paragraph(f"Orçamento número: {order.id}", styles["Heading1"]))
    elements.append(line)
    elements.append(
        Paragraph(
            f"Cliente: {order.customer.first_name} {order.customer.last_name}",
            styles["Heading3"],
        )
    )
    elements.append(Paragraph(f"Telefone: {order.customer.phone}", styles["Heading3"]))
    elements.append(Paragraph(f"Email: {order.customer.email}", styles["Heading3"]))
    elements.append(Paragraph(f"Total: R${order.total_price:.2f}", styles["Heading3"]))
    elements.append(Spacer(1, 24))
    # Table Data for Products
    data = [["Produto", "Preço unit", "Quantidade", "Preço total"]]
    for product_order in order.productorder_set.all():
        row = [
            product_order.product.name,
            f"${product_order.product.price_sale:.2f}",
            product_order.quantity,
            f"${product_order.product.price_sale * product_order.quantity:.2f}",
        ]
        data.append(row)

    # Create and style the table
    table = Table(data, colWidths="*")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 1), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 32))
    elements.append(line)
    elements.append(Paragraph(f"Feira de Santana, {now}", styles["Heading5"]))

    # Build the PDF
    doc.build(elements)
    print(f"Saved PDF to {file_path}")  # Debug print statement
    return file_path
