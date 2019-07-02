from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class AuthenticatedServiceClient:
    def is_authenticated(self):
        return True


class JwtServiceOnlyAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        # Assign properties from payload to the AuthenticatedServiceClient object if necessary
        return AuthenticatedServiceClient()
