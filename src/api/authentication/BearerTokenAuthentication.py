from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_header(self, request):
        return "Bearer"
