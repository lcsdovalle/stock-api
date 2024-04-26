from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from api.settings import API_VERSION
from api.views.whatsapp import WhatsappAPIView
from users.admin import admin_site

app_name = "api"  # Add the label for the app

urlpatterns = [
    path("admin/", admin_site.urls),
    path(f"{API_VERSION}/users/", include("users.urls")),
    path(f"{API_VERSION}/stock/", include("stock.urls")),
    path(f"{API_VERSION}/product/", include("product.urls")),
    path(f"{API_VERSION}/order/", include("order.urls")),
    path(f"{API_VERSION}/customer/", include("customer.urls")),
    path(f"{API_VERSION}/purchase/", include("purchase.urls")),
    path(
        f"{API_VERSION}/send-whatsapp-message/",
        WhatsappAPIView.as_view(),
        name="whatsapp",
    ),
]

# This is only suitable for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
