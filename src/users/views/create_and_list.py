from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.serializers.user import UserSerializer


class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]  # Or another permission class
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
