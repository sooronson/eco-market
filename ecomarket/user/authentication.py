from rest_framework.authentication import BaseAuthentication
from . import exceptions
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings


cred = credentials.Certificate({
        "type": settings.FIREBASE_ACCOUNT_TYPE,
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
        "private_key": settings.FIREBASE_PRIVATE_KEY,
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": settings.FIREBASE_CLIENT_ID,
        "auth_uri": settings.FIREBASE_AUTH_URI,
        "token_uri": settings.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL
})

default_app = firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.NoAuthToken("No authorization token is provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()

        user, created = User.objects.get_or_create(username=uid)

        return (user, None)



