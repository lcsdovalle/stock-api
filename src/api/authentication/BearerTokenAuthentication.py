from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_header(self, request):
        return "Bearer"
