from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.settings.base import FIXTURES_LOAD_SEQUENCE
from order.models.order import Order


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.SessionAuthentication",
        ),
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    }
)
class BaseAuthenticatedAPITestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up the test environment for authenticated API test cases.

        This method is executed before each test case in the `BaseAuthenticatedAPITestCase`
        class. It performs the following tasks:
        
        1. Loads the fixture data specified in `FIXTURES_LOAD_SEQUENCE` into the test database.
        2. Retrieves the first order's owner as the test user.
        3. Creates an authentication token for the test user.
        4. Configures the `APIClient` with the token for authenticated API requests.
        5. Forces authentication for the test client with the test user.

        This ensures all test cases have a consistent and authenticated setup.

        Returns:
            None
        """
        for fixture in FIXTURES_LOAD_SEQUENCE:
            call_command("loaddata", fixture)
        self.user = Order.objects.first().owner
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {self.token.key}"
        self.client.force_authenticate(user=self.user)
        return super().setUp()
