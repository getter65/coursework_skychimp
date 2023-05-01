from rest_framework import generics
from rest_framework.response import Response

from users.models import User
from users.permissions import UserChangeUserPermissionManager
from users.serializers import UserSerializer, ProfileSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance:
            serializer = UserSerializer
        else:
            serializer = ProfileSerializer
        return Response(serializer(instance).data)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserChangeUserPermissionManager]
