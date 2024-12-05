from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_header(self, request):
        """
        Return the authentication header for a Bearer token.

        This method overrides the `authenticate_header` method from the 
        `TokenAuthentication` class to specify the "Bearer" authentication scheme 
        used in Authorization headers.

        Args:
            request: The HTTP request object. This is typically provided by Django 
                    and contains metadata about the current request.

        Returns:
            str: The string "Bearer", which indicates the authentication scheme 
                expected in the `Authorization` header.

        Example:
            A client should include the following header in their request:
            Authorization: Bearer <your_token>
        """
        return "Bearer"
