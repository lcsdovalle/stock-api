from django.contrib import admin

from customer.models.customer import Customer
from users.admin import admin_site


class MyCustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "cpf",
        "rg",
        "created_at",
        "updated_at",
    )  # Display these fields in the admin list
    list_editable = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "cpf",
        "rg",
    )  # Enable editing of the discount field in the admin list


admin_site.register(Customer, MyCustomerAdmin)
