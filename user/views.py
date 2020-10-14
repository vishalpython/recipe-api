from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserModelSerializers,AuthTokenSeralizer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserModelSerializers


class CreateTokenView(ObtainAuthToken):
    """Create the new authh token for user"""
    serializer_class = AuthTokenSeralizer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authentcated user"""
    serializer_class = UserModelSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive and return aunthecation user"""
        return self.request.user