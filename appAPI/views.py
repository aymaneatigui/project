from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from appAPI.models import MyUser
from appAPI.Serializer import UserSerializer

class UsersList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = MyUser.objects.all()
        serializer_data = UserSerializer(queryset, many = True)
        return Response({
            'Users Number': queryset.count(),
            'Users': serializer_data.data
        }, status = status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer_data = UserSerializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status = status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRUD(GenericAPIView, ListModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    
    def get_user(self, user_id):
        return get_object_or_404(MyUser, pk=user_id)
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = self.get_user(user_id)
        serializer_data = UserSerializer(user)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = self.get_user(user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = self.get_user(user_id)
        user.delete()
        return Response({"details":"User deleted successfully.",},status=status.HTTP_204_NO_CONTENT)
