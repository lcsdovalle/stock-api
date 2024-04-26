from django.urls import path

from customer.views.customer import CustomerByCPFView, CustomerCreateView, CustomerListView

app_name = "customer"  # Add the label for the app

urlpatterns = [
    path("read/<str:cpf>/", CustomerByCPFView.as_view(), name="customer_by_cpf"),
    path("list/", CustomerListView.as_view(), name="customer_list"),
    path("create/", CustomerCreateView.as_view(), name="customer_create"),
]
