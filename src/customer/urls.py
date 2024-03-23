from django.urls import path

from customer.views.customer import CustomerByCPFView

app_name = "customer"  # Add the label for the app

urlpatterns = [
      path('<str:cpf>/', CustomerByCPFView.as_view(), name='customer_by_cpf'),
    
]
