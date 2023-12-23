from django.urls import path

from users.views.create_and_list import CreateUserView, ListUsersView
from users.views.login import LoginView

urlpatterns = [
    path("users", ListUsersView.as_view(), name="list_users"),
    path("user", CreateUserView.as_view(), name="create_users"),
    path("login", LoginView.as_view(), name="login"),
]
