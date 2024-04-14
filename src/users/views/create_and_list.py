from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing users and their groups.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter the queryset based on the logged-in user's rights or other business logic
        return super().get_queryset()
