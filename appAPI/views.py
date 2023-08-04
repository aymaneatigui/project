from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from appAPI.models import MyUser
from appAPI.Serializer import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from appAPI.tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate



class UsersList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, OrderingFilter]  
    search_fields = ['^username','^first_name', '^last_name']  
    filterset_fields =['username','first_name','last_name']
    ordering_fields = ['username']

    def get(self, request, *args, **kwargs):
        users_data = self.filter_queryset(self.get_queryset())
        perpage = request.query_params.get('perpage',default=2)
        page= request.query_params.get('page',default=1)
        # paginator = Paginator(users_data,per_page=perpage)
        # try:
        #     users_data=paginator.page(number=page)
        # except EmptyPage:
        #     users_data = []

        serializer_data = UserSerializer(users_data, many = True)
        return Response({
            'Users Number': users_data.count(),
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
    permission_classes = [IsAuthenticated]

    def get_user(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(MyUser, pk=user_id)
    
    def get(self, request, *args, **kwargs):
        user = self.get_user()
        serializer_data = UserSerializer(user)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user = self.get_user()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        user = self.get_user()
        user.delete()
        return Response({"details":"User deleted successfully.",},status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated])
class message(GenericAPIView):
    def get(self,request):
        if request.user.groups.filter(name="Manager").exists():
            return Response({"Message":"secrete code"}, status=status.HTTP_200_OK)
        else:
            return Response({"Message":"You arent a manager"}, status=status.HTTP_403_FORBIDDEN)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUpView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "User Created Successfully", "data": serializer.data, "Token": tokens}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)