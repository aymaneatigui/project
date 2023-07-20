from appAPI.models import User
from appAPI.Serializer import UserSerializer
from rest_framework import generics
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
